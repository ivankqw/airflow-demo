"""Word count example using MapReduce."""


from multiprocessing import Pool, current_process
import itertools
from typing import Tuple, List

# Map function
def map_function(data: List[str]) -> List[Tuple[str, int, str]]:
    output = []
    # just to show which process we are in
    process_name = current_process().name
    for word in data:
        output.append((word, 1, process_name))
    return output

# Shuffle and sort
def shuffle_and_sort(mapped_data: List[Tuple[str, int, str]]) -> List[Tuple[str, List[Tuple[str, int, str]]]]:

    # shuffle is not parallelizable
    shuffled = itertools.groupby(sorted(mapped_data), lambda x: x[0])
    # [('Cat', <itertools._grouper object at 0x1015255e0>), ('Dog', <itertools._grouper object at 0x1015256a0>), ('Duck', <itertools._grouper object at 0x101525640>), ('Mouse', <itertools._grouper object at 0x101525670>)]
    
    # Convert groupby object to list of tuples
    shuffled = [(word, list(group)) for word, group in shuffled]
    return shuffled

# Reduce function
def reduce_function(mapped_data: Tuple[str, List[Tuple[str, int]]]):
    word, group = mapped_data
    return (word, sum(count for _, count in group))


# Sample data
data = ["Dog", "Cat", "Mouse", "Dog", "Dog", "Cat", "Dog", "Cat", "Duck"]
# Splitting phase
# Split data into 3 chunks
splitted_data = [data[i:i + 3] for i in range(0, len(data), 3)]
# [['Dog', 'Cat', 'Mouse'], ['Dog', 'Dog', 'Cat'], ['Dog', 'Cat', 'Duck']]

# Initialize pool 
if __name__ == '__main__':
    # Create a pool of workers (4 processes)
    pool = Pool(processes=4)
    # Map phase
    mapped = pool.map(map_function, splitted_data)
    # words are mapped to which process?
    # [[('Dog', 1, 'SpawnPoolWorker-1'), ('Cat', 1, 'SpawnPoolWorker-1'), ('Mouse', 1, 'SpawnPoolWorker-1')], [('Dog', 1, 'SpawnPoolWorker-2'), ('Dog', 1, 'SpawnPoolWorker-2'), ('Cat', 1, 'SpawnPoolWorker-2')], ...]
    
    # Flatten and remove process name
    flattened_mapped = [(word, count)
                        for sublist in mapped for word, count, _ in sublist]
    # [('Dog', 1), ('Cat', 1), ('Mouse', 1), ('Dog', 1), ('Dog', 1), ('Cat', 1), ('Dog', 1), ('Cat', 1), ('Duck', 1)]
    
    # Shuffle phase
    shuffled = shuffle_and_sort(flattened_mapped)
    # word to all its corresponding (word, count) pairs
    # [('Cat', [('Cat', 1), ('Cat', 1), ('Cat', 1)]), ('Dog', [('Dog', 1), ('Dog', 1), ('Dog', 1), ('Dog', 1)]), ('Duck', [('Duck', 1)]), ('Mouse', [('Mouse', 1)])]

    # Reduce phase
    reduced = pool.map(reduce_function, shuffled)
    print(list(reduced))
    # [('Cat', 3), ('Dog', 4), ('Duck', 1), ('Mouse', 1)]

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()
