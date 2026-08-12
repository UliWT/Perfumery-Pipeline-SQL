"""Shared configuration for the PostgreSQL ELT pipeline."""

from __future__ import annotations

import logging
import os
import sys


def setup_logging() -> logging.Logger:
    log_dir = os.getenv("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "pipeline.log")),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("perfumeria_elt")


logger = setup_logging()
