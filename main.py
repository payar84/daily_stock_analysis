#!/usr/bin/env python3
"""Daily Stock Analysis - Main Entry Point

This module serves as the primary entry point for the daily stock analysis tool.
It orchestrates data fetching, analysis, and report generation.
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"logs/analysis_{datetime.now().strftime('%Y%m%d')}.log", mode='a')
    ]
)
logger = logging.getLogger(__name__)


def get_config() -> dict:
    """Load configuration from environment variables."""
    return {
        "api_key": os.getenv("STOCK_API_KEY", ""),
        "market": os.getenv("MARKET", "US"),  # changed default from CN to US for my use case
        "symbols": os.getenv("WATCH_SYMBOLS", "").split(","),
        "output_dir": os.getenv("OUTPUT_DIR", "output"),
        "notify_email": os.getenv("NOTIFY_EMAIL", ""),
        "analysis_period": int(os.getenv("ANALYSIS_PERIOD_DAYS", "90")),  # extended default from 30 to 90 days
    }


def ensure_directories(config: dict) -> None:
    """Ensure required directories exist."""
    dirs = ["logs", config["output_dir"], "data/cache"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        logger.debug(f"Directory ensured: {d}")


def run_analysis(config: dict) -> bool:
    """Run the main stock analysis pipeline.

    Args:
        config: Configuration dictionary.

    Returns:
        True if analysis completed successfully, False otherwise.
    """
    logger.info("Starting daily stock analysis")
    logger.info(f"Market: {config['market']} | Period: {config['analysis_period']} days")

    symbols = [s.strip() for s in config["symbols"] if s.strip()]
    if not symbols:
        logger.warning("No symbols configured. Set WATCH_SYMBOLS in .env")
        return False

    logger.info(f"Analyzing {len(symbols)} symbol(s): {', '.join(symbols)}")

    # Placeholder for pipeline steps — modules to be implemented
    # from fetcher import StockDataFetcher
    # from analyzer import StockAnalyzer
    # from reporter import ReportGenerator

    logger.info("Analysis pipeline completed successfully")
    return True


def main() -> int:
    """Main function.

    Returns:
        Exit code (0 = success, 1 = failure).
    """
    config = get_config()
    ensure_directories(config)

    logger.info(f"Daily Stock Analysis started at {datetime.now().isoformat()}")

    try:
        success = run_analysis(config)
        if success:
            logger.info("All tasks completed.")
            return 0
        else:
            logger.error("Analysis did not complete successfully.")
            return 1
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        return 0
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
