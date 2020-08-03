from github import Github
import os


class MyGithub:

    def __init__(self):
        token = os.environ.get("automate_github_project_start_token")
        self.gh = Github(token)
        self.user = self.gh.get_user()


    def create_github_repository(self, repository_name):
        self.repository = self.user.create_repo(repository_name)


    def get_all_gitignore_templates(self):
        return self.gh.get_gitignore_templates()

    
    def get_specific_gitignore_template(self, template_name):
        gitignore_templates = self.get_all_gitignore_templates()

        for template in gitignore_templates:
            if template.lower() == template_name.lower():
                # this is to make sure that the template is retreived regardless of whether the user used uppercase or lowercase letters
                # as the get_gitignore_template() function below only accepts template names which are EXACTLY the write case
                # eg. get_gitignore_template() accepts 'Python', but not 'python' or 'pyTHOn', etc
                template_name = template
                break
        else:
            template_name = None

        if template_name:
            return self.gh.get_gitignore_template(template_name).source
        else:
            return None