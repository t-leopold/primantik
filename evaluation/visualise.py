from typing import cast
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.regression.mixed_linear_model as mlm
import arviz as az
import bambi as bmb

def plot_rt(df, figures_dir: str, show: bool = False) -> None:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='relationship', y='rt', hue='soa', data=df)
    plt.title('Reaction Times by SOA and Relationship (Raw Data)')
    plt.ylabel('Reaction Time [ms]')
    plt.xlabel('Relationship Type')
    plt.legend(title='SOA [ms]')
    plt.tight_layout()
    plt.savefig(figures_dir)
    if show:
        plt.show()

def plot_response(df, figures_dir: str, show: bool = False) -> None:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='relationship', y='response', hue='soa', data=df)
    plt.title('Response correctness by SOA and Relationship (Raw Data)')
    plt.ylabel('Response correctness')
    plt.xlabel('Relationship Type')
    plt.legend(title='SOA [ms]')
    plt.tight_layout()
    plt.savefig(figures_dir)
    if show:
        plt.show()

def plot_emm_rt(df: pd.DataFrame, model: mlm.MixedLM | bmb.Model, figures_dir: str, show: bool = True) -> None:
    predict_df = df[['soa', 'relationship']].drop_duplicates().copy()
    predict_df['participant'] = 'p1' # Dummy participant for prediction

    # Get model matrix and predictions
    if isinstance(model, mlm.MixedLM):
        results: mlm.MixedLMResultsWrapper = model.fit()
        predict_df['predicted_rt'] = results.predict(predict_df)
    else:
        results: az.InferenceData = model.fit()
        predict_df['predicted_rt'] = model.predict(results)

    # Plot estimated marginal means
    plt.figure(figsize=(10, 6))
    sns.pointplot(x='relationship', y='predicted_rt', hue='soa', data=predict_df)
    plt.title('Model-Predicted Reaction Times')
    plt.ylabel('Predicted RT [ms]')
    plt.xlabel('Relationship Type')
    plt.legend(title='SOA [ms]')
    plt.tight_layout()
    plt.savefig(figures_dir)
    if show:
        plt.show()

def plot_emm_response(df: pd.DataFrame, model: bmb.Model, figures_dir: str, show: bool = True) -> None:
    predict_df = df[['soa', 'relationship']].drop_duplicates().copy()
    predict_df['participant'] = 'p1' # Dummy participant for prediction

    # Get model matrix and predictions
    results: az.InferenceData = model.fit()
    predict_df['predicted_response'] = model.predict(results)

    # Plot estimated marginal means
    plt.figure(figsize=(10, 6))
    sns.pointplot(x='relationship', y='predicted_response', hue='soa', data=predict_df)
    plt.title('Model-Predicted Response correctness')
    plt.ylabel('Predicted Response correctness')
    plt.xlabel('Relationship Type')
    plt.legend(title='SOA [ms]')
    plt.tight_layout()
    plt.savefig(figures_dir)
    if show:
        plt.show()
