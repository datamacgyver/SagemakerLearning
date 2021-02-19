import pickle
import tarfile

import smart_open as smart
from plotnine import *
from plotnine.themes import theme_minimal

from config import boto_session


def _is_num(x):
    try:
        float(x)
        return 1
    except:
        return 0


def plot_tuning(tuner):
    """
    Simply spin over each hyper parameter in the tuner and plot
    how the error changes.
    """
    ranges = tuner.analytics().tuning_ranges
    df = tuner.analytics().dataframe()
    figures = []
    for hp_name, hp_range in ranges.items():
        g = ggplot(df, aes(x=hp_name, y='FinalObjectiveValue')) +\
            geom_point(colour="steelblue", alpha=0.8)+\
            ggtitle("Objective vs %s" % hp_name)+\
            xlab(hp_name) +\
            ylab("objective function")+\
            theme_minimal()

        g.draw()


def get_var_imp(df_with_cols, model_loc, importance_type="weight"):
    """
    Go get the best model and extrac the given importance type,
    returning a dict of importances.
    Defaults to weight but options are:
    * ‘weight’: the number of times a feature is used to split the data across all trees.
    * ‘gain’: the average gain across all splits the feature is used in.
    * ‘cover’: the average coverage across all splits the feature is used in.
    * ‘total_gain’: the total gain across all splits the feature is used in.
    * ‘total_cover’: the total coverage across all splits the feature is used in.
    """

    with smart.open(model_loc.as_uri(), 'rb', transport_params={'session': boto_session}) as f:
        with tarfile.open(fileobj=f, mode='r') as tar_f:
            with tar_f.extractfile("xgboost-model") as extracted_f:
                xgbooster = pickle.load(extracted_f)

    var_imp = xgbooster.get_score(importance_type=importance_type)  # Uses weight (times used to split)
    col_names = df_with_cols.columns.tolist()
    col_names = col_names[1:]  # Assuming index 1 is predictor

    # Replace index numbers with columns from data frame
    var_imp = {v: col_names[int(k[1:])] for k, v in var_imp.items()}
    return var_imp


def plot_errors(validation_df, predictions):
    """
    Take the actuals off predictions and plot the differences as both histograms
    and scatters.
    """
    validation_df['predictions'] = predictions[0]
    validation_df['err'] = validation_df.predictions - validation_df.PropRepaid

    g = ggplot(validation_df, aes(x='err')) + \
        geom_histogram(fill='steelblue', alpha=0.8) + \
        xlab("Residual Error") + \
        ylab("Freq") + \
        theme_minimal()
    g.draw()

    validation_df = validation_df.reset_index(drop=False)
    g = ggplot(validation_df, aes(x='index', y='err')) + \
        geom_point(colour='steelblue', alpha=0.8) + \
        xlab("") + \
        ylab("Residual") + \
        theme_minimal() + \
        theme(axis_text_x=element_blank())
    g.draw()

    g = ggplot(validation_df, aes(x='PropRepaid', y='predictions')) + \
        geom_point(colour='steelblue', alpha=0.8) + \
        xlab("PropRepaid") + \
        ylab("prediction") + \
        theme_minimal() + \
        theme(axis_text_x=element_blank())
    g.draw()

    validation_df['propBucket'] = validation_df.PropRepaid.round(decimals=1).astype('str')
    g = ggplot(validation_df, aes(x='propBucket', y='err')) + \
        geom_boxplot(fill='steelblue', alpha=0.6) + \
        xlab("Rounded Proportion") + \
        ylab("Residual Err") + \
        theme_minimal()
    g.draw()

# if __name__ == "__main__":
#     import os
#     import boto3
#     import pandas as pd
#     os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
#     boto_session = boto3.session.Session(profile_name='saml')
#     model_loc = 's3://robtests/sagemaker/aa/output/aamod20200124-tuner-210129-2303-006-8dd64a24/output/model.tar.gz'
#     get_var_imp(pd.read_csv(r"C:\z\azzass\data\outputs\validation.csv"), model_loc, boto_session)
