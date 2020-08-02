from github import Github
import os
import argparse
import configparser

token = os.environ.get("automate_github_project_start_token")

def create_github_repo():
    pass
    # gh = Github(token)
    # rate_limit = gh.get_rate_limit()
    # print(rate_limit)

    # user = gh.get_user()
    # repo = user.create_repo("test")


def generate_repo_name_based_upon_cwd():
    parent_directory_folder_name = os.path.basename(os.getcwd())
    parent_directory_folder_name = parent_directory_folder_name.lower().replace(" ", "_")
    return parent_directory_folder_name

def get_args_from_terminal():
    parser = argparse.ArgumentParser(description="A script used to automatically setup a remote github repository and then setup your local repository with all the things that you require, such as a virtual env, src directory, .gitignore file, etc")
    
    parser.add_argument("--no_remote_repo", action="store_true", help="do not create a remote github repository, only create a local repository")
    parser.add_argument("-n", "--repo_name", metavar="name", type=str, default=generate_repo_name_based_upon_cwd(), help="choose a name for your remote github repository, defaults to name of cwd, note that this requires the --no_remote_repo flag not to be used")
    # parser.add_argument("--create_remote_repo", metavar="name", nargs="?", const=generate_repo_name_based_upon_cwd(), help="create a remote repository on github with your given name, if no name is given, it will default to the name of the cwd")
    parser.add_argument("-d", "--local_directory", metavar="path", type=str, default=os.getcwd(), help="create local repository in chosen path, defaults to cwd if flag is not specified")
    parser.add_argument("-v", "--venv", action="store_true", help="create a venv")
    parser.add_argument("--docs", action="store_true", help="create a docs directory")
    parser.add_argument("--logs", action="store_true", help="create a logs directory")
    parser.add_argument("--notes", action="store_true", help="create a notes directory")
    parser.add_argument("--src", action="store_true", help="create a src directory")
    parser.add_argument("--tests", action="store_true", help="create a tests directory")
    parser.add_argument("--requirements", action="store_true", help="create a requirements.txt file")
    parser.add_argument("--gitignore", type=str, help="choose a gitignore template")
    parser.add_argument("-c", "--config", type=argparse.FileType('r'), help="enter a config.ini file")

    args = parser.parse_args()
    return args


def get_args_from_config_file_and_overwrite_old_args(args):
    filename = args.config

    config = configparser.ConfigParser()
    config.read_file(filename)

    args.no_remote_repo = bool(config['ARGUMENTS'].get("no_remote_repo", args.no_remote_repo))
    args.venv = bool(config['ARGUMENTS'].get("venv", args.venv))
    args.docs = bool(config['ARGUMENTS'].get("docs", args.docs))
    args.logs = bool(config['ARGUMENTS'].get("logs", args.logs))
    args.notes = bool(config['ARGUMENTS'].get("notes", args.notes))
    args.src = bool(config['ARGUMENTS'].get("src", args.src))
    args.tests = bool(config['ARGUMENTS'].get("tests", args.tests))
    args.gitignore = str(config['ARGUMENTS'].get("gitignore", args.gitignore))
    args.repo_name = str(config['ARGUMENTS'].get("repo_name", args.repo_name))
    args.local_directory = str(config['ARGUMENTS'].get("local_directory", args.local_directory))

    return args



if __name__ == "__main__":
    args = get_args_from_terminal()
    if args.config:
        args = get_args_from_config_file_and_overwrite_old_args(args)

    print(args.no_remote_repo)
    print(args.venv)
    print(args.docs)
    print(args.logs)
    print(args.notes)
    print(args.src)
    print(args.tests)
    print(args.gitignore)
    print(args.repo_name)
    print(args.local_directory)
    print()