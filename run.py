import argparse
import os

from datasets.read_dataset import DatasetLoader, DataAugumentation
from PrefixSpan import PrefixSpan, PrefixSpanNonRecursive


datasets = [filename[:-4] for filename in os.listdir(".\datasets") if filename[-4:]==".txt"]

parser = argparse.ArgumentParser(prog="PrefixSpan")
parser.add_argument(
    "dataset",
    type=str,
    choices=datasets,
    help="Choose dataset",
)
parser.add_argument("minsup", type=float, help="Parameter: minimum support threshold")
parser.add_argument(
    "-r",
    "--recursive",
    type=bool,
    default=False,
    help="Use recursive PrefixSpan"
)
parser.add_argument(
    "--sequences_limit",
    type=int,
    default=None,
    help="Limit of sequences to process"
)
parser.add_argument(
    "--max_seq_lenght",
    type=int,
    default=None,
    help="Max sequence lenght (max itemlists)"
)


def run(dataset, minsup, recursive=False, sequences_limit=None, max_seq_lenght=None):
    sequences = DatasetLoader.read_dataset(dataset)
    if not recursive:
        pf = PrefixSpanNonRecursive()
    else:
        pf = PrefixSpan()

    if sequences_limit:
        sequences = sequences[:sequences_limit]
    if max_seq_lenght:
        sequences = [seq[:max_seq_lenght] for seq in sequences]

    patterns = pf.mine(sequences,minsup)
    [print(pattern[0], '|',  pattern[1]) for pattern in patterns]
    print(f"---\nFound patterns: {len(patterns)}")

if __name__ == "__main__":
    args = parser.parse_args()
    run(args.dataset, args.minsup, args.recursive, args.sequences_limit, args.max_seq_lenght)