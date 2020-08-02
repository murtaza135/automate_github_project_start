from github import Github
import os

token = os.environ.get("automate_github_project_start_token")


gh = Github(token)
user = gh.get_user()
repo = user.create_repo("test")

