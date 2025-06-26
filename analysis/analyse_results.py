import json
from os import path
import pandas as pd
import statsmodels.formula.api as smf
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

# Fit the linear mixed model
model = smf.mixedlm('rt ~ soa * relationship', df, groups=df['participant'])
result = model.fit()

# Show summary
print(result.summary())

visualise_results.plot_rt(df)
visualise_results.plot_emm(df, result)
