from datasets.read_dataset import DatasetLoader, DataAugumentation
from PrefixSpan import PrefixSpan, PrefixSpanNonRecursive

import matplotlib.pyplot as plt
from time import perf_counter

minsup = 0.3

sequences = DatasetLoader.read_dataset("OnlineRetail_II_best")


pf = PrefixSpanNonRecursive()

def run_minsup_experiment(dataset, num_of_experiments, recursive=False, sequences_limit=None, max_seq_lenght=None, min_minsup=0):

    sequences = DatasetLoader.read_dataset(dataset)

    if sequences_limit:
        sequences = sequences[:sequences_limit]
    if max_seq_lenght:
        sequences = [seq[:max_seq_lenght] for seq in sequences]

    interval = 1/num_of_experiments

    times = []
    minsups = []
    patterns_found = []

    for minsup in [round(minsup * interval, 2) for minsup in range(1, num_of_experiments+1)]:
        if minsup<1/len(sequences) or minsup<min_minsup:
            continue

        pf = PrefixSpanNonRecursive() if not recursive else PrefixSpan()
        start = perf_counter()
        patterns = pf.mine(sequences,minsup)
        time = perf_counter() - start
        minsups.append(minsup)
        times.append(time)
        patterns_found.append(len(patterns))

    plot_minsup_experiment(minsups, times, patterns_found, "Minsup parameter exmperiment", dataset, size=len(sequences))

    return minsups, times, patterns_found

def run_size_experiment(dataset, max_size, num_of_experiments, minsup, recursive=False, max_seq_lenght=None):

    sequences = DatasetLoader.read_dataset(dataset)

    if max_seq_lenght:
        sequences = [seq[:max_seq_lenght] for seq in sequences]

    interval = max_size/num_of_experiments

    times = []
    sizes = []
    patterns_found = []

    for size in [round(i * interval, 2) for i in range(1, num_of_experiments+1)]:
        pf = PrefixSpanNonRecursive() if not recursive else PrefixSpan()
        size = int(size)
        print(size)
        start = perf_counter()
        patterns = pf.mine(sequences[:size],minsup)
        time = perf_counter() - start
        print(time)
        print(len(patterns))
        sizes.append(size)
        times.append(time)
        patterns_found.append(len(patterns))

    plot_dataset_size_experiment(sizes, times, patterns_found, "Dataset size exmperiment", dataset, minsup)

    return sizes, times, patterns_found

def run_augumented_dataset_experiment(aug_type, dataset, minsup, init_size=None, how_many_times_list=[1,2,3,4], recursive=False):
    sequences = DatasetLoader.read_dataset(dataset)

    if init_size:
        sequences = sequences[:init_size]

    augumenter = DataAugumentation.augumenter(aug_type)

    times = []
    patterns_found = []
    for how_many_times in how_many_times_list:
        pf = PrefixSpanNonRecursive() if not recursive else PrefixSpan()
        seq = augumenter(sequences, how_many_times)
        start = perf_counter()
        patterns = pf.mine(seq,minsup)
        time = perf_counter() - start
        times.append(time)
        patterns_found.append(len(patterns))

    plot_augumented_dataset_experiment(how_many_times_list, times, patterns_found, "Dataset augumentation exmperiment", dataset, aug_type)



def plot_minsup_experiment(minsups, times, patterns, title, dataset, size):
    plt.cla()
    plt.clf()
    plt.scatter(minsups, times)
    plt.title(f"{title} - dataset {dataset}, size {size}")
    plt.xlabel("Minimum Support")
    plt.ylabel("Time elapsed (s)")
    # plt.show()
    plt.savefig(f"images/{dataset}_minsup_to_time.png")

    plt.cla()
    plt.clf()
    plt.scatter(minsups, patterns)
    plt.title(f"{title} - dataset {dataset}, size {size}")
    plt.xlabel("Minimum Support")
    plt.ylabel("Number of found patterns")
    # plt.show()
    plt.savefig(f"images/{dataset}_minsup_to_patterns.png")

def plot_dataset_size_experiment(sizes, times, patterns, title, dataset, minsup):
    plt.cla()
    plt.clf()
    plt.scatter(sizes, times)
    plt.title(f"{title} - dataset {dataset}, minsup: {minsup}")
    plt.xlabel("Size of the database")
    plt.ylabel("Time elapsed (s)")
    plt.savefig(f"images/{dataset}_time_to_size.png")

    plt.cla()
    plt.clf()
    plt.scatter(sizes, patterns)
    plt.title(f"{title} - dataset {dataset}, minsup: {minsup}")
    plt.xlabel("Size of the database")
    plt.ylabel("Number of found patterns")
    plt.savefig(f"images/{dataset}_patterns_to_size.png")

def plot_augumented_dataset_experiment(how_many_times_list, times, patterns, title, dataset, aug_type):
    plt.cla()
    plt.clf()
    plt.scatter(how_many_times_list, times)
    plt.title(f"{title} - dataset {dataset}, multiplied: {aug_type}")
    plt.xlabel("Multiplier")
    plt.ylabel("Time elapsed (s)")
    # plt.show()
    plt.savefig(f"images/{dataset}_{aug_type}_multiplier_to_time.png")

    plt.cla()
    plt.clf()
    plt.scatter(how_many_times_list, patterns)
    plt.title(f"{title} - dataset {dataset}, multiplied: {aug_type}")
    plt.xlabel("Multiplier")
    plt.ylabel("Number of found patterns")
    # plt.show()
    plt.savefig(f"images/{dataset}_{aug_type}_multiplier_to_patterns.png")




# run_minsup_experiment("FIFA", 50, min_minsup=0.2, sequences_limit=1000)
# run_minsup_experiment("OnlineRetail_II_best", 50, min_minsup=0.2)
# run_minsup_experiment("e_shop", 50, min_minsup=0.4, sequences_limit=1000)
    
run_size_experiment("FIFA", 1000, num_of_experiments=50, minsup=0.25)
# run_size_experiment("e_shop", 1000, num_of_experiments=50, minsup=0.5)
# run_size_experiment("OnlineRetail_II_best", 1000, num_of_experiments=50, minsup=0.5)
    
# run_augumented_dataset_experiment("itemsets", "example", 0.5)
# run_augumented_dataset_experiment("sequences", "example", 0.5)
# run_augumented_dataset_experiment("itemsets", "OnlineRetail_II_best", 0.5)
# run_augumented_dataset_experiment("sequences", "OnlineRetail_II_best", 0.5)