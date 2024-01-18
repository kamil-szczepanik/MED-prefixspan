class DatasetLoader:
    def read_dataset(name, max_sequence_lenght=None, sequences_limit=None):

        data_type = int if not name=="example2" else str

        with open(f'datasets/{name}.txt') as f:
            sequences = [[[data_type(item) for item in itemlist.split()] for itemlist in line.split(' -1 ')][:-1] for line in f]

        if sequences_limit:
            sequences = sequences[:sequences_limit]

        if max_sequence_lenght:
            sequences = [seq[:max_sequence_lenght] for seq in sequences]
        return sequences


class DataAugumentation:
    def copy_sequences(sequences, how_many_times):
        new_sequences = sequences*how_many_times
        return new_sequences

    def copy_itemsets(sequences, how_many_times):
        new_sequences = []
        for sequence in sequences:
            new_sequences.append(sequence*how_many_times)
        return new_sequences
    
    def augumenter(type):
        types = {
            "sequences": DataAugumentation.copy_sequences,
            "itemsets": DataAugumentation.copy_itemsets,
        }
        return types[type]


    

