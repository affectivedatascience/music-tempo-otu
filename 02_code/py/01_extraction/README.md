# Tempo Study Data Processing

## Easiest setup

Install `uv` [https://astral.sh/uv/install/](https://astral.sh/uv/install/).

Then install dependencies with
```bash
uv sync
```

## Usage

```bash
python main.py -apath <path_to_acq_files> -rpath <path_to_response_files> [-o <output_directory>]
```

### Arguments

- `-apath`, `--acq_inpath`: (Required) The path to the directory containing the `.acq` data files.
- `-rpath`, `--response_inpath`: (Required) The path to the directory containing the participant response `.csv` files.
- `-opath`, `--outpath`: (Optional) The directory where the output `.csv` files will be saved. If this argument is omitted, the output will be saved to a directory named `out/` by default.**

### Example

```bash
python main.py -apath ./data -rpath ./tempo-study-responses -opath ./out
```

This command will:
1. Read the `.acq` files from the `data/` directory.
2. Read the corresponding participant response `.csv` files from the `tempo-study-responses/` directory to determine the order of experimental conditions.
3. Process the data and extract trials for each condition.
4. Save the processed data as `.csv` files in the `out/` directory, organized by participant ID.
