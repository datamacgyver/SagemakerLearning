"""
This module simply provides an easy place to customise my training job. From
here I could do pretty much whatever I wanted to the model without changing
my notebook (well, within limits. Happy to discuss!)
"""

import sagemaker
from sagemaker.tuner import IntegerParameter, ContinuousParameter, HyperparameterTuner
from config import role, sm_sess


def _init_model(role, output_path, model_name):
    container = sagemaker.image_uris.retrieve('xgboost', sm_sess.boto_region_name, 'latest')

    return sagemaker.estimator.Estimator(container,
                                         role,
                                         base_job_name=model_name,
                                         instance_count=1,
                                         instance_type='ml.m4.xlarge', #'local' can be used for sklearn and the like.
                                         output_path=output_path.as_uri(),
                                         sagemaker_session=sm_sess)


def get_xgb_tuner(output_path, model_name):
    xgb = _init_model(role, output_path, model_name)

    # Set core hyperparameters
    xgb.set_hyperparameters(eval_metric='rmse',
                            objective='reg:linear', # plenty of options out there: https://github.com/dmlc/xgboost/blob/master/doc/parameter.rst#learning-task-parameters
                            num_round=100,
                            rate_drop=0.3,
                            tweedie_variance_power=1.4)

    hyperparemeters_to_tune = {
        'eta': ContinuousParameter(0, 1),
        'min_child_weight': ContinuousParameter(1, 10),
        'alpha': ContinuousParameter(0, 2),
        'max_depth': IntegerParameter(1, 10)
    }

    tuner = HyperparameterTuner(xgb,
                                'validation:rmse',  # objective metric
                                hyperparemeters_to_tune,
                                max_jobs=20,
                                max_parallel_jobs=3,
                                base_tuning_job_name=model_name + "-tuner",
                                objective_type='Minimize')
    return tuner
