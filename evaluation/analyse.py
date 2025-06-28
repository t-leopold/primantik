import json
from functools import reduce
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import scipy.stats as stats
import bambi as bmb
import arviz as az
from custom_types import *

def load_relationship_data(file: str) -> RelationshipDict:
    relationship_df = pd.read_csv(file)
    relationship_lookup: RelationshipDict = {
        (row['prime'], row['target']): row['condition']
        for _, row in relationship_df.iterrows()
    }
    return relationship_lookup

def load_trial_data(trial_data: str, relation_data: str, dependence: str) -> TrialsList:
    relationship_lookup: RelationshipDict = load_relationship_data(relation_data)
    data: list[dict[str, ProValue]] = []

    with open(trial_data, 'r') as file:
        for i, line in enumerate(file):
            participant_id = f'p{i+1}'
            try:
                trials = json.loads(line.strip())
                for trial in trials:
                    if dependence == 'rt' and trial['response'] != True:
                        continue
                    response = trial['response']
                    prime = trial['prime']
                    target = trial['target']
                    rt = trial['rt']
                    soa = trial['soa_soll']
                    
                    # Look up the relationship
                    key = (prime, target)
                    relationship = relationship_lookup.get(key, None)

                    if relationship is None:
                        # print(f'Warning: No relationship found for {key}, skipping...')
                        continue

                    data.append({
                        'participant': participant_id,
                        'soa': soa,
                        # 'prime': prime,
                        # 'target': target,
                        'rt': rt,
                        'response': response,
                        'relationship': relationship
                    })
            except json.JSONDecodeError:
                print(f'Skipping invalid line {i+1}')
    return data

def analyse_metadata(metadata_file: str) -> dict[str, int | float]:
    ages: list[int] = []
    sexes: list[str] = []

    with open(metadata_file, 'r') as file:
        try:
            metadata = json.loads(file.readline().strip())
            for participant in metadata:
                ages.append(participant['alter'])
                sexes.append(participant['geschlecht'])

        except json.JSONDecodeError:
            print(f'Error in metadata file.')

    analysed: dict[str, int | float] = {
        'min_age' : min(ages),
        'max_age' : max(ages),
        'mean_age' : float(np.mean(ages)),
        'num_fem' : reduce(lambda acc, val: acc+1 if val == 'f' else acc, sexes, 0),
        'num_mas' : reduce(lambda acc, val: acc+1 if val == 'm' else acc, sexes, 0)
    }

    for k, v in analysed.items():
        print(f'{k} = {v}')

    return analysed

def calculate_model_stats(interaction: Interaction, trial_data: str, relation_data: str):
    type_of_model: dict[Interaction, str] = {
        True : f'rt ~ soa * relationship',
        False : f'rt ~ soa + relationship'
    }
    df = pd.DataFrame(load_trial_data(trial_data, relation_data, 'rt'))
    df['soa'] = pd.Categorical(df['soa'], categories=[50, 850])
    df['relationship'] = pd.Categorical(df['relationship'], categories=['Unrelated', 'Associative', 'Semantic'])
    df['participant'] = df['participant'].astype('category')

    return smf.mixedlm(type_of_model[interaction], df, groups=df['participant'])

def calculate_model_bambi(interaction: Interaction, dependence: DependentVariable, trial_data: str, relation_data: str):
    random_intercepts: str = '(1|participant)'
    type_of_model: dict[Interaction, str] = {
        True : f'{dependence} ~ soa * relationship + {random_intercepts}',
        False : f'{dependence} ~ soa + relationship + {random_intercepts}'
    }
    df = pd.DataFrame(load_trial_data(trial_data, relation_data, dependence))
    df['soa'] = pd.Categorical(df['soa'], categories=[50, 850])
    df['relationship'] = pd.Categorical(df['relationship'], categories=['Unrelated', 'Associative', 'Semantic'])
    df['participant'] = df['participant'].astype('category')

    family: str = 'gaussian'
    if dependence == 'response':
        family = 'bernoulli'
    return bmb.Model(type_of_model[interaction], df, family=family)

def show_model_results_stats(model):
    results = model.fit()
    print(results.summary())

def show_model_results_bambi(model):
    results = model.fit(tune=1000, draws=1000)
    print(az.summary(results))

def calculate_lrt_stats(dependence: DependentVariable, trial_data: str, relation_data: str) -> tuple[float, float, float]:
    result_full = calculate_model_stats(True, trial_data, relation_data).fit()
    result_reduced = calculate_model_stats(False, trial_data, relation_data).fit()

    lr_stat = 2 * (result_full.llf - result_reduced.llf)
    df_diff = result_full.df_modelwc - result_reduced.df_modelwc
    p_value = stats.chi2.sf(lr_stat, df_diff)
    return (lr_stat, df_diff, p_value)

def show_lrt_results(lr_stat, df_diff, p_value):
    print(f'Likelihood Ratio Test:')
    print(f'  LR stat = {lr_stat:.3f}')
    print(f'  df = {df_diff}')
    print(f'  p-value = {p_value:.4f}')

    if p_value < 0.05:
        print('\n✅ The interaction significantly improves model fit.\n')
    else:
        print('\n❌ The interaction does not significantly improve model fit.\n')
