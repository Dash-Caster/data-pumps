import os
import sys
import logging
import locale

try:
    from common.base import BasePumpService
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common.base import BasePumpService

import calendar
from datetime import datetime
import boto3
from boto3.session import Session
import botocore


class AWSBillPumpService(BasePumpService):
    def configure(self):
        if Session().get_credentials() is None:
            logging.critical(
                'Please provide AWS credentials via the AWS_ACCESS_KEY_ID '
                'and AWS_SECRET_ACCESS_KEY environment variables.'
            )
            sys.exit(1)
        
        self.currency_symbol_dict = {}
        for l in locale.locale_alias:
            try:
                locale.setlocale(locale.LC_ALL, l)
            except locale.Error:
                continue
            conv = locale.localeconv()
            self.currency_symbol_dict[conv['int_curr_symbol'].strip()] = conv['currency_symbol'].strip()
    
    def poll(self):
        dt_now = datetime.utcnow()
        dt_start = datetime(year=dt_now.year, month=dt_now.month, day=1)
        dt_end = datetime(year=dt_now.year, month=dt_now.month, day=calendar.monthrange(dt_now.year, dt_now.month)[1])

        client = boto3.client('ce')
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': dt_start.strftime('%Y-%m-%d'),
                'End': dt_end.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=[
                'AmortizedCost',
            ]
        )
        try:
            amount = float(response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount'])
        except (KeyError, IndexError, ValueError) as e:
            logging.exception(e)
            logging.critical('Unable to parse the amount value from Cost Explorer response.')
            self.data = None
            return

        try:
            unit = response['ResultsByTime'][0]['Total']['AmortizedCost']['Unit']
        except (KeyError, IndexError, ValueError) as e:
            unit = None
            logging.error('Unable to parse the unit value from Cost Explorer response.')

        symbol = None
        if unit in self.currency_symbol_dict:
            symbol = self.currency_symbol_dict[unit]
        
        if symbol:
            self.data = f'{symbol}{round(amount, 2)}'
        elif unit:
            self.data = f'{round(amount, 2)} {unit}'
        else:
            self.data = f'{round(amount, 2)}'
        


if __name__ == '__main__':
    service = AWSBillPumpService()
    service.start()
