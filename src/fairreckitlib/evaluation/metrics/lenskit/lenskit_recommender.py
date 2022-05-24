"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from typing import Any, Dict

from lenskit import topn

from src.fairreckitlib.evaluation.metrics.evaluator import Evaluator
from src.fairreckitlib.evaluation.metrics.lenskit.lenskit_evaluator import LensKitEvaluator
from src.fairreckitlib.evaluation.metrics.metric_factory import KEY_METRIC_PARAM_K


class LensKitRecommendationEvaluator(Evaluator):
    """Predictor implementation for the LensKit framework."""

    # TODO eval_func is a function
    def __init__(self, eval_func: Any, params: Dict[str, Any], **kwargs):
        Evaluator.__init__(self, eval_func, params)
        self.group = kwargs['group']

    def evaluate(self, test_set, recs):
        print(test_set.head())
        print(recs.head())
        analysis = topn.RecListAnalysis()
        analysis.add_metric(self.eval_func, k=self.params[KEY_METRIC_PARAM_K])
        results = analysis.compute(recs, test_set).head()

        evaluation = results.groupby('Algorithm')[self.group].mean()[0]

        return evaluation
