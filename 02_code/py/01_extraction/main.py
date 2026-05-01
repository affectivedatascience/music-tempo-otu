#!usr/bin/env python3

# Python standard libraries
from argparse import ArgumentParser
from pathlib import Path

# External libraries
import bioread


# Local
from util import convert_acq_to_ndarray, condition_order_from_responses
from trial_extraction import save_trial_data


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-apath",
        "--acq_inpath",
        type=Path,
        required=True,
        help="The directory containing the ACQ files",
    )
    parser.add_argument(
        "-rpath",
        "--response_inpath",
        type=Path,
        required=True,
        help="The directory containing the participant responses",
    )
    parser.add_argument(
        "-opath",
        "--outpath",
        type=Path,
        default="out",
        help="The directory where the output csv will be saved",
    )
    args = parser.parse_args()

    for acq_filename in args.acq_inpath.glob("*.acq"):
        data = bioread.read(acq_filename)
        participant_id = acq_filename.stem
        sampling_rate = data.samples_per_second
        mat = convert_acq_to_ndarray(data)

        ordered_conditions = condition_order_from_responses(
            args.response_inpath / f"{participant_id}.csv"
        )

        save_trial_data(
            args.outpath,
            participant_id,
            ordered_conditions,
            mat,
            sampling_rate,
        )


if __name__ == "__main__":
    main()
