from itertools import combinations
from datasets.read_dataset import DatasetLoader, DataAugumentation

class PrefixSpan:

    def __init__(self) -> None:
        self.found_patterns = []

    def count_item_support(self, projected_db, prefix):
        
        items_support = {}
        for seq in projected_db:
            unique_items = set()
            for itemset in seq:
                # print("itemset", itemset)
                if '_' in itemset:
                    prefix_last_itemset = prefix[-1]
                    # print(prefix_last_itemset)
                    subsets = []
                    for i in range(1, len(itemset[1:]) + 1):
                        for combo in combinations(itemset[1:], i):
                            subsets.append(list(combo))
                    for subset in subsets:
                        frequent_itemlist = [*prefix_last_itemset] + subset
                        unique_items.add(tuple(frequent_itemlist)) # this is not item, it is an itemlist
 
                else:
                    for item in itemset:
                        unique_items.add(item)
                        

            for item in unique_items:
                if item not in items_support:
                    items_support[item] = 1
                else:
                    items_support[item] += 1
                        
        return items_support

    def build_new_projected_db(self, projected_db, current_item, new_prefix):
        new_projected_db = []

        for sequence in projected_db:
            new_sequence = []

            flag = int(type(current_item) is tuple) # if it is a tuple then we search for continuation of itemset
            item_to_check = current_item[-1] if flag else current_item

            for i, itemset in enumerate(sequence):
                if itemset[0] == '_' and len(new_prefix[-1])==1: # we are checking itemsets starting with '_' only when prefixs last itemset has more than one items
                    continue
                
                for j, item in enumerate(itemset[flag:]): # if continuation of itemset then skip first because of '_'
                    if item==item_to_check:
                        
                        first_itemset = ['_'] + itemset[j+flag+1:]
                        # first_itemset = ['_'] + itemset[flag:j+flag] + itemset[j+flag+1:]
                    
                        if first_itemset!=['_']:
                            new_sequence = [first_itemset] + sequence[i+1:]
                        else:
                            new_sequence = sequence[i+1:]

                        break
                if new_sequence:
                    new_projected_db.append(new_sequence)
                    break

        return new_projected_db

    def prefix_span(self, prefix, projected_db, min_support):

        counts = self.count_item_support(projected_db, prefix)
        frequent_items = {item:count for item, count in counts.items() if count >= min_support}

        for item in frequent_items:
            support = frequent_items[item]
            if type(item) is tuple:
                
                if prefix:
                    new_prefix = prefix[:-1] + [list(item)]
                else:
                    new_prefix = [prefix[:-1] + list(item)]
                
            else:
                new_prefix = prefix + [[item]]

            if not prefix==new_prefix:
                self.found_patterns.append((support, new_prefix))
            new_projected_db = self.build_new_projected_db(projected_db, item, new_prefix)
            self.prefix_span(new_prefix, new_projected_db, min_support)


    def mine(self, sequences, min_support):
        if min_support<0 or min_support>1:
            raise Exception("Minimum support must be between [0, 1]")
        min_support = len(sequences)*min_support
        min_support = max(1, min_support)
        self.prefix_span([], sequences, min_support)
        
        return self.found_patterns
    
class PrefixSpanNonRecursive(PrefixSpan):

    def prefix_span(self, initial_prefix, initial_projected_db, min_support):
        stack = [(initial_prefix, initial_projected_db)]

        while stack:

            prefix, projected_db = stack.pop()
            
            counts = self.count_item_support(projected_db, prefix)
            frequent_items = {item:count for item, count in counts.items() if count >= min_support}
            for item in frequent_items:
                support = frequent_items[item]
                if type(item) is tuple:

                    if prefix:
                        new_prefix = prefix[:-1] + [list(item)]
                    else:
                        new_prefix = [prefix[:-1] + list(item)]
                else:
                    new_prefix = prefix + [[item]]

                if prefix != new_prefix:
                    self.found_patterns.append((support, new_prefix))

                new_projected_db = self.build_new_projected_db(projected_db, item, new_prefix)
                stack.append((new_prefix, new_projected_db))

if __name__ == "__main__":

    # sequences = [[['a','b'], ['c'], ['a']],
    #             [['a','b'], ['b'], ['c']],
    #             [['b'], ['c'], ['d']],
    #             [['b'], ['a','b'], ['c']]]
    
    with open('datasets/example.txt') as f:
        sequences = [[[int(item) for item in itemlist.split()] for itemlist in line.split(' -1 ')][:-1] for line in f]
    
    # sequences = DatasetLoader.read_dataset("FIFA")
    # sequences = DatasetLoader.read_dataset("OnlineRetail_II_best")
    min_support=0.5

    ps = PrefixSpanNonRecursive()
    frequent_patterns = ps.mine(sequences, min_support)
    [print(pattern[0], '|',  pattern[1]) for pattern in frequent_patterns]
    print(f"Found {len(frequent_patterns)} frequent patterns")
