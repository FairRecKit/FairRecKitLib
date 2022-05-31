"""This module contains the base class for data splitting.

Classes:

    DataSplitter: the base class for data splitting.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from typing import Any, Dict, Tuple

import pandas as pd

from ..data_modifier import DataModifier


class DataSplitter(DataModifier):
    """Base class for FairRecKit data splitters.

    A splitter is used to split a dataframe into a train and test set.

    Public methods:

    get_test_ratio
    """

    def __init__(self, name: str, params: Dict[str, Any], test_ratio: float):
        """Construct the base splitter.

        The constructor raises a RuntimeError if the test ratio is not within the
        accepted range of 0.01 < ratio < 0.99.

        Args:
            name: the name of the splitter.
            params: a dictionary containing the parameters for the splitter.
            test_ratio: the fraction of users to use for testing.
        """
        DataModifier.__init__(self, name, params)
        self.test_ratio = test_ratio

        if self.test_ratio < 0.01 or self.test_ratio > 0.99:
            raise RuntimeError()

    def get_test_ratio(self) -> float:
        """Get the test ratio used by the splitter when run.

        Returns:
            the test ratio
        """
        return self.test_ratio

    def run(self, dataframe: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Run the splitter on the specified dataframe.

        Args:
            dataframe: with at least the 'user' column.

        Returns:
            the train and test set dataframes of the split.
        """
        raise NotImplementedError()
