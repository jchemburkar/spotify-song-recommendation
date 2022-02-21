""" generic utils """
from typing import List

def split_list_n_sized_chunks(data: List, chunk_size: int) -> List[List]:
    """ takes a list and splits it into chunks of size n """
    return [data[i * chunk_size:(i + 1) * chunk_size] for i in range((len(data) + chunk_size - 1) // chunk_size )]
