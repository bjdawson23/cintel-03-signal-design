"""
signal_design_disney_wait.py - Disney wait-time signal pipeline.

Author: Branton Dawson
Date: 2026-03-26

Paths (relative to repo root)

    INPUT FILE: data/disney_wait_times.csv
    OUTPUT FILE: artifacts/signals_disney_wait.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.signal_design_disney_wait
"""

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

LOG: logging.Logger = get_logger("P3", level="DEBUG")

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "disney_wait_times.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "signals_disney_wait.csv"


def main() -> None:
    """Run the Disney wait-time signal pipeline."""
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    df: pl.DataFrame = pl.read_csv(DATA_FILE)
    LOG.info(f"Loaded {df.height} Disney wait-time records")
    LOG.info("Designing signals from the raw metrics...")

    df_prepped: pl.DataFrame = df.with_columns(
        [
            pl.col("Local Time").alias("local_time"),
            pl.col("Wait Time")
            .cast(pl.Int64)
            .clip(lower_bound=0)
            .alias("wait_minutes"),
        ]
    )

    long_wait_flag_signal: pl.Expr = (pl.col("wait_minutes") >= 45).alias(
        "is_long_wait"
    )

    land_avg_wait_df: pl.DataFrame = df_prepped.group_by(["Land", "local_time"]).agg(
        pl.mean("wait_minutes").round(2).alias("land_avg_wait")
    )

    df_with_land_avg: pl.DataFrame = df_prepped.join(
        land_avg_wait_df,
        on=["Land", "local_time"],
        how="left",
    )

    df_sorted: pl.DataFrame = df_with_land_avg.sort(["Ride", "local_time"])

    df_with_signals: pl.DataFrame = df_sorted.with_columns(
        [
            long_wait_flag_signal,
        ]
    ).with_columns(
        [
            pl.when(pl.col("wait_minutes") < 15)
            .then(pl.lit("low"))
            .when(pl.col("wait_minutes") < 30)
            .then(pl.lit("medium"))
            .when(pl.col("wait_minutes") < 60)
            .then(pl.lit("high"))
            .otherwise(pl.lit("extreme"))
            .alias("wait_bucket"),
        ]
    )

    LOG.info("Created signal columns: is_long_wait, land_avg_wait, wait_bucket")

    signals_df = df_with_signals.select(
        [
            "Land",
            "Ride",
            "Day of Week",
            "Local Time",
            "wait_minutes",
            "is_long_wait",
            "wait_bucket",
            "land_avg_wait",
        ]
    )

    LOG.info(f"Enhanced signals table has {signals_df.height} rows")
    signals_df.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote signals file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


if __name__ == "__main__":
    main()
