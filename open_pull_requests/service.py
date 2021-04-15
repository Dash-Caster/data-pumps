import os
import sys
import logging

try:
    from common.base import BasePumpService
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common.base import BasePumpService

from urllib.parse import urlparse
import github
from github import Github


class GitOpenPullRequestsPumpService(BasePumpService):

    def configure(self):
        git_access_token = os.getenv('GIT_ACCESS_TOKEN')

        git_url = os.getenv('GIT_URL')
        git_api_url = os.getenv('GIT_API_URL')

        if not git_url:
            logging.critical('Required parameter GIT_URL not specified. Aborting...')
            sys.exit(1)

        git_host, git_owner, git_repo = self._parse_git_url(git_url)

        if not git_host:
            logging.critical('Specified parameter GIT_URL not valid. Aborting...')
            sys.exit(1)

        git_args = {}
        if git_access_token:
            git_args['login_or_token'] = git_access_token

        if git_api_url:
            git_args['base_url'] = git_api_url

        g = Github(**git_args)

        if not git_owner:
            logging.critical('Required parameter USER_NAME not specified. Aborting...')
            sys.exit(1)

        try:
            owner = g.get_user(git_owner)
            if owner.type.lower() == 'organization':
                owner = g.get_organization(git_owner)
            self.owner = owner
        except github.UnknownObjectException:
            logging.critical('User specified in USER_NAME parameter not found. Aborting...')
            sys.exit(1)

        if git_repo:
            try:
                self.repo = self.owner.get_repo(git_repo)
            except github.UnknownObjectException:
                logging.critical(
                    f'Repository specified in GIT_URL parameter not found for user {git_owner}. '  \
                    'If the repository is private, please make sure that GIT_ACCESS_TOKEN '  \
                    'parameter is set and valid.'
                )
                logging.critical('Aborting...')
                sys.exit(1)
        else:
            self.repo = None

    @classmethod
    def _parse_git_url(cls, url):
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        git_path = parsed_url.path
        split_git_path = git_path.strip('/').split('/')
        
        try:
            owner = split_git_path[0]
            if len(split_git_path) > 1:
                repo = split_git_path[1]
            else:
                repo = None
        except IndexError:
            logging.critical('Invalid URL specified for GIT_URL parameter. Aborting...')
            sys.exit(1)
        
        return host, owner, repo

    def poll(self):
        if self.repo:
            self.data = int(len(list(self.repo.get_pulls(state='open'))))
        else:
            n_pulls = 0
            for repo in self.owner.get_repos(type='all'):
                n_pulls += len(list(repo.get_pulls(state='open')))
            self.data = n_pulls

if __name__ == "__main__":
    service = GitOpenPullRequestsPumpService()
    service.start()