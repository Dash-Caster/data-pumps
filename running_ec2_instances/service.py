import os
import sys
import logging

try:
    from common.base import BasePumpService
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common.base import BasePumpService

from boto3.session import Session
import botocore

class RunningEC2PumpService(BasePumpService):
    def configure(self):
        if Session().get_credentials() is None:
            logging.critical(
                "Please provide AWS credentials via the AWS_ACCESS_KEY_ID "
                "and AWS_SECRET_ACCESS_KEY environment variables."
            )
            sys.exit(1)
        self.regions = os.getenv("AWS_REGIONS")

    def poll(self):
        session = Session()

        # Get available regions for EC2
        ec2_regions = session.get_available_regions('ec2')

        # Get regions defined in evironment variables
        if self.regions:
            config_regions = [region.strip() for region in regions.lower().split(",")]
        else:
            config_regions = ec2_regions
        logging.info(f"Gathering running EC2 instances count for the following regions: {', '.join(config_regions)}")

        # create filter for instances in running state
        filters = [
            {
                'Name': 'instance-state-name', 
                'Values': ['running']
            }
        ]

        total_instances = 0

        for region in config_regions:
            if region not in ec2_regions:
                logging.critical(
                    f"The region '{region}' is not a valid region for EC2. "
                    "Please check AWS_REGIONS environment variable. Continuing..."
                )
                continue
            logging.debug(f"Getting EC2 instances for {region}")
            ec2_conn = session.resource("ec2", region_name=region)
            try:
                instance_count = len(list(ec2_conn.instances.filter(Filters=filters)))
            except botocore.exceptions.ClientError as error:
                logging.critical(error)
                logging.critical(f"Unable to get instances for region {region} using the provided credentials.")
                continue
            logging.debug(f"Found {instance_count} running EC2 instances in {region}.")
            total_instances += instance_count
        
        logging.info(f"POLL: Found {total_instances} running EC2 instances across specified regions.")
        self.data = total_instances


if __name__ == "__main__":
    service = RunningEC2PumpService()
    service.start()