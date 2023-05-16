import os
import sys
import logging

try:
    from common.base import BasePumpService
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common.base import BasePumpService

import pyowm
from pyowm import OWM

class WeatherDataPumpService(BasePumpService):

    def configure(self):
        api_key = os.getenv('OWM_API_KEY')
        location = os.getenv('LOCATION')
        self.temp_unit = os.getenv('TEMP_UNIT', 'celsius').lower()

        if not api_key:
            logging.critical('Required parameter OWM_API_KEY not specified. Aborting...')
            sys.exit(1)
        
        if not location:
            logging.critical('Required parameter LOCATION not specified. Aborting...')
            sys.exit(1)

        if self.temp_unit not in ['celsius', 'fahrenheit']:
            logging.critical('Invalid value specified for parameter TEMP_UNIT. Use one of: \'celsius\', \'fahrenheit\'. Aborting...')
            sys.exit(1)
        
        owm = OWM(api_key)
        self.weather_manager = owm.weather_manager()

        try:
            observation = self.weather_manager.weather_at_place(location)
        except pyowm.commons.exceptions.NotFoundError:
            logging.critical(f'Unable to find specified location {location}. Aborting...')
            sys.exit(1)
        except pyowm.commons.exceptions.UnauthorizedError:
            logging.critical('Unable to authenticate using the specified API key. Aborting...')
            sys.exit(1)
        
        self.location_id = observation.location.id

    def poll(self):
        observation = self.weather_manager.weather_at_id(self.location_id)
        temperature = observation.weather.temperature(self.temp_unit)
        temp_value = temperature.get('temp')
        formatted_value = f'{round(temp_value)} °{self.temp_unit[0].upper()}'
        self.data = formatted_value


if __name__ == "__main__":
    service = WeatherDataPumpService()
    service.start()