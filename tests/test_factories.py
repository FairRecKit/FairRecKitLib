"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import pytest

from src.fairreckitlib.core.config_constants import KEY_NAME, KEY_PARAMS
from src.fairreckitlib.core.config_constants import KEY_RATED_ITEMS_FILTER
from src.fairreckitlib.core.config_constants import TYPE_PREDICTION, TYPE_RECOMMENDATION
from src.fairreckitlib.core.config_params import ConfigParameters, create_empty_parameters
from src.fairreckitlib.core.factories import Factory, GroupFactory, create_factory_from_list
from src.fairreckitlib.data.set.dataset import DATASET_RATINGS_EXPLICIT
from src.fairreckitlib.data.split.base_splitter import DataSplitter
from src.fairreckitlib.data.split.split_factory import create_split_factory
from src.fairreckitlib.model.algorithms.base_predictor import BasePredictor
from src.fairreckitlib.model.algorithms.base_recommender import BaseRecommender
from src.fairreckitlib.model.model_factory import create_model_factory

dummy_names = ['dummy_a', 'dummy_b', 'dummy_c']


def create_dummy_obj(name, params, **kwargs):
    """Create dummy object that returns the function arguments."""
    return name, params, kwargs


def create_dummy_params():
    """Create dummy config that has at least one parameter."""
    params = ConfigParameters()
    params.add_random_seed('seed')
    return params


def test_factory_add_and_available():
    """Test adding objects to factory and (name) availability."""
    factory = Factory('factory')
    for i, name in enumerate(dummy_names):
        assert not factory.is_obj_available(name), 'object should not be available'
        assert factory.get_num_entries() == i

        factory.add_obj(name, create_dummy_obj, None)

        assert factory.get_num_entries() == i + 1
        assert factory.is_obj_available(name), 'object should be available'

        pytest.raises(KeyError, factory.add_obj, name, create_dummy_obj, None)

        assert name in factory.get_available_names(), 'object should be available'

    availability = factory.get_available()
    assert len(availability) == factory.get_num_entries(), 'availability should have the same' \
                                                           'length as the number of entries'

    for _, entry in enumerate(availability):
        assert KEY_NAME in entry, 'each entry should have a name'
        assert KEY_PARAMS in entry, 'each entry should have parameters'
        assert entry[KEY_NAME] in dummy_names, 'name of the entry should be in the original list.'


def test_factory_create():
    """Test object creation with parameters and keyword arguments."""
    obj_name = 'obj'
    obj_kwargs = { 'kwargs': True }
    obj_params = { 'params': True }

    factory = Factory('factory')
    factory.add_obj(obj_name, create_dummy_obj, create_dummy_params)

    assert factory.create(obj_name + '1') is None, 'object should not exist.'

    # check creation with default params and no kwargs
    name, params, kwargs = factory.create(obj_name, None, **{})

    assert len(params) == create_dummy_params().get_num_params(), 'expected default params'
    assert len(kwargs) == 0, 'expected no keyword arguments'

    # check creation with params and kwargs
    name, params, kwargs = factory.create(obj_name, obj_params, **obj_kwargs)

    assert name == obj_name, 'expected object name.'
    assert params['params'], 'expected object params.'
    assert kwargs['kwargs'], 'expected object kwargs.'


@pytest.mark.parametrize('create_params', [None, create_dummy_params])
def test_factory_create_params(create_params):
    """Test parameter creation for objects."""
    factory = Factory('factory')
    factory.add_obj('obj', create_dummy_obj, create_params)

    params = factory.create_params('obj')
    assert params.get_num_params() == 0 if create_params is None else 1

    params = factory.create_params('obj1')
    assert params.get_num_params() == 0, 'non existing object should have no parameters.'


def test_factory_create_from_tuples():
    """Test factory creation from a list of object name/create/parameters tuples."""
    obj_tuple_list = []

    factory = create_factory_from_list('factory', obj_tuple_list)
    assert factory.get_num_entries() == 0, 'factory should have no entries for an empty list.'

    obj_tuple_list = [(name, create_dummy_obj, create_empty_parameters) for name in dummy_names]

    factory = create_factory_from_list('factory', obj_tuple_list)
    assert factory.get_num_entries() == len(obj_tuple_list), 'factory should have all tuples' \
                                                             'added after creation.'


@pytest.mark.parametrize('create_factory', [Factory, GroupFactory])
def test_factory_name(create_factory):
    """Test (group) factory names are correct."""
    for _, name in enumerate(dummy_names):
        factory = create_factory(name)
        assert factory.get_name() == name, 'factory name should be the same after creation.'


@pytest.mark.parametrize('create_child_factory', [Factory, GroupFactory])
def test_group_factory_add_and_available(create_child_factory):
    """Test adding child factories to group factory and (name) availability."""
    group = GroupFactory('group')
    for i, name in enumerate(dummy_names):
        factory = create_child_factory(name)

        assert group.get_factory(name) is None, 'factory should not be available.'
        assert group.get_num_entries() == i

        group.add_factory(factory)

        assert group.get_factory(name) is not None, 'factory should be available.'
        assert group.get_num_entries() == i + 1

        pytest.raises(KeyError, group.add_factory, factory)

        assert name in group.get_available_names(), 'factory should be in available names.'
        assert not group.is_obj_available(name), 'factory should not be available, only objects.'

    availability = group.get_available()
    assert len(availability) == group.get_num_entries(), 'availability should have the same' \
                                                         ' length as the number of entries'

    child_name = 'child'
    child = Factory('child')
    child.add_obj('obj', create_dummy_obj, None)
    group.add_factory(child)
    assert group.is_obj_available('obj'), 'obj should be available in the child factory.'

    for factory_name, factory_availability in availability.items():
        if factory_name == child_name:
            assert len(factory_availability) == 1, 'child factory should have one available entry.'
        else:
            assert factory_name in dummy_names, 'factory name should be in the original list'
            assert len(factory_availability) == 0, 'each original factory has no availability'


@pytest.mark.parametrize('model_type, algo_type', [
    (TYPE_PREDICTION, BasePredictor), (TYPE_RECOMMENDATION, BaseRecommender)
])
def test_model_factory(model_type, algo_type):
    """Test if all algorithms of different model types are derived from the correct base class."""
    api_factory = create_model_factory().get_factory(model_type)

    for _, api_name in enumerate(api_factory.get_available_names()):
        algo_factory = api_factory.get_factory(api_name)

        for _, algo_name in enumerate(algo_factory.get_available_names()):
            # contains correct entries for all algorithms across different apis and types
            algo_kwargs = {
                'rating_type': DATASET_RATINGS_EXPLICIT,
                'rating_scale': (1.0, 5.0),
                KEY_RATED_ITEMS_FILTER: True,
                'num_threads': 1
            }
            algo_params = None
            algo = algo_factory.create(algo_name, algo_params, **algo_kwargs)
            assert isinstance(algo, algo_type), str(model_type) + ' algorithm has incorrect' \
                                                                  'type: ' + algo_name


def test_split_factory():
    """Test if all splitters in the factory are derived from the correct base class."""
    split_factory = create_split_factory()
    for _, splitter_name in enumerate(split_factory.get_available_names()):
        splitter = split_factory.create(splitter_name)
        assert isinstance(splitter, DataSplitter)
