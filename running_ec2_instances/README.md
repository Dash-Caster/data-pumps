# Running EC2 Instances Pump Service

An open-source data pump service based on Python that counts the running AWS EC2 instances running across specified regions and sends the data to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in minutes before executing the next pump. (**optional**, *default*: 5)
* **`AWS_ACCESS_KEY_ID`**: The access key ID of your AWS credentials. (**required**)
* **`AWS_SECRET_ACCESS_KEY`**: The access key secret of your AWS credentials. (**required**)
* **`AWS_REGIONS`**: A comma-separated list of region names for which to gather the count of running EC2 instances. (**optional**, *default*: All regions)


### Built With

* Python 3.9.1
  * boto3
  * requests
