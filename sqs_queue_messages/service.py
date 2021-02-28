import os
import sys
import logging

try:
    from common.base import BasePumpService
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common.base import BasePumpService

import boto3
from boto3.session import Session
import botocore

class SQSMessagesPumpService(BasePumpService):
    def configure(self):
        if Session().get_credentials() is None:
            logging.critical(
                'Please provide AWS credentials via the AWS_ACCESS_KEY_ID '
                'and AWS_SECRET_ACCESS_KEY environment variables.'
            )
            sys.exit(1)
        try:
            self.region = os.environ['AWS_REGION']
            self.sqs_queue_name = os.environ['SQS_QUEUE_NAME']
        except KeyError as e:
            key = e.args[0]
            logging.critical('Missing a required environment variable: ' + key)
            sys.exit(1)

        if self.region not in Session().get_available_regions('sqs'):
            logging.critical(f'{self.region} is not a valid region name for SQS.')
            sys.exit(1)
    
    def poll(self):
        sqs = boto3.resource('sqs', region_name=self.region)
        try:
            queue = sqs.get_queue_by_name(QueueName=self.sqs_queue_name)
        except botocore.errorfactory.QueueDoesNotExist:
            logging.critical('Unable to find an SQS Queue in the specified region' \
                             'with the specified name. Exiting...')
            sys.exit(1)
        logging.info(f'POLL: Found {queue.attributes["ApproximateNumberOfMessages"]} messages in the SQS queue.')
        self.data = queue.attributes['ApproximateNumberOfMessages']


if __name__ == '__main__':
    service = SQSMessagesPumpService()
    service.start()