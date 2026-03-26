"""Create summary charts for Disney wait-time signals.
Author: Branton Dawson
Date: 2026-03-26

Paths (relative to repo root)

    INPUT FILE: artifacts/disney_wait_times.csv
    OUTPUT FILE: artifacts/images/xxxxx.png

Terminal command to run this file from the root project folder

    uv run python -m cintel.plot_disney_waits
"""

import logging
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

LOG: logging.Logger = get_logger("P3", level="DEBUG")

ROOT_DIR: Final[Path] = Path.cwd()
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"
IMAGES_DIR: Final[Path] = ARTIFACTS_DIR / "images"
SIGNALS_FILE: Final[Path] = ARTIFACTS_DIR / "signals_disney_wait.csv"


def _load_signals() -> pl.DataFrame:
    """Load signal data and add hour_of_day for time-based charts."""
    df = pl.read_csv(SIGNALS_FILE)
    return df.with_columns(
        pl.col("Local Time").str.slice(11, 2).cast(pl.Int64).alias("hour_of_day")
    )


def _plot_avg_wait_by_day(df: pl.DataFrame) -> None:
    """Plot average wait by day of week."""
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    by_day = (
        df.group_by("Day of Week")
        .agg(pl.mean("wait_minutes").round(2).alias("avg_wait_minutes"))
        .with_columns(
            pl.col("Day of Week").replace(day_order, list(range(7))).alias("day_sort")
        )
        .sort("day_sort")
    )

    x = by_day.get_column("Day of Week").to_list()
    y = by_day.get_column("avg_wait_minutes").to_list()

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker="o", linewidth=2)
    plt.title("Average Wait by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Average Wait (minutes)")
    plt.grid(alpha=0.3)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "avg_wait_by_day.png", dpi=150)
    plt.close()


def _plot_avg_wait_by_ride(df: pl.DataFrame, top_n: int = 15) -> None:
    """Plot top rides by average wait."""
    by_ride = (
        df.group_by("Ride")
        .agg(pl.mean("wait_minutes").round(2).alias("avg_wait_minutes"))
        .sort("avg_wait_minutes", descending=True)
        .head(top_n)
    )

    rides = by_ride.get_column("Ride").to_list()
    waits = by_ride.get_column("avg_wait_minutes").to_list()

    plt.figure(figsize=(12, 7))
    plt.barh(rides, waits)
    plt.gca().invert_yaxis()
    plt.title(f"Top {top_n} Rides by Average Wait")
    plt.xlabel("Average Wait (minutes)")
    plt.ylabel("Ride")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "top_rides_avg_wait.png", dpi=150)
    plt.close()


def _plot_avg_wait_by_hour(df: pl.DataFrame) -> None:
    """Plot average wait by hour of day."""
    by_hour = (
        df.group_by("hour_of_day")
        .agg(pl.mean("wait_minutes").round(2).alias("avg_wait_minutes"))
        .sort("hour_of_day")
    )

    hours = by_hour.get_column("hour_of_day").to_list()
    waits = by_hour.get_column("avg_wait_minutes").to_list()

    plt.figure(figsize=(10, 5))
    plt.plot(hours, waits, marker="o", linewidth=2)
    plt.title("Average Wait by Hour of Day")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Wait (minutes)")
    plt.xticks(range(0, 24, 1))
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "avg_wait_by_hour.png", dpi=150)
    plt.close()


def _plot_ride_hour_heatmap(df: pl.DataFrame, top_n: int = 20) -> None:
    """Plot a ride-by-hour heatmap to reveal peak congestion windows."""
    top_rides_df = (
        df.group_by("Ride")
        .agg(pl.mean("wait_minutes").alias("avg_wait_minutes"))
        .sort("avg_wait_minutes", descending=True)
        .head(top_n)
    )

    top_rides = top_rides_df.get_column("Ride").to_list()

    heatmap_df = (
        df.filter(pl.col("Ride").is_in(top_rides))
        .group_by(["Ride", "hour_of_day"])
        .agg(pl.mean("wait_minutes").round(2).alias("avg_wait_minutes"))
        .pivot(index="Ride", on="hour_of_day", values="avg_wait_minutes")
    )

    hour_columns = sorted(
        [col for col in heatmap_df.columns if col != "Ride"],
        key=lambda x: int(x),
    )

    heatmap_df = heatmap_df.select(["Ride", *hour_columns])
    rides = heatmap_df.get_column("Ride").to_list()
    matrix = heatmap_df.select(hour_columns).fill_null(0.0).to_numpy()

    plt.figure(figsize=(14, 8))
    image = plt.imshow(matrix, aspect="auto", cmap="YlOrRd")
    plt.colorbar(image, label="Average Wait (minutes)")
    plt.title(f"Ride-by-Hour Wait Heatmap (Top {top_n} Rides)")
    plt.xlabel("Hour of Day")
    plt.ylabel("Ride")
    plt.xticks(
        range(len(hour_columns)), [int(hour) for hour in hour_columns], rotation=45
    )
    plt.yticks(range(len(rides)), rides)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "ride_hour_heatmap.png", dpi=150)
    plt.close()


def main() -> None:
    """Generate Disney wait-time charts from the signals artifact."""
    log_header(LOG, "CINTEL")

    log_path(LOG, "SIGNALS_FILE", SIGNALS_FILE)
    log_path(LOG, "IMAGES_DIR", IMAGES_DIR)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    df = _load_signals()
    _plot_avg_wait_by_day(df)
    _plot_avg_wait_by_ride(df, top_n=15)
    _plot_avg_wait_by_hour(df)
    _plot_ride_hour_heatmap(df, top_n=20)

    LOG.info(
        "Saved charts: avg_wait_by_day.png, top_rides_avg_wait.png, avg_wait_by_hour.png, ride_hour_heatmap.png"
    )


if __name__ == "__main__":
    main()
