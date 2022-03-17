
"""

"""

import pandas as pd
from dataloaders.utility import get_configs
from typing import Dict
import os

CONFIGS = get_configs(os.path.dirname(os.path.abspath(__file__)) + "\\config.ini")

def dataloader(dataset: str) -> Dict[str, pd.DataFrame]:
    """
    This function takes a dataset and returns a dictionary contains the content of each file in one dataframe
    """
    dfs = dict()
    for sub_dataset in [section for section in CONFIGS.sections() if section.startswith(dataset)]:
        params = dict(delimiter=CONFIGS.get(sub_dataset, "delimeter", fallback=","), names=CONFIGS.get(sub_dataset, "headers").split(","))
        if CONFIGS.get(sub_dataset, "timestamp", fallback=None):
            params.update(dict(date_parser=CONFIGS.get(sub_dataset, "timestamp").split(",")))
        df = pd.read_csv(CONFIGS.get(sub_dataset, "file_path"), **params)
        df.set_index(CONFIGS.get(sub_dataset, "index_key", fallback=None), inplace=True)
        dfs.update(dict(sub_dataset=df))
    
    # Return the dataframe
    return dfs

# from dataloaders import dataloaders as dl
# dl.dataloader('lfm_360k')
