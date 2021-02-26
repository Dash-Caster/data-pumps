# Web Scraped Value Pump Service

An open-source data pump service based on Python that scrapes a value from a webpage and sends the scraped value to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in minutes before executing the next pump. (**optional**, *default*: 5)
* **`WEBPAGE_URL`**: The URL of the webpage from where you want to scrape a value. (**required**)
* **`XPATH_SELECTOR`**: The Xpath selector of the element from where the value is to be scraped. (**required**)


**Example:** To scrape number of public commits made by Linus Torvalds on GitHub, set the following: 
```sh
WEBPAGE_URL=https://github.com/search?q=author%3Atorvalds&type=commits
XPATH_SELECTOR=//span[@data-search-type="Commits"]/text()
```

### Built With

* Python 3.9.1
  * requests
  * parsel
