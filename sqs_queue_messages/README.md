# SQS Messages Count Pump Service

An open-source data pump service based on Python that counts the number of messages in an SQS message queue and sends the data to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in minutes before executing the next pump. (**optional**, *default*: 5)
* **`AWS_ACCESS_KEY_ID`**: The access key ID of your AWS credentials. (**required**)
* **`AWS_SECRET_ACCESS_KEY`**: The access key secret of your AWS credentials. (**required**)
* **`AWS_REGION`**: The region where your SQS queue is hosted. (**required**)
* **`SQS_QUEUE_NAME`**: The name of your SQS queue for which you want to count the number of messages. (**required**)

### Built With

* Python 3.9.1
  * boto3
  * requests
