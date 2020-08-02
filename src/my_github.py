from github import Github
import os


class MyGithub:

    def __init__(self):
        pass


    def create_github_repository(self, repository_name):
        token = os.environ.get("automate_github_project_start_token")

        self.gh = Github(token)

        self.user = gh.get_user()
        self.repository = user.create_repository(repository_name)


    @staticmethod
    def get_all_gitignore_templates():
        return Github.get_gitignore_templates()


    @staticmethod
    def get_specific_gitignore_template(template_name):
        return Github.get_gitignore_template(template_name)