from github import Github
import os
import argparse

token = os.environ.get("automate_github_project_start_token")

def create_github_repo():
    pass
    # gh = Github(token)
    # rate_limit = gh.get_rate_limit()
    # print(rate_limit)

    # user = gh.get_user()
    # repo = user.create_repo("test")


def generate_repo_name_based_upon_parent_directory():
    # parent_directory_path = os.path.dirname(os.getcwd())
    parent_directory_folder_name = os.path.basename(os.getcwd())
    parent_directory_folder_name = parent_directory_folder_name.lower().replace(" ", "_")
    return parent_directory_folder_name

def get_parent_directory():
    pass


def parse_arguments():
    pass
    parser = argparse.ArgumentParser(description="A script used to automatically setup a remote github repository and then setup your local repository with all the things that you require, such as a virtual env, src directory, .gitignore file, etc")
    # parser.add_argument("--no_remote_repo", action="store_true", help="do not create a remote repository, only create a local repository")
    # parser.add_argument("-n", "--name", )
    parser.add_argument("--create_remote_repo", metavar="name", nargs="?", const=generate_repo_name_based_upon_parent_directory(), help="create a remote repository on github with your given name")

    parser.add_argument("-d", "--local_directory", )


    args = parser.parse_args()





if __name__ == "__main__":
    pass
    parse_arguments()