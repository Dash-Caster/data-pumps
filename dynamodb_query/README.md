# DynamoDB Query Aggregation Pump Service

An open-source data pump service based on Python that aggregates the result of a DynamoDB query and sends the data to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in minutes before executing the next pump. (**optional**, *default*: 5)
* **`AWS_ACCESS_KEY_ID`**: The access key ID of your AWS credentials. (**required**)
* **`AWS_SECRET_ACCESS_KEY`**: The access key secret of your AWS credentials. (**required**)
* **`AWS_REGION`**: The AWS region where your RDS instance is hosted. (**required**)
* **`DYNAMO_OPERATION_MODE`**: The type of operation to perform on the DynamoDB table. (**required**, valid values: `['scan', 'query']`)
* **`DYNAMO_AGGREGATION_MODE`**: The type of aggregation to perform on the query results. (**required**, valid values: `['count', 'sum', 'average']`)
* **`DYNAMO_AGGREGATION_ATTRIBUTE`**: The attribute column on which to perform the aggregation in case of sum or average. (**required** only when `DYNAMO_AGGREGATION_MODE` is `sum` or `average`)

Additional arguments such as `TableName` and `KeyConditionExpression` to be passed to query / scan function are to be defined in `arguments.json` file. More details can be found in AWS API Reference for [query](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html#API_Query_RequestSyntax) and [scan](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html#API_Scan_RequestSyntax) operations, respectively.

### Built With

* Python 3.9.1
  * boto3
  * requests
