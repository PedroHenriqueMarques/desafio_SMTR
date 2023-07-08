
from concurrent.futures import ThreadPoolExecutor
from typing import List, Iterator, Callable

import pandas as pd
from prefect import task


def chunks(lst: List, n: int) -> Iterator[int]:
    '''Yield successive n-sized chunks from lst.
    '''

    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@task
def parallel_function(func: Callable[[List[int]], pd.DataFrame], 
                      req_args: List, 
                      workers: int | None = None) -> pd.DataFrame:
    ''' Distribute request batches into <workers> threads for faster
    collection of data. Returns a pandas dataframe.
    '''

    #  if there is no number of threads, use 1 thread (python default).
    if not workers:
        workers = 1
    
    #  Generates a sub list from req_args with [1, <workers>] sized sub list. 
    chunk_list = chunks(req_args, workers)

    #  Each thread will return its result to the thread_res variable.
    with ThreadPoolExecutor(max_workers=workers) as executor:
        thread_res = list(executor.map(func, chunk_list))

    #  Combines the results in a dataframe.
    df_ids = pd.DataFrame()
    for df_res in thread_res:
        df_ids = pd.concat([df_ids, df_res], ignore_index=True)

    return df_ids


if __name__ == '__main__':
    f = lambda x: pd.Series(x)
    x = parallel_function(f, list(range(1000)), 2)
    print(x)