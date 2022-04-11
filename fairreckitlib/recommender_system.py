"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os

from .data.registry import DataRegistry
from .data.split.factory import get_split_factory
from .events import io_event
from .events.dispatcher import EventDispatcher
from .experiment.common import EXP_KEY_NAME
from .experiment.common import EXP_KEY_TYPE
from .experiment.common import EXP_TYPE_PREDICTION
from .experiment.common import EXP_TYPE_RECOMMENDATION
from .experiment.experiment import Experiment
from .pipelines.model.factory import create_predictor_model_factory
from .pipelines.model.factory import create_recommender_model_factory


class RecommenderSystem:
    """
    Top level API intended for use by applications
    """
    def __init__(self, data_dir, result_dir, verbose=True):
        self.data_registry = DataRegistry(data_dir)
        self.split_factory = get_split_factory()
        self.predictor_factory = create_predictor_model_factory()
        self.recommender_factory = create_recommender_model_factory()

        self.verbose = verbose
        self.event_dispatcher = EventDispatcher()

        event_listeners = [
            (io_event.ON_MAKE_DIR, io_event.on_make_dir),
            (io_event.ON_REMOVE_DIR, io_event.on_remove_dir),
            (io_event.ON_REMOVE_FILE, io_event.on_remove_file),
            (io_event.ON_RENAME_FILE, io_event.on_rename_file)
        ]

        for _, (event, func_on_event) in enumerate(event_listeners):
            self.event_dispatcher.add_listener(event, self, func_on_event)

        self.result_dir = result_dir
        if not os.path.isdir(self.result_dir):
            os.mkdir(self.result_dir)
            self.event_dispatcher.dispatch(
                io_event.ON_MAKE_DIR,
                dir=self.result_dir
            )

    def abort_experiment(self):
        """TODO"""
        # TODO cancel an active experiment computation
        raise NotImplementedError()

    def evaluate_experiment(self, experiment_dir, config):
        """TODO"""
        result_dir = os.path.join(self.result_dir, experiment_dir)
        if not os.path.isdir(result_dir):
            raise IOError('Result does not exist: ' + result_dir)

        # TODO evaluate additional metrics
        raise NotImplementedError()

    def run_experiment(self, config, num_threads=0):
        """TODO"""
        result_dir = os.path.join(self.result_dir, config[EXP_KEY_NAME])
        if os.path.isdir(result_dir):
            raise IOError('Result already exists: ' + result_dir)

        os.mkdir(result_dir)
        self.event_dispatcher.dispatch(
            io_event.ON_MAKE_DIR,
            dir=result_dir
        )

        run_0_dir = os.path.join(result_dir, 'run_0')
        os.mkdir(run_0_dir)
        self.event_dispatcher.dispatch(
            io_event.ON_MAKE_DIR,
            dir=run_0_dir
        )

        if config[EXP_KEY_TYPE] == EXP_TYPE_PREDICTION:
            model_factory = self.predictor_factory
        elif config[EXP_KEY_TYPE] == EXP_TYPE_RECOMMENDATION:
            model_factory = self.recommender_factory
        else:
            raise NotImplementedError()

        experiment = Experiment(
            self.data_registry,
            self.split_factory,
            model_factory,
            self.event_dispatcher,
            verbose=self.verbose
        )

        experiment.run(
            run_0_dir,
            config,
            num_threads
        )

    def validate_experiment(self, experiment_dir, num_runs):
        """TODO"""
        result_dir = os.path.join(self.result_dir, experiment_dir)
        if not os.path.isdir(result_dir):
            raise IOError('Result does not exist: ' + result_dir)

        # TODO run the same experiment again for 'num_runs'
        raise NotImplementedError()

    def get_available_datasets(self):
        """Gets the available datasets of the recommender system."""
        return self.data_registry.get_info()

    def get_available_metrics(self):
        """Gets the available metrics of the recommender system."""
        raise NotImplementedError()

    def get_available_predictors(self):
        """Gets the available predictors of the recommender system.

        Returns:
            (dict) with all available predictors.
                Each key-value pair describes an API:
                    key(str): name of the API,
                    value(array like): dict entries with predictor name and params.
        """
        return self.predictor_factory.get_available_algorithms()

    def get_available_recommenders(self):
        """Gets the available recommenders of the recommender system.

        Returns:
            (dict) with all available predictors.
                Each key-value pair describes an API:
                    key(str): name of the API,
                    value(array like): dict entries with recommender name and params.
        """
        return self.recommender_factory.get_available_algorithms()

    def get_available_splitters(self):
        """Gets the available splitters of the recommender system."""
        raise NotImplementedError()
