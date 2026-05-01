# Python standard libraries
from pathlib import Path

# External libraries
import bioread
import pandas as pd
import numpy as np

def convert_acq_to_ndarray(data: bioread.Datafile) -> np.ndarray:
    mat = np.empty([len(data.channels[0].data), len(data.channels)])
    for i in range(len(data.channels)):
        mat[:, i] = data.channels[i].data

    return mat

def condition_order_from_responses(responses_path: Path) -> list[str]:
    """Return a list of the conditions in experimental presentation order."""
    response_df = pd.read_csv(responses_path)

    # The presentation order of the 'Slow' condition; can be 2 or 3
    slow_condition_order = response_df.loc[
        response_df.Condition == "Slow"
    ].Order.item()
    if slow_condition_order == 2:
        return [
            "Practice",
            "Baseline1",
            "Slow",  # slow was presented first in this case
            "Baseline2",
            "Fast",
            "Breathe",
        ]

    return [
        "Practice",
        "Baseline1",
        "Fast",  # fast was presented first in this case
        "Baseline2",
        "Slow",
        "Breathe",
    ]
