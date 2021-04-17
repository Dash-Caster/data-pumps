# Weather Data Pump Service

An open-source data pump service based on Python that takes an OpenWeatherMap API key, a location name and sends the current temperature at the location as data to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in **minutes** before executing the next pump. (**optional**, *default*: 5)
* **`OWM_API_KEY`**: API key for OpenWeatherMap API. [Click here](https://home.openweathermap.org/users/sign_up) to sign up for one. After signing up, click on API keys to obtain the API key. (**required**)
* **`LOCATION`**: The location for which to pull the weather data, in the format `<city OR country>` or `<city>, <country>`. (**required**, *example*: `Sydney`, `Sydney, Australia`, `Australia`)
* **`TEMP_UNIT`**: The unit to use for temperature for the data pulled. Must be one of `celsius` or `fahrenheit`. (**optional**, *default*: `celsius`)

### Built With

* Python 3.9.1
  * requests
  * pyowm
