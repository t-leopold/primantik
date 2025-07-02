import argparse
from os import path
import arviz as az
from custom_types import *
from evaluation.process import process_results, extract_metadata
from evaluation.analyse import calculate_correct_responses, calculate_lrt_stats, show_lrt_results, show_model_results_stats, calculate_model_stats, show_model_results_bambi, calculate_model_bambi, analyse_metadata
from evaluation.visualise import plot_response, plot_rt, plot_emm_rt_statsmodels, plot_emm_rt_bambi, plot_emm_response

DATA: dict[DataFiles, str] = {
    "conditions": "./conditions-experiment.csv",
    "results raw": "./results/results-raw.txt",
    "results processed": "./results/results-processed.txt",
    "metadata": "./results/metadata.txt",
    "plots": "./plots/"
}
SCRIPTS: dict[Scripts, str] = {
    "process": "./evaluation/process.py",
    "analyse": "./evaluation/analyse.py"
}
base_path: str = path.dirname(path.abspath(__file__))
trial_data_path: str = path.join(base_path, DATA["results processed"])
relation_data_path: str = path.join(base_path, DATA["conditions"])

def run_glmm_bambi(interaction: bool) -> None:
    print("Running GLMM with Bambi...")
    df, model = calculate_model_bambi(interaction, 'response', trial_data_path, relation_data_path)
    results: az.InferenceData = show_model_results_bambi(model)
    plot_emm_response(df, model, results, path.join(base_path, f'{DATA["plots"]}response-bambi-{'inter' if interaction else 'indep'}.pdf'))

def run_lmm_bambi(interaction: bool) -> None:
    print("Running LMM with Bambi...")
    df, model = calculate_model_bambi(interaction, 'rt', trial_data_path, relation_data_path)
    results: az.InferenceData = show_model_results_bambi(model)
    plot_rt(df, path.join(base_path, f'{DATA["plots"]}rt-raw.pdf'))
    plot_emm_rt_bambi(df, model, results, path.join(base_path, f'{DATA["plots"]}rt-bambi-{'inter' if interaction else 'indep'}.pdf'))

def run_statsmodels(interaction: bool) -> None:
    print("Running LMM with Statsmodels...")
    df, model = calculate_model_stats(interaction, trial_data_path, relation_data_path)
    show_model_results_stats(model)
    plot_rt(df, path.join(base_path, f'{DATA["plots"]}rt-raw.pdf'))
    plot_emm_rt_statsmodels(df, model, path.join(base_path, f'{DATA["plots"]}rt-statsmodels-{'inter' if interaction else 'indep'}.pdf'))

def run_responses() -> None:
    print("Running correct response statistics...")
    responses = calculate_correct_responses(trial_data_path, relation_data_path)
    plot_response(responses, path.join(base_path, f'{DATA["plots"]}response-raw.pdf'))

def run_lrt_stats() -> None:
    print("Running Likelihood-ratio test based on Statsmodels...")
    lr_stat, df_diff, p_value = calculate_lrt_stats(trial_data_path, relation_data_path)
    show_lrt_results(lr_stat, df_diff, p_value)

def run_processing() -> None:
    print("Running results processing...")
    input_file_path = path.join(base_path, DATA["results raw"])
    output_file_path = path.join(base_path, DATA["results processed"])
    process_results(input_file_path, output_file_path)

def run_metadata() -> None:
    print("Running metadata extraction...")
    input_file_path = path.join(base_path, DATA["results raw"])
    output_file_path = path.join(base_path, DATA["metadata"])
    extract_metadata(input_file_path, output_file_path)
    analyse_metadata(output_file_path)

def get_user_choice(prompt: str, options: list[str]) -> str:
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def main() -> int:
    valid_modes: list[str] = ["analysis", "lrt", "responses", "processing", "metadata"]
    valid_libraries: list[str] = ["bambi", "statsmodels"]
    valid_interaction: list[str] = ["yes", "no"]
    valid_dvs: list[str] = ["rt", "response"]

    parser = argparse.ArgumentParser(description="Select mode, library, interaction, and dependent variables")
    parser.add_argument("mode", nargs="?", choices=valid_modes, help="Mode of operation")
    parser.add_argument("library", nargs="?", choices=valid_libraries, help="Statistics library to use")
    parser.add_argument("interact", nargs="?", choices=valid_interaction, help="Interaction of independent variables")
    parser.add_argument("dv", nargs="?", choices=valid_dvs, help="Dependent variables to use")
    args = parser.parse_args()

    # Prompt if missing
    mode: str = args.mode or get_user_choice("Select the mode of operation:", valid_modes)
    if mode == "processing":
        run_processing()
        return 0
    elif mode == "responses":
        run_responses()
        return 0
    elif mode == "lrt":
        run_lrt_stats()
        return 0
    elif mode == "metadata":
        run_metadata()
        return 0

    library: str = args.library or get_user_choice("Select the library to use:", valid_libraries)
    interaction: bool = True if (args.interact or get_user_choice("Select whether independent variables interact:", valid_interaction)) == 'yes' else False
    if library == "statsmodels":
        run_statsmodels(interaction)
        return 0

    dv: str = args.dv or get_user_choice("Select the dependent variable to use:", valid_dvs)
    if dv == "response":
        run_glmm_bambi(interaction)
    else:
        run_lmm_bambi(interaction)
    return 0

if __name__ == "__main__":
    main()
