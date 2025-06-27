import argparse
import subprocess
import os
import sys

SCRIPTS = {
    "process": "./results/process_results.py",
    "analyse": "./analysis/analyse_results.py"
}

def run_script(script_key: str, script_args: list[str]):
    if script_key not in SCRIPTS:
        print(f"Error: Unknown script '{script_key}'. Available options: {', '.join(SCRIPTS.keys())}")
        return

    base_path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_path, SCRIPTS[script_key])

    print(f"Running {script_key} ({script_path}) with arguments: {script_args}")
    result = subprocess.run([sys.executable, script_path] + script_args, capture_output=True, text=True)

    print("Output:\n", result.stdout)
    if result.stderr:
        print("Errors:\n", result.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run processing or analysis script.")
    parser.add_argument("script", choices=SCRIPTS.keys(), help="Script to run: 'process' or 'analyse'")
    parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments to pass to the selected script")

    args = parser.parse_args()

    run_script(args.script, args.script_args)
