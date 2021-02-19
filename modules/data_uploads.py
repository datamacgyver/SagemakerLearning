import numpy as np
from sagemaker import TrainingInput

from config import data_dir, s3_train_loc, s3_test_loc, s3_validation_loc
from modules.utils import push_sm_csv


class DataUploader:
    """
    Does this *have* to be an object? No, I was bored. Basically this
    just runs the data splits and uploads/saves as appropriate, you can then extract
    the training datasets for tuning.
    """
    def __init__(self, df, train=0.7, test=0.2, validate=0.1):
        self.df = df
        # Yes, this is a bit much for a constructor
        self.train_df, self.test_df, self.validation_df = self._do_split(train, test, validate)

    def _do_split(self, train, test, validate):
        split_fracs = [int(train * len(self.df)), int((1-validate) * len(self.df))]
        return np.split(self.df.sample(frac=1, random_state=49), split_fracs)

    def check_split(self):
        print("Data Split. initial len: %s train_len: %s, test_len: %s, validation_len: %s" %
              (len(self.df), len(self.train_df), len(self.test_df), len(self.validation_df)))

    def save_local(self):
        # TODO: Object to wrap all this file stuff up more neatly?
        self.train_df.to_csv(data_dir / 'train.csv', index=False, header=False)
        self.test_df.to_csv(data_dir / 'test.csv', index=False, header=False)
        self.validation_df.to_csv(data_dir / 'validation.csv', index=False)

    def validation_df(self):
        return self.validation_df()

    def save_s3(self):
        push_sm_csv(s3_train_loc / 'train.csv', self.train_df, index=False, header=False)
        push_sm_csv(s3_test_loc / 'test.csv', self.test_df, index=False, header=False)
        push_sm_csv(s3_validation_loc / 'validation.csv', self.validation_df.drop(['PropRepaid'], axis=1),
                    index=False, header=False)

    def s3_train_in(self):
        return TrainingInput(s3_data=s3_train_loc.as_uri(), content_type='csv')

    def s3_test_in(self):
        return TrainingInput(s3_data=s3_test_loc.as_uri(), content_type='csv')

