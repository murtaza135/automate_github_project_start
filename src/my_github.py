from github import Github
import os


class MyGithub:

    def __init__(self):
        token = os.environ.get("automate_github_project_start_token")
        self.gh = Github(token)
        self.user = self.gh.get_user()


    def create_github_repository(self, repository_name):
        self.repository = user.create_repository(repository_name)


    def get_all_gitignore_templates(self):
        return self.gh.get_gitignore_templates()

    
    def get_specific_gitignore_template(self, template_name):
        try:
            gitignore_templates = self.get_all_gitignore_templates()

            for template in gitignore_templates:
                if template.lower() == template_name:
                    template_name = template
                    break

            return self.gh.get_gitignore_template(template_name).source

        except:
            return None