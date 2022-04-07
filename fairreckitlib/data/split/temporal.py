"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import lenskit.crossfold as xf

from .base import DataSplitter


class TemporalSplitter(DataSplitter):

    def run(self, df, test_ratio, params):
        # Note: for this function to work, it needs a 'user' and 'timestamp' header.
        for train_set, test_set in xf.partition_users(df, 1 / test_ratio, xf.LastFrac(test_ratio)):
            return train_set, test_set



def create_temporal_splitter():
    return TemporalSplitter()
