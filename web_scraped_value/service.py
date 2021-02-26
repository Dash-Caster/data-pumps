import os
import sys
import logging

try:
    from common.base import BasePumpService
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common.base import BasePumpService

import requests
from parsel import Selector


class WebScrapedValuePumpService(BasePumpService):
    def configure(self):
        try:
            self.webpage_url = os.environ['WEBPAGE_URL']
            self.xpath_selector = os.environ['XPATH_SELECTOR']
        except KeyError as e:
            key = e.args[0]
            logging.critical('Missing a required environment variable: ' + key)
            sys.exit(1)

    def poll(self):
        response = requests.get(self.webpage_url)
        if response.ok:
            try:
                selector = Selector(text=response.text)
                logging.debug("Using selector: " + self.xpath_selector)
                if not selector.xpath(self.xpath_selector).get():
                    logging.error("Unable to find a value by the specified XPATH_SELECTOR.")
                else:
                    self.data = selector.xpath(self.xpath_selector).get()
            except Exception as e:
                logging.exception(e)
                logging.critical("Could not find selector.")
        else:
            logging.error('Unable to get a valid response from the specifed WEBPAGE_URL.')
            self.data = None



if __name__ == '__main__':
    service = WebScrapedValuePumpService()
    service.start()
