#This files generates some train data from an local SKLearnProcessor
#runs a local SKLearn training job and finally uses the model 
#to run some local predictions

from sagemaker.local import LocalSession
from sagemaker.processing import ProcessingOutput
from sagemaker.sklearn.processing import SKLearnProcessor
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
>>>>>>> ccb7363 (Processing Job Working)
sagemaker_session = LocalSession()
sagemaker_session.config = {'local': {'local_code': True}}

import boto3
import pandas as pd
import tarfile
import os

def main():
    role = 'arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001'
    bucket = os.environ["BUCKET"]
    path = "/processingJob/run-"+ datetime.now().strftime("%d%m%Y_%H_%M_%S")
    runProcessingJob(role, bucket, path)


def runProcessingJob(role, bucket, path):
    output_dir = "/opt/ml/processing/processed_data/"
    processor = SKLearnProcessor(
        framework_version = '1.0-1',
        instance_count = 1,
        instance_type = 'local',
        role = role 
    )
    print('Starting processing job.')
    processor.run(
        code='process.py',
        outputs=[
                ProcessingOutput(
                    output_name='train-test',
                    source=output_dir,
                    destination= bucket + path,
                    s3_upload_mode="EndOfJob"
                ),
            ],
        arguments=[
            '--train-ratio', '0.8',
            '--output-dir', output_dir
        ]
    )

if __name__ == "__main__":
    main()