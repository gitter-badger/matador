#!/usr/bin/env python
from os import devnull
import logging
import subprocess
import yaml
from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.errors import NotGitRepository
from configparser import ConfigParser
from pathlib import Path

logger = logging.getLogger(__name__)


def get_environments(project_folder):
    file_path = Path(
        project_folder, 'config', 'environments.yml')
    try:
        file = file_path.open('r')
        return yaml.load(file)
    except FileNotFoundError:
        logger.error('Cannot find environments.yml file')


def get_credentials(project_folder):
    file_path = Path(
        project_folder, 'config', 'credentials.yml')
    try:
        file = file_path.open('r')
        return yaml.load(file)
    except FileNotFoundError:
        logger.error('Cannot find credentials.yml file')


def initialise_repository(proj_folder, repo_folder):
    config_file = Path(repo_folder, '.git', 'config')
    config = ConfigParser()

    porcelain.init(str(repo_folder))
    config.read(config_file)

    config['core']['sparsecheckout'] = 'true'
    config['remote "origin"'] = {
        'url': proj_folder,
        'fetch': '+refs/heads/*:refs/remotes/origin/*'
    }

    with open(config_file, 'w') as f:
        f.write(config)
        f.close()

    sparse_checkout_file = Path(
        repo_folder, '.git', 'info', 'sparse-checkout')
    with sparse_checkout_file.open('a') as f:
        f.write('/src\n')
        f.write('/deploy\n')
        f.close()


def project_folder():
    return Path(Repo.discover().index_path()).parents[1]


class Session(object):

    project_folder = None
    environment = None

    @classmethod
    def initialise_session(self):
        if self.project_folder is not None:
            return
        else:
            self.project_folder = project_folder()

            self.project = self.project_folder.name

            self.matador_project_folder = Path(
                Path.home(), '.matador', self.project)

            self.matador_repository_folder = Path(
                self.matador_project_folder, 'repository')

            self.environments = get_environments(self.project_folder)

    @classmethod
    def _initialise_matador_repository(self):
        Path.mkdir(
            self.matador_project_folder, parents=True, exist_ok=True)
        Path.mkdir(
            self.matador_repository_folder, parents=True, exist_ok=True)

        try:
            Repo(str(self.matador_repository_folder))
        except NotGitRepository:
            initialise_repository(
                self.project_folder, self.matador_repository_folder)

    @classmethod
    def set_environment(self, environment):

        if self.environment is not None:
            return
        else:
            self._initialise_matador_repository()
            self.environment = self.environments[environment]
            credentials = get_credentials(self.project_folder)
            self.credentials = credentials[environment]

            self.matador_environment_folder = Path(
                self.matador_project_folder, environment)
            self.matador_tickets_folder = Path(
                self.matador_environment_folder, 'tickets')
            self.matador_packages_folder = Path(
                self.matador_environment_folder, 'packages')

            Path.mkdir(
                self.matador_environment_folder, parents=True, exist_ok=True)
            Path.mkdir(
                self.matador_tickets_folder, parents=True, exist_ok=True)
            Path.mkdir(
                self.matador_packages_folder, parents=True, exist_ok=True)

    @classmethod
    def update_repository(self):
        repo_folder = self.matador_repository_folder

        try:
            subprocess.run(
                ['git', '-C', repo_folder, 'status'],
                stderr=subprocess.STDOUT,
                stdout=open(devnull, 'w'),
                check=True)
        except subprocess.CalledProcessError:
            proj_folder = self.project_folder
            initialise_repository(proj_folder, repo_folder)

        subprocess.run(
            ['git', '-C', repo_folder, 'fetch', '-a'],
            stderr=subprocess.STDOUT,
            stdout=open(devnull, 'w'))
