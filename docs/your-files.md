# Your Files

Projects include instructor example files that end with `_case`.
Keep these as working examples.

You will generally copy the instructor file, rename it with your alias,
and run your version in addition to the instructor version.

## Choose Your Name (example: `stellar_analytics`)

You may use your real name or any professional alias.
You are **never required to use your real name**.

Naming rules:

- all lowercase
- no spaces (use underscores as needed)

## 1. Python Files

Copy the instructor Python file and rename the copy using your alias.

```text
src/cintel/anomaly_detector_case.py
src/cintel/anomaly_detector_stellar_analytics.py
```

## 2. Python File Execution Command

In your `README.md`, add a line with the execution command just after the instructor command.
Use this command to run your file.

```shell
uv run python -m cintel.anomaly_detector_case
uv run python -m cintel.anomaly_detector_stellar_analytics
```

## 3. Data Files

Copy the instructor data file and rename the copy using your alias.

```text
data/static_data_case.csv
data/static_data_stellar_analytics.csv
```

You may modify the copied dataset as needed for your project,
or choose your own dataset if appropriate.

## My Modifications

I added a success rate signal.  It complements the error_rate signal.
Interpretation:  Closer to 1.0 signals a healthier connection.  Closer to 0.0 is not healty.

I changed the errors from 4 to 140 on row 6 of the data to make sure to flag that row.  
I also added a success rate signal to flag any success rate under .98 as a connection to check.
Four of the rows in the data came back with a "true" on success rate under .98.
