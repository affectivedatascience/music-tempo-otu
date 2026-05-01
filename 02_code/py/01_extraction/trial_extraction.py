# Python standard libraries
import os
from pathlib import Path

# External libraries
import numpy as np
import pandas as pd
from tqdm import tqdm


def get_trial_matrix(trial_column: np.ndarray) -> np.ndarray:
    """Return a two-column trial matrix where each row is a pair that represents
    the beginning and end indices of the corresponding trial."""
    # All indices where a trial is occurring
    trial_indices = np.argwhere(trial_column > 2.5).flatten()

    # Do a basic search for value jumps in the trial indices. This separates
    # the indices for each trial from the others.
    value = trial_indices[0]
    result = [trial_indices[0]]
    for i in range(1, len(trial_indices)):
        if trial_indices[i] == value + 1:
            value += 1
        else:
            result.append(trial_indices[i - 1])
            result.append(trial_indices[i])
            value = trial_indices[i]
    result.append(trial_indices[-1])
    trial_mat = np.array(result).reshape(len(result) // 2, 2)
    baseline1 = np.array((trial_mat[0, 1], trial_mat[1, 0])).reshape((1, 2))
    baseline2 = np.array((trial_mat[1, 1], trial_mat[2, 0])).reshape((1, 2))
    trial_mat = np.concatenate(
        (
            trial_mat[0:1, :],
            baseline1,
            trial_mat[1, :].reshape((1, 2)),
            baseline2,
            trial_mat[2:, :],
        ),
        axis=0,
    )

    return trial_mat


def save_trial_data(
    outpath: Path,
    participant_id: str,
    ordered_conditions: list[str],
    mat: np.ndarray,
    sampling_rate: float,
) -> None:
    """Extracts ands and saves the each trial from the complete experiment for a
    single participant."""

    T = 1.0 / sampling_rate

    trial_column = mat[:, -1]
    mat_without_trial_col = mat[:, 0:-1]
    trial_matrix = get_trial_matrix(trial_column)
    # Accounts for 30 seconds before the final trial
    trial_matrix[-1, 0] -= int(30 * sampling_rate)

    savepath: Path = outpath / participant_id
    savepath.mkdir(parents=True, exist_ok=True)

    for i in tqdm(
        range(trial_matrix.shape[0]),
        desc=f"Writing participant {participant_id}",
    ):
        start_index = trial_matrix[i, 0]
        end_index = trial_matrix[i, 1]
        trial = mat_without_trial_col[start_index : end_index + 1, :]

        time_col = np.arange(trial.shape[0]) * T

        df = pd.DataFrame(
            np.concatenate([time_col[..., np.newaxis], trial], axis=1)
        )

        clip = os.path.splitext(ordered_conditions[i])[0]
        filename = str(participant_id) + "-" + str(clip) + ".csv"

        df.to_csv(
            savepath / filename,
            index=False,
            header=[
                "Time",
                "Zygomaticus_EMG",
                "Corrugator_EMG",
                "ECG",
                "Respiration",
            ],
        )
