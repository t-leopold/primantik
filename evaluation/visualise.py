import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.regression.mixed_linear_model as mlm

# Plot 1: Raw data - RTs by SOA and Relationship
def plot_rt(df, figures_dir: str, show: bool = False) -> None:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='relationship', y='rt', hue='soa', data=df)
    plt.title("Reaction Times by SOA and Relationship (Raw Data)")
    plt.ylabel("Reaction Time [ms]")
    plt.xlabel("Relationship Type")
    plt.legend(title="SOA")
    plt.tight_layout()
    plt.savefig(figures_dir)
    if show:
        plt.show()

# Plot 2: Estimated marginal means from the model
def plot_emm(df: pd.DataFrame, results: mlm.MixedLMResultsWrapper, figures_dir: str, show: bool = True) -> None:
    predict_df = df[['soa', 'relationship']].drop_duplicates().copy()
    predict_df['participant'] = 'p1' # Dummy participant for prediction

    # Get model matrix and predictions
    predict_df['predicted_rt'] = results.predict(predict_df)

    # Plot estimated marginal means
    plt.figure(figsize=(10, 6))
    sns.pointplot(x='relationship', y='predicted_rt', hue='soa', data=predict_df)
    plt.title("Model-Predicted Reaction Times")
    plt.ylabel("Predicted RT [ms]")
    plt.xlabel("Relationship Type")
    plt.legend(title="SOA")
    plt.tight_layout()
    plt.savefig(figures_dir)
    if show:
        plt.show()
