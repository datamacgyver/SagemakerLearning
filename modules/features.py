import re
from warnings import warn

import pandas as pd

# Feature creation config
BAND_COLS = ["lastpayband", "CollectionsBand", "balanceband", "remainingbalband"]
NA_FILL_COLS = ["Accountid", "SDL3m", "SDL6m", "SDL12m", "SDL24m", "SDHist",
                "VarL3m", "VarL6m", "VarL12m", "VarL24m", "VarHist", "monthstodefault",
                "age"]
DROP_COLS = ["Accountid", "Month", "PrevCols", "insample", "DefaultDate", "settlementdate", "transflag",
             "Number", "PreviousPayments", "collectionstodate",  # All on this row are single val
             "cumpctofbalance", "settle",
             "pay", "MonthlyTransaction", "repaid"  # Not in NewData
             ]


def _get_numeric_band(df_in, band_cols, n_suffix="N"):
    """
    For each band_col, get the number ID of the band, save that
    to a column and drop the original. Needed as there was an
    error in the input data.
    # TODO: one hot / get dummies instead.
    """
    for col in band_cols:
        bandN = df_in.loc[:, col].apply(lambda x: re.sub(r"\).*", "", x)).astype("int")
        df_in[col+n_suffix] = bandN
        df_in = df_in.drop([col], axis=1)
    return df_in


def _drop_useless_cols(df_in, drop_cols, include_bands=True):
    if include_bands:
        band_cat_cols = [c for c in df_in.columns if re.search("Band[0-9]+_\(.*", c)]
        df_in = df_in.drop(band_cat_cols, axis=1)

    drop_cols = [d for d in drop_cols if d in df_in.columns]
    df_in = df_in.drop(drop_cols, axis=1)
    return df_in


def _fill_nas(df_in, na_fill_cols, fill_val=-9999):
    """
    As we are using a non-linear model I usually prefer extreme value
    replacement for my NAs as I feel it gives the model a clue that
    something is different. It can depend on *why* they are NA.
    """
    for c in na_fill_cols:
        df_in[c] = df_in[c].fillna(fill_val)

    return df_in


def _create_y(df_in):
    """
    This is a function unique to this model so shouldn't techincally live
    with the above generic functions. It takes the difference between min
    and max balance over a 12 month period and uses that to calculate the
    proportion repaid. It also ensures that that this number is not >1 which
    happens when overpayments occurr.
    """
    y = df_in \
        .loc[df_in.Number < 12, ["Accountid", "remainingbalance", "CurrentBalance"]] \
        .groupby("Accountid", as_index=False) \
        .agg({"remainingbalance": ["min"], "CurrentBalance": ["max"]})

    y["PropRepaid"] = 1 - (y['remainingbalance']['min'] / y['CurrentBalance']['max'])
    y = y[["Accountid", "PropRepaid"]]
    y.columns = y.columns.droplevel(1)

    y.loc[y.PropRepaid > 1, "PropRepaid"] = 1.0  # Yeah, this happens. Gonna set to 1 as I may want to go logistic
    return y.merge(df_in.loc[df_in.Number == 0], on="Accountid")


def _data_quality_tests(df_in):
    """
    Runs a couple of checks to see if I've broken anything! Raises
    if NAs are found, warns if single valued.
    # TODO: More!

    Parameters
    ----------
    df_in: pd.DataFrame
        Processed df ready for output

    Returns
    -------
    None
        Raises if NAs are present

    """
    if df_in.isnull().any(axis=1).sum() > 0:
        raise AssertionError("NAs in the dataset!\n%s" % df_in.isnull().head())

    for c in df_in.columns:
        if df_in[c].nunique() == 1:
            warn("Column %s is single valued" % c)


def create_features(df, make_y=True):
    """
    Entry function to all of the above.
    #TODO: I'm still not convinced of the transflag fix
    """
    df = _get_numeric_band(df, BAND_COLS, n_suffix="N")
    df = _fill_nas(df, NA_FILL_COLS)
    if make_y:
        df = _create_y(df)
    df = df.loc[df.transflag == 1]  # transflag == 0 means they won't pay anything so don't bother.
    df = _drop_useless_cols(df, DROP_COLS)

    _data_quality_tests(df)
    return df


if __name__ == "__main__":
    print("todo")
