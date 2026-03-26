# cintel-03-signal-design

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](#)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project for continuous intelligence.

Continuous intelligence systems monitor data streams, detect change, and respond in real time.
This course builds those capabilities through working projects.

In the age of generative AI, durable skills are grounded in real work:
setting up a professional environment,
reading and running code,
understanding the logic,
and pushing work to a shared repository.
Each project follows the structure of professional Python projects.
We learn by doing.

## This Project

This project introduces **signal design**.

The goal is to copy this repository,
set up your environment,
run the Disney wait-time analysis,
and explore how useful signals can be derived from ride wait data.

You will run the example pipeline, read the code,
and make small modifications to understand how
signals are created from operational measurements.

## Data

The Disney pipeline reads wait-time data from: `data/disney_wait_times.csv`.

Each row represents an attraction observation with fields such as:

- `Land`
- `Ride`
- `Wait Time`
- `Local Time`
- `Day of Week`

The pipeline derives operational signals such as **long-wait flags**,
**land average wait**, and a **wait bucket**.

## My Modifications

I built a Disney wait-time signal pipeline and visualization workflow.

Current derived signals added to `artifacts/signals_disney_wait.csv`:

- `wait_minutes`
- `is_long_wait`
- `land_avg_wait`
- `wait_bucket` (`low`, `medium`, `high`, `extreme`)

I also added chart generation with:

- `uv run python -m cintel.plot_disney_waits`

This produces:

- `artifacts/images/avg_wait_by_day.png`
- `artifacts/images/top_rides_avg_wait.png`
- `artifacts/images/avg_wait_by_hour.png`
- `artifacts/images/ride_hour_heatmap.png`

Together, these outputs make it easier to identify peak congestion windows,
compare attraction pressure within each land, and summarize guest-facing wait conditions.

## Working Files

You'll work with just these areas:

- **data/** - it starts with the data
- **docs/** - project narrative and interpretation
- **src/cintel/** - analysis and plotting modules
- **pyproject.toml** - update authorship & links
- **zensical.toml** - update authorship & links

## Instructions

Follow the [step-by-step workflow guide](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/) to complete:

1. Phase 1. **Start & Run**
2. Phase 2. **Change Authorship**
3. Phase 3. **Read & Understand**
4. Phase 4. **Modify**
5. Phase 5. **Apply**

## Challenges

Challenges are expected.
Sometimes instructions may not quite match your operating system.
When issues occur, share screenshots, error messages, and details about what you tried.
Working through issues is part of implementing professional projects.

## Success

After completing Phase 1. **Start & Run**, you'll have your own GitHub project
running on your machine. Running the Disney signal pipeline will print:

```shell
========================
Pipeline executed successfully!
========================
```

And a new file named `project.log` will appear in the project folder.

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
git clone https://github.com/bjdawson23/cintel-03-signal-design

cd cintel-03-signal-design
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
git add -A
uvx pre-commit run --all-files

uv run python -m cintel.signal_design_case
uv run python -m cintel.signal_design_dawson
uv run python -m cintel.signal_design_disney_wait
uv run python -m cintel.plot_disney_waits

uv run ruff format .
uv run ruff check . --fix
uv run zensical build

git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.
