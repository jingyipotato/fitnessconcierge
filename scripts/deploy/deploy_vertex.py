"""Script for deployment to Vertex AI."""

import os
import random
import subprocess
from pathlib import Path

from fitness_agent.infra.logging import get_logger

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]
DEPLOY_DIR = PROJECT_ROOT / "deploy_agent"

logger = get_logger(__name__)

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

def main():
    regions_list = [
        "europe-west1",
        "europe-west4",
        "us-east4",
        "us-west1",
        ]

    deployed_region = random.choice(regions_list)
    logger.info(f"Selected deployment region: {deployed_region}")

    cmd = [
        "adk", "deploy", "agent_engine",
        "--project", PROJECT_ID,
        "--region", deployed_region,
        str(DEPLOY_DIR),
        "--agent_engine_config_file",
        str(DEPLOY_DIR / ".agent_engine_config.json" ),
    ]
    logger.info(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
