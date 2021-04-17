# Github Open PRs Pump Service

An open-source data pump service based on Python that takes in a Github user, organization, or repository URL and pumps the total number of open PRs as data to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in **minutes** before executing the next pump. (**optional**, *default*: 5)
* **`GIT_URL`**: The URL for a Github user, organization, or repository for which to count the number of open PRs. (**required**, *example*: `https://github.com/Dash-Caster` or `https://github.com/Dash-Caster/data-pumps`)
* **`GIT_ACCESS_TOKEN`**: The personal access token to use for accessing Github. This is required if your specified repository is private, or your specified organization contains private repositories. See [creating a personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) for instructions on how to get one. (**optional**)


### Built With

* Python 3.9.1
  * requests
  * PyGithub
