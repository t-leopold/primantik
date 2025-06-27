import argparse
from os import path
from custom_types import *
from evaluation.process import process_results
from evaluation.analyse import show_model_results_stats, calculate_model_stats, show_model_results_bambi, calculate_model_bambi

DATA: dict[DataFiles, str] = {
    "conditions": "./conditions-experiment.csv",
    "results raw": "./results/results-raw.txt",
    "results processed": "./results/results-processed.txt"
}
SCRIPTS: dict[Scripts, str] = {
    "process": "./evaluation/process.py",
    "analyse": "./evaluation/analyse.py"
}
base_path = path.dirname(path.abspath(__file__))
trial_data_path = path.join(base_path, DATA["results processed"])
relation_data_path = path.join(base_path, DATA["conditions"])

def run_glmm_bambi(interaction: bool):
    print("Running GLMM with Bambi...")
    show_model_results_bambi(calculate_model_bambi(interaction, 'response', trial_data_path, relation_data_path))

def run_lmm_bambi(interaction: bool):
    print("Running LMM with Bambi...")
    show_model_results_bambi(calculate_model_bambi(interaction, 'rt', trial_data_path, relation_data_path))

def run_statsmodels(interaction: bool):
    print("Running LMM with Statsmodels...")
    show_model_results_stats(calculate_model_stats(interaction, trial_data_path, relation_data_path))

def run_processing():
    print("Running results processing...")
    input_file_path = path.join(base_path, DATA["results raw"])
    output_file_path = path.join(base_path, DATA["results processed"])
    process_results(input_file_path, output_file_path)

def get_user_choice(prompt, options):
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

def main():
    valid_modes = ["analysis", "processing"]
    valid_libraries = ["bambi", "statsmodels"]
    valid_interaction = ["yes", "no"]
    valid_dvs = ["rt", "response"]

    parser = argparse.ArgumentParser(description="Select mode, library, and dependent variables")
    parser.add_argument("mode", nargs="?", choices=valid_modes, help="Mode of operation (analysis or processing)")
    parser.add_argument("library", nargs="?", choices=valid_libraries, help="Library to use (bambi or statsmodels)")
    parser.add_argument("interact", nargs="?", choices=valid_interaction, help="Interaction of independent variables (yes or no)")
    parser.add_argument("dv", nargs="?", choices=valid_dvs, help="Dependent variables to use (rt or response)")
    args = parser.parse_args()

    # Prompt if missing
    mode = args.mode or get_user_choice("Select the mode of operation:", valid_modes)
    if mode == "processing":
        run_processing()
        return

    library = args.library or get_user_choice("Select the library to use:", valid_libraries)
    interaction = True if (args.interact or get_user_choice("Select whether independent variables interact:", valid_interaction)) == 'yes' else False
    if library == "statsmodels":
        run_statsmodels(interaction)
        return

    dv = args.dv or get_user_choice("Select the dependent variable to use:", valid_dvs)
    if dv == "response":
        run_glmm_bambi(interaction)
    else:
        run_lmm_bambi(interaction)

if __name__ == "__main__":
    main()
