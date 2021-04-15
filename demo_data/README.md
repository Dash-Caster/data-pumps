# Demo Data Pump Service

An open-source data pump service based on Python that takes a list of values and sends the values periodically as data to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in **minutes** before executing the next pump. (**optional**, *default*: 5)
* **`VALUE_LIST`**: The comma-separated list of numbers to be pumped periodically. (**required**, *example*: `1,2,3`)


### Built With

* Python 3.9.1
  * requests
