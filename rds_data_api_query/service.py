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

import random

class RDSDataQueryPumpService(BasePumpService):
    def configure(self):
        if Session().get_credentials() is None:
            logging.critical(
                'Please provide AWS credentials via the AWS_ACCESS_KEY_ID '
                'and AWS_SECRET_ACCESS_KEY environment variables.'
            )
            sys.exit(1)

        try:
            self.aws_region = os.environ['AWS_REGION']
            self.rds_db_name = os.environ['RDS_DB_NAME']
            self.rds_db_arn = os.environ['RDS_DB_ARN']
            self.rds_db_secret_arn = os.environ['RDS_DB_SECRET_ARN']
            self.sql_statement = os.environ['SQL_STATEMENT']
        except KeyError as e:
            key = e.args[0]
            logging.critical('Missing a required environment variable: ' + key)
            sys.exit(1)

    def poll(self):
        client = boto3.client('rds-data', region_name=self.aws_region)
        logging.error("Query is")
        logging.error(self.sql_statement)
        query_result = client.execute_statement(
            secretArn=self.rds_db_secret_arn,
            database=self.rds_db_name,
            resourceArn=self.rds_db_arn,
            sql=self.sql_statement
        )
        try:
            data_dict = query_result['records'][0][0]
            self.data = next(iter(data_dict.values()))
        except (KeyError, IndexError, StopIteration) as e:
            logging.exception(e)
            logging.critical('Unable to get results for the SQL Query.')
            self.data = None


if __name__ == '__main__':
    service = RDSDataQueryPumpService()
    service.start()
