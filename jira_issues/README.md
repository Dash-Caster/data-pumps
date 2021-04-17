# JIRA Issues Pump Service

An open-source data pump service based on Python that counts the number of JIRA issues filtered by the configured criteria and sends it to a DashCaster widget.


### Configuration

The configration variables are defined in the `.env` file. This service supports the following configuration variables:

#### Required
* **`EDITOR_ID`**: The Editor ID of your DashCaster board where you want to broadcast the data. (**required**)
* **`DATA_ID`**: The Data ID of your DashCaster widget where you want to broadcast the data. (**required**)
* **`POLL_INTERVAL`**: The waiting interval after each pump in **minutes** before executing the next pump. (**optional**, *default*: 5)
* **`JIRA_URL`**: The URL to your JIRA server. (**required**, *example*: `https://companyname.atlassian.net`)
* **`JIRA_USER`**: The username to use for JIRA. (**required**)
* **`JIRA_TOKEN`**: An API token generated for the user specified in `JIRA_USER`. See [Create an API Token](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/#APItokens-CreateanAPItoken) for instructions on how to get one. (**required**)

#### Optional
* **`JIRA_ISSUE_STATUS`**: The status or statuses by which you want to filter JIRA issues. Separate multiple values by a comma. (**optional**, *example*: `in progress, backlog` or `done`, *default*: All statuses)
* **`JIRA_ISSUE_TYPE`**: The status or statuses by which you want to filter JIRA issues. Separate multiple values by a comma. (**optional**, *example*: `in progress, backlog` or `done`, *default*: All statuses)
* **`JIRA_ISSUE_PRIORITY`**: The status or statuses by which you want to filter JIRA issues. Separate multiple values by a comma. (**optional**, *example*: `in progress, backlog` or `done`, *default*: All statuses)
* **`JIRA_ASSIGNEE`**: The assignee(s) by whom you want to filter JIRA issues. Separate multiple values by a comma. (**optional**, *example*: `Jim` or `currentUser(), John, Simon`, *default*: All users)
* **`JIRA_PROJECT`**: The project(s) by which you want to filter JIRA issues. Separate multiple values by a comma. (**optional**, *example*: `DASH` or `PROJ1, PROJ2`, *default*: All projects)

#### Advanced
* **`JIRA_JQL`**: A JIRA JQL query for advanced filtering of JIRA issues. Overrides any and all values specified by `JIRA_ISSUE_STATUS`, `JIRA_ISSUE_TYPE`, `JIRA_ISSUE_PRIORITY`, `JIRA_ASSIGNEE`, and `JIRA_PROJECT` parameters. (**optional**, *example*: `assignee != currentUser() and status NOT IN ('backlog', 'done')`, *default*: Empty JQL query)

### Built With

* Python 3.9.1
  * requests
  * jira-python
