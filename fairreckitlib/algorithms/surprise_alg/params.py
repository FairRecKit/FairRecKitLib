"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from ..params import *


def get_params_baseline_only_als():
    return {
        PARAM_KEY_VALUES: [
            _create_param_epochs(10),
            _create_param_regularization('reg_i', 10),
            _create_param_regularization('reg_u', 15)
        ],
        PARAM_KEY_OPTIONS: []
    }


def get_params_baseline_only_sgd():
    return {
        PARAM_KEY_VALUES: [
            _create_param_epochs(20),
            _create_param_regularization('regularization', 0.02),
            _create_param_learning_rate('learning_rate', 0.005),
        ],
        PARAM_KEY_OPTIONS: []
    }


def get_params_co_clustering():
    return {
        PARAM_KEY_VALUES: [
            _create_param_epochs(20),
            create_value_param('user_clusters', 0, 30, 3),
            create_value_param('item_clusters', 0, 30, 3),
            create_param_seed('random_seed')
        ],
        PARAM_KEY_OPTIONS: []
    }

def get_params_nmf():
    return {
        PARAM_KEY_VALUES: [
            create_param_factors(15),
            _create_param_epochs(50),
            _create_param_regularization('reg_pu', 0.06),
            _create_param_regularization('reg_qi', 0.06),
            _create_param_regularization('reg_bu', 0.02),
            _create_param_regularization('reg_bi', 0.02),
            _create_param_learning_rate('lr_bu', 0.005),
            _create_param_learning_rate('lr_bi', 0.005),
            create_value_param('init_low', 0, 100, 0),
            create_value_param('init_high', 0, 100, 1),
            create_param_seed('random_seed')
        ],
        PARAM_KEY_OPTIONS: [
            create_param_bool('biased', False)
        ]
    }


def get_params_empty():
    return {
        PARAM_KEY_VALUES: [],
        PARAM_KEY_OPTIONS: []
    }


def get_params_svd():
    return {
        PARAM_KEY_VALUES: [
            create_param_factors(100),
            _create_param_epochs(20),
            _create_param_init_mean(),
            _create_param_init_std_dev(),
            _create_param_learning_rate('learning_rate', 0.005),
            _create_param_regularization('regularization', 0.02),
            create_param_seed('random_seed')
        ],
        PARAM_KEY_OPTIONS: [
            create_param_bool('biased', True)
        ]
    }


def get_params_svd_pp():
    return {
        PARAM_KEY_VALUES: [
            create_param_factors(20),
            _create_param_epochs(20),
            _create_param_init_mean(),
            _create_param_init_std_dev(),
            _create_param_learning_rate('learning_rate', 0.007),
            _create_param_regularization('regularization', 0.02),
            create_param_seed('random_seed')
        ],
        PARAM_KEY_OPTIONS: []
    }


def _create_param_epochs(epochs):
    return create_value_param('epochs', 1, 50, epochs)


def _create_param_init_mean():
    return create_value_param('init_mean', -1000, 1000, 0)


def _create_param_init_std_dev():
    return create_value_param('init_std_dev', 0.0, 1.0, 0.1)


def _create_param_learning_rate(name, learning_rate):
    return create_value_param(name, 0.0001, 1.0, learning_rate)


def _create_param_regularization(name, regularization):
    return create_value_param(name, 0.0001, 1.0, regularization)
