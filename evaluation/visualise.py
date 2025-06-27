import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import bootstrap

# Plot 1: Raw data - RTs by SOA and Relationship
def plot_rt(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='relationship', y='rt', hue='soa', data=df)
    plt.title("Reaction Times by SOA and Relationship (Raw Data)")
    plt.ylabel("Reaction Time (ms)")
    plt.xlabel("Relationship Type")
    plt.legend(title="SOA")
    plt.tight_layout()
    plt.show()

# Plot 2: Estimated marginal means from the model
# Create a grid of predictor combinations
def plot_emm(df, result):
    predict_df = df[['soa', 'relationship']].drop_duplicates().copy()
    predict_df['participant'] = 'p1'  # Dummy participant for prediction

    # Step 1: Get model matrix and predictions
    predict_df['predicted_rt'] = result.predict(predict_df)

    # Step 2: Compute bootstrapped 95% CIs per soa × relationship
    def compute_bootstrap_ci(x):
        x = np.array(x)
        if len(x) < 2:
            return (np.nan, np.nan)  # Cannot compute CI on 1 value
        res = bootstrap((x,), np.mean, confidence_level=0.95, n_resamples=1000, method='basic')
        return res.confidence_interval.low, res.confidence_interval.high

    summary = predict_df.groupby(['soa', 'relationship'])['predicted_rt'].agg(
        mean='mean',
        ci_low=lambda x: compute_bootstrap_ci(x)[0],
        ci_high=lambda x: compute_bootstrap_ci(x)[1]
    ).reset_index()

    summary['ci_width'] = summary['ci_high'] - summary['mean']

    # Step 3: Plot
    plt.figure(figsize=(10, 6))
    sns.pointplot(
        data=summary,
        x='relationship',
        y='mean',
        hue='soa',
        dodge=0.3,
        join=True,
        markers=['o', 's'],
        linestyles='-',
        errwidth=1,
        ci=None  # We'll add custom error bars below
    )

    # Add manual error bars using the bootstrapped CIs
    for i, row in summary.iterrows():
        x_offset = -0.2 if row['soa'] == 'short' else 0.2
        x_base = ['Unrelated', 'Semantic', 'Associative'].index(row['relationship'])
        
        x = x_base + x_offset
        plt.errorbar(
            x=x,
            y=row['mean'],
            yerr=[[row['mean'] - row['ci_low']], [row['ci_high'] - row['mean']]],
            fmt='none',
            color='black',
            capsize=5,
            elinewidth=1
        )

    # Plot estimated marginal means
    plt.title("Model-Predicted Reaction Times with 95% Confidence Intervals")
    plt.ylabel("Predicted RT (ms)")
    plt.xlabel("Relationship Type")
    plt.legend(title="SOA")
    plt.tight_layout()
    plt.show()
