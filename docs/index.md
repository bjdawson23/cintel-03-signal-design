# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
This project uses Disney California Adventure wait-time observations from [data/disney_wait_times.csv](../data/disney_wait_times.csv).

Each row includes:

- `Land`
- `Ride`
- `Wait Time` (minutes)
- `Local Time`
- `Day of Week`

### Signals
The Disney signal pipeline creates the following fields:

- `wait_minutes`: cleaned wait time (non-negative integer minutes)
- `is_long_wait`: `True` when wait is 45 minutes or more
- `land_avg_wait`: mean wait for all rides in the same land at the same timestamp
- `wait_bucket`: categorical wait class (`low` < 15, `medium` 15-29, `high` 30-59, `extreme` >= 60)

### Visualizations
The plotting module creates these charts from the signals artifact:

- [artifacts/images/avg_wait_by_day.png](../artifacts/images/avg_wait_by_day.png)
- [artifacts/images/top_rides_avg_wait.png](../artifacts/images/top_rides_avg_wait.png)
- [artifacts/images/avg_wait_by_hour.png](../artifacts/images/avg_wait_by_hour.png)
- [artifacts/images/ride_hour_heatmap.png](../artifacts/images/ride_hour_heatmap.png)

Run the plotting module with:

- `uv run python -m cintel.plot_disney_waits`

### Experiments
Signals:

- threshold alerts (`is_long_wait`)
- local context (`land_avg_wait`)
- readable operational categories (`wait_bucket`)
- visual outputs by day, ride, hour, and ride-hour heatmap

### Results
The pipeline now outputs at [artifacts/signals_disney_wait.csv](../artifacts/signals_disney_wait.csv) with both raw and derived signal columns.

This will help:

- identify rides with severe current waits
- compare each ride with its land-level average wait
- summarize status quickly with bucketed labels
- identify peak congestion windows by attraction using the heatmap

### Interpretation
These signals improve operational awareness by separating:

- immediate guest pain (`is_long_wait`, `wait_bucket`)
- local crowd context (`land_avg_wait`)

Together, they support better staffing, communication, and crowd-flow decisions across the park.
