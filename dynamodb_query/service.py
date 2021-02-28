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

import json

class DynamoDbQueryPumpService(BasePumpService):
    def configure(self):
        if Session().get_credentials() is None:
            logging.critical(
                'Please provide AWS credentials via the AWS_ACCESS_KEY_ID '
                'and AWS_SECRET_ACCESS_KEY environment variables.'
            )
            sys.exit(1)

        try:
            self.aws_region = os.environ['AWS_REGION']
            self.operation_mode = os.environ['DYNAMO_OPERATION_MODE']
            self.aggregation_mode = os.environ['DYNAMO_AGGREGATION_MODE']
        except KeyError as e:
            key = e.args[0]
            logging.critical('Missing a required environment variable: ' + key)
            sys.exit(1)

        self.operation_mode = self.operation_mode.strip().lower()
        if self.operation_mode not in ['query', 'scan']:
            logging.critical('Invalid value specified for DYNAMO_OPERATION_MODE. Must be one of "query" or "scan".')
            sys.exit(1)

        self.aggregation_mode = self.aggregation_mode.strip().lower()
        if self.aggregation_mode not in ['count', 'sum', 'average']:
            logging.critical('Invalid value specified for DYNAMO_AGGREGATION_MODE. Must be one of "count", "sum", or "average".')
            sys.exit(1)

        if self.aggregation_mode in ['sum', 'average']:
            try:
                self.aggregation_attribute = os.environ['DYNAMO_AGGREGATION_ATTRIBUTE']
            except KeyError as e:
                logging.critical('DYNAMO_AGGREGATION_ATTRIBUTE value is required for "sum" or "average" aggregation modes.')
                sys.exit(1)

        try:
            with open('arguments.json', 'r') as f:
                self.args = json.load(f)
        except FileNotFoundError as e:
            logging.critical('Unable to find a file named "arguments.json" with operation arguments.')
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            logging.exception(e)
            logging.critical('Unable to load JSON object from the "arguments.json" file.')
            sys.exit(1)
        except Exception as e:
            logging.exception(e)
            logging.critical('Unexpected error occurred while loading "arguments.json" file.')

        if hasattr(self, 'aggregation_attribute'):
            projection_expression = self.args.get('ProjectionExpression', '')
            projection_attrs = [attr.strip() for attr in projection_expression.split(',') if attr]
            if self.aggregation_attribute not in projection_attrs:
                projection_attrs.append(self.aggregation_attribute)
            self.args['ProjectionExpression'] = ', '.join(projection_attrs)


    def poll(self):
        client = boto3.client('dynamodb', region_name=self.aws_region)

        if self.aggregation_mode == 'count':
            self.args.pop('ProjectionExpression', None)
            self.args['Select'] = 'COUNT'
            fn = getattr(client, self.operation_mode)
            results = fn(**self.args)
            self.data = results['Count']
        else:
            self.args.pop('Select', None)
            paginator = client.get_paginator(self.operation_mode)
            items = []
            for page in paginator.paginate(**self.args):
                items.extend(page['Items'])

            attr = self.aggregation_attribute
            if self.aggregation_mode == 'sum':
                self.data = str(round(sum([float(next(iter(item.get(attr, {'N': 0}).values()))) for item in items]), 2))
            elif self.aggregation_mode == 'average':
                self.data = str(round(sum([float(next(iter(item.get(attr, {'N': 0}).values()))) for item in items]) / len(items), 2))


if __name__ == '__main__':
    service = DynamoDbQueryPumpService()
    service.start()
