import json
from os import path
import pandas as pd
import statsmodels.formula.api as smf
import scipy.stats as stats
import visualise_results

conditions_file: str = path.join(path.dirname(__file__), '../conditions-experiment.csv')
processed_results: str = path.join(path.dirname(__file__), '../results/results-processed.txt')

# Load the relationship mapping from the CSV
# This CSV must have: 'condition', 'prime', 'target' columns
relationship_df = pd.read_csv(conditions_file)

# Create a lookup dictionary for faster matching
# Keys are (prime, target) tuples
relationship_lookup: dict[tuple[str, str], str] = {
    (row['prime'], row['target']): row['condition']
    for _, row in relationship_df.iterrows()
}

# Load the participant trial data from the JSON lines text file
data: list[dict[str, str | int]] = []
with open(processed_results, 'r') as f:
    for i, line in enumerate(f):
        participant_id = f'p{i+1}'
        try:
            trials = json.loads(line.strip())
            for trial in trials:
                prime = trial['prime']
                target = trial['target']
                rt = trial['rt']
                soa = trial['soa_soll']
                
                # Look up the relationship
                key = (prime, target)
                relationship = relationship_lookup.get(key, None)

                if relationship is None:
                    print(f'Warning: No relationship found for {key}, skipping...')
                    continue  # Skip this trial if relationship is missing

                data.append({
                    'participant': participant_id,
                    'soa': soa,
                    'prime': prime,
                    'target': target,
                    'rt': rt,
                    'relationship': relationship
                })
        except json.JSONDecodeError:
            print(f'Skipping invalid line {i+1}')

# Convert to DataFrame
df = pd.DataFrame(data)

# Ensure categorical variables
df['soa'] = df['soa'].astype('category')
df['relationship'] = df['relationship'].astype('category')
df['participant'] = df['participant'].astype('category')

# Full model with interaction
full_model = smf.mixedlm('rt ~ soa * relationship', df, groups=df['participant'])
full_result = full_model.fit()

# Reduced model without interaction
reduced_model = smf.mixedlm('rt ~ soa + relationship', df, groups=df['participant'])
reduced_result = reduced_model.fit()

# Calculate LRT statistic
ll_full = full_result.llf  # Log-likelihood of full model
ll_reduced = reduced_result.llf  # Log-likelihood of reduced model

lr_stat = 2 * (ll_full - ll_reduced)
df_diff = full_result.df_modelwc - reduced_result.df_modelwc  # Difference in number of parameters
p_value = stats.chi2.sf(lr_stat, df_diff)

print(f'Likelihood Ratio Test:')
print(f'  LR stat = {lr_stat:.3f}')
print(f'  df = {df_diff}')
print(f'  p-value = {p_value:.4f}')

preferred_model_result = None

if p_value < 0.05:
    print('\n✅ The interaction significantly improves model fit.\n')
    preferred_model_result = full_result
else:
    print('\n❌ The interaction does not significantly improve model fit.\n')
    preferred_model_result = reduced_result

# Show summary
print(preferred_model_result.summary())

visualise_results.plot_rt(df)
visualise_results.plot_emm(df, preferred_model_result)
