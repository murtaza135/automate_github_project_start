from github import Github
import os


class MyGithub:

    def __init__(self):
        try:
            TOKEN = os.environ.get("automate_github_project_start_token")
            self.gh = Github(TOKEN)
            self.user = self.gh.get_user()
        except:
            raise Exception("Could not connect to Github")


    def create_github_repository(self, repository_name):
        try:
            self.repository = self.user.create_repo(repository_name)
        except:
            raise Exception("Could not create new remote repository on Github")


    @staticmethod
    def get_all_gitignore_templates():
        try:
            gh = Github(timeout=5)
            return gh.get_gitignore_templates()
        except:
            raise Exception("Could not retrieve .gitignore templates from Github")


    @classmethod
    def get_specific_gitignore_template(cls, template_name):
        try:
            gitignore_templates = cls.get_all_gitignore_templates()
        except:
            raise

        for template in gitignore_templates:
            if template.lower() == template_name.lower():
                # this is to make sure that the template is retreived regardless of whether the user used uppercase or lowercase letters
                # as the get_gitignore_template() function below only accepts template names which are EXACTLY the write case
                # eg. get_gitignore_template() accepts 'Python', but not 'python' or 'pyTHOn', etc
                template_name = template
                break
        else:
            raise Exception(f"Could not retrieve the {template_name} .gitignore template from Github")

        try:
            gh = Github(timeout=5)
            return gh.get_gitignore_template(template_name).source
        except:
            raise Exception(f"Could not retrieve the {template_name} .gitignore template from Github")