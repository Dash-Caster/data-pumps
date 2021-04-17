import os
import sys
import logging
import re

try:
    from common.base import BasePumpService
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common.base import BasePumpService

import jira
from jira import JIRA


class JiraIssuesPumpService(BasePumpService):
    def configure(self):
        jira_url = os.getenv('JIRA_URL')
        jira_username = os.getenv('JIRA_USER')
        jira_token = os.getenv('JIRA_TOKEN')
        try:
            self.jira = JIRA(jira_url, basic_auth=(jira_username, jira_token))
        except jira.exceptions.JIRAError as exc:
            logging.critical('JIRA authentication failed.')
            logging.critical(exc.text)
            sys.exit(1)
        
        self.jira_jql = os.getenv('JIRA_JQL')
        if not self.jira_jql:
            self.jira_jql = ''
            filters = []
            if os.getenv('JIRA_PROJECT'):
                filters.append(self._make_filter('project', os.getenv('JIRA_PROJECT')))
            if os.getenv('JIRA_ISSUE_TYPE'):
                filters.append(self._make_filter('type', os.getenv('JIRA_ISSUE_TYPE')))
            if os.getenv('JIRA_ISSUE_PRIORITY'):
                filters.append(self._make_filter('priority', os.getenv('JIRA_ISSUE_PRIORITY')))
            if os.getenv('JIRA_ISSUE_STATUS'):
                filters.append(self._make_filter('status', os.getenv('JIRA_ISSUE_STATUS')))
            if os.getenv('JIRA_ASSIGNEE'):
                filters.append(self._make_filter('assignee', os.getenv('JIRA_ASSIGNEE')))
            self.jira_jql = ' AND '.join(filters)
        
        if self.jira_jql:
            try:
                self.jira.search_issues(self.jira_jql, maxResults=1, validate_query=True)  # Validate user-provided JQL
            except jira.exceptions.JIRAError as exc:
                logging.critical(exc.text)
                logging.critical(f'Failed to validate JQL query: {self.jira_jql}')
                sys.exit(1)
        
        logging.info('JQL query:')
        logging.info(self.jira_jql)

    @classmethod
    def _make_filter(cls, key, value):
        values = [v.strip() for v in value.split(',') if v.strip()]
        values = map(lambda value: f"'{value}'" if not cls._is_function_call(value) else value, values)
        return f"{key} IN ({', '.join(values)})"

    @classmethod
    def _is_function_call(cls, s):
        fn_re = r'^([\s\n\r]*[\w]+)[\s\n\r]*(?=\(.*\))'
        return bool(re.match(fn_re, s))

    def poll(self):
        logging.debug(f"Using JQL query: {self.jira_jql}")
        issues = self.jira.search_issues(self.jira_jql, maxResults=0, fields='id')  # Get all results with minimum fields
        self.data = len(issues)


if __name__ == "__main__":
    service = JiraIssuesPumpService()
    service.start()
