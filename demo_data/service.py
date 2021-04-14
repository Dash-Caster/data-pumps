import os
import sys
import logging

try:
    from common.base import BasePumpService
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common.base import BasePumpService


class DemoDataPumpService(BasePumpService):
    def configure(self):
        demo_values = os.getenv("VALUE_LIST")
        try:
            self.values = [int(value.strip()) for value in demo_values.split(',')]
        except Exception as e:
            logging.debug(e)
            logging.critical(
                "Invalid value provided for VALUE_LIST. "  \
                "Please provide a valid comma-separated value list containing numberes only. "  \
                "E.g. \"44, 42,43, 45, 58\"."
            )
            sys.exit(1)
        self.current_index = 0

    def poll(self):
        if self.current_index >= len(self.values):
            self.current_index = 0
        self.data = self.values[self.current_index]
        self.current_index += 1


if __name__ == "__main__":
    service = DemoDataPumpService()
    service.start()