import abc
import time
import sys
import requests
import logging
import os
import json

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} {levelname:<8} {message}',
    style='{'
)

class BasePumpService(metaclass=abc.ABCMeta):
    def __init__(self):
        try:
            config_data = json.load(open('./common/config.json', 'r'))
        except FileNotFoundError:
            config_data = json.load(open('../common/config.json', 'r'))
        
        try:
            self.base_url = config_data['base_url']
        except KeyError as e:
            logging.critical('base_url not found in config.json.')
            sys.exit(1)

        try:
            self.editor_id = os.environ['EDITOR_ID']
            self.entity_id = os.environ['DATA_ID']
            try:
                self.interval = float(os.environ['POLL_INTERVAL']) * 60
            except (KeyError, ValueError) as e:
                self.interval = 5 * 60
                logging.debug(e)
                logging.debug('POLL_INTERVAL environment variable not found or invalid. Using default of 5 minutes.')
        except KeyError as e:
            key = e.args[0]
            logging.critical('Missing a required environment variable: ' + key)
            sys.exit(1)
        
        self.configure()
        self.data = None

    @abc.abstractmethod
    def configure(self):
        pass

    @abc.abstractmethod
    def poll(self):
        pass

    def pump(self):
        assert getattr(self, 'data', None), 'Data could not be polled successfully. Aborting pump...'
        update_data = {
            'entity_id': self.entity_id,
            'properties': [{'current_value': self.data}]
        }
        headers = {
            'x-editor-id': self.editor_id
        }
        response = requests.put(self.base_url + '/data', json=update_data, headers=headers)
        if response.ok:
            body = response.json()
            if 'error' or 'message' in body:
                if body.get('error'):
                    if body['error'].lower().strip() == 'no_email':
                        logging.critical('Your DashCaster Dashboard Demo period has expired. ' \
                                         'Please extend your trial by providing an e-mail address ' \
                                         'on the DashCaster web interface.'
                                        )
                    elif body['error'].lower().strip() == 'not_paid':
                        logging.critical('Your DashCaster Dashboard Trial period has expired. ' \
                                         'Please extend your subscription by subscribing to a ' \
                                         'DashCaster monthly or yearly plan on the DashCaster web interface.'
                                        )
                    elif body['error'].lower().strip() == 'unauthorized':
                        logging.critical('Unable to authenticate with DashCaster ' \
                                         'using the provided credentials.'
                                        )
                    else:
                        logging.critical('An unknown error occurred: ' + body['error'])
                    sys.exit(1)
                elif body.get('message'):
                    if body['message'].lower().strip() == 'unauthorized':
                        logging.critical('Unable to authenticate with DashCaster ' \
                                         'using the provided credentials.'
                                        )
                    else:
                        logging.critical('An unknown error occurred: ' + body['message'])
                    sys.exit(1)
        else:
            logging.critical('PUMP: Unable to get a response from DashCaster.')

        self.data = None


    def start(self):
        while True:
            # Poll for data
            try:
                self.poll()
                if self.data:
                    logging.info('Data polled successfully...')
            except Exception as e:
                logging.error(e)
                logging.error('Unexpected error occurred while polling for data.')

            # Pump the data
            try:
                self.pump()
                logging.info('Data pump successful...')
            except Exception as e:
                logging.error(e)
                logging.error('Unexpected error occurred while pumping the data.')
            
            # Wait for sleep interval
            logging.info(f'Sleeping for {self.interval} seconds...')
            time.sleep(self.interval)
