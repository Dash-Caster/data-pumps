# Current AWS Bill Pump Service

An open-source data pump service based on Python that gets your estimated AWS bill MTD (month-to-date) and sends the data to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in minutes before executing the next pump. (**optional**, *default*: 5)
* **`AWS_ACCESS_KEY_ID`**: The access key ID of your AWS credentials. (**required**)
* **`AWS_SECRET_ACCESS_KEY`**: The access key secret of your AWS credentials. (**required**)
* **`AWS_REGION`**: The AWS region where your RDS instance is hosted. (**required**)
* **`RDS_DB_ARN`**: The ARN of your RDS instance. (**required**)
* **`RDS_DB_SECRET_ARN`**: The ARN of the Secret which contains the credentials of your RDS instance. (**required**)
* **`RDS_DB_NAME`**: The name of the database to be queried that exists in your RDS instance. (**required**)
* **`SQL_STATEMENT`**: The SQL statement which is to be executed to query your RDS database. Ideally this query should return a single value (I.e. single row and single column). (**required**)

* **Note:** Make sure that your RDS database instance has Data API enabled.

### Built With

* Python 3.9.1
  * boto3
  * requests
