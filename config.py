"""
A lot of what you see here should be passed to the notebook at runtime.
"""

from pathlib import Path
import os

from s3path import PureS3Path
import boto3
from botocore.exceptions import ClientError
import sagemaker

# Main names and paths
model_name = "aamod20200130"
data_dir = Path("./data/outputs/")
s3_root = PureS3Path('/robtests/sagemaker/aa/')

# train/test/validate dirs in S3
s3_train_loc = s3_root / "train"
s3_test_loc = s3_root / "test"
s3_validation_loc = s3_root / "validation"

# Predict in/out in s3
s3_predict_in = s3_root / 'predictions_in'
s3_predict_out = s3_root / 'predictions_out'

# Boto3 connection (this handles talking to AWS)
os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
boto_session = boto3.session.Session(profile_name='saml')

# sagemaker specific AWS interfaces
sm_sess = sagemaker.Session(boto_session=boto_session)
sm_client = boto_session.client('sagemaker')

# role to define my permissions on AWS, autopopulates if you are on sagemaker.
try:
    role = sagemaker.get_execution_role()
except ClientError:
    role = ""
