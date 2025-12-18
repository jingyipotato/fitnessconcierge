"""Script for User Simulation for Agent Evaluation."""

import subprocess
from pathlib import Path
from dotenv import load_dotenv

from fitness_agent.infra.logging import get_logger

BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parents[1]
DATA_DIR = BASE_DIR / "data"
AGENT_DIR = PROJECT_ROOT / "src" / "fitness_agent"
EVAL_SET_NAME = "eval_set_with_scenarios"

load_dotenv()
logger = get_logger(__name__)


def run_cmd(cmd: list[str]):
    logger.info(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    try:
        # Create EvalSet
        run_cmd([
            "adk", "eval_set", "create",
            str(AGENT_DIR),
            EVAL_SET_NAME,
        ])
    except subprocess.CalledProcessError:
        logger.info(f"Eval set '{EVAL_SET_NAME}' already exists, continuing...")
    
    # Add eval cases
    run_cmd([
        "adk", "eval_set", "add_eval_case",
        str(AGENT_DIR),
        EVAL_SET_NAME,
        "--scenarios_file", str(DATA_DIR / "conversation_scenarios.json"),
        "--session_input_file", str(DATA_DIR / "session_input.json")
    ])
    
    # Run eval
    run_cmd([
        "adk", "eval",
        str(AGENT_DIR),
        "--config_file_path", str(DATA_DIR / "eval_config.json"),
        EVAL_SET_NAME,
        "--print_detailed_results"
    ])
   
 
if __name__ == "__main__":
    main()