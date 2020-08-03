import os
import argparse
import configparser


class MyArgs:

    def __init__(self):
        pass


    def get_args_from_terminal(self):
        self.parser = argparse.ArgumentParser(description="A script used to automatically setup a remote github repository and then setup your local repository with all the things that you require, such as a virtual env, src directory, .gitignore file, etc")
        
        self.parser.add_argument("-l", "--local_repo_only", action="store_true", help="do not create a remote github repository, only create a local repository")
        self.parser.add_argument("-n", "--repository_name", metavar="name", type=str, default=type(self).generate_repository_name_based_upon_cwd(), help="choose a name for your remote github repository, defaults to name of cwd, note that this requires the --local_repo_only flag not to be used")
        self.parser.add_argument("-d", "--local_directory_path", metavar="path", type=str, default=os.getcwd(), help="choose path to create local repository, defaults to cwd if flag is not specified")
        self.parser.add_argument("--no_venv", action="store_true", help="do not create a venv")
        self.parser.add_argument("--no_docs", action="store_true", help="do not create a docs directory")
        self.parser.add_argument("--no_logs", action="store_true", help="do not create a logs directory")
        self.parser.add_argument("--no_notes", action="store_true", help="do not create a notes directory")
        self.parser.add_argument("--no_src", action="store_true", help="do not create a src directory")
        self.parser.add_argument("--no_tests", action="store_true", help="do not create a tests directory")
        self.parser.add_argument("--no_requirements", action="store_true", help="create a requirements.txt file")
        self.parser.add_argument("-g", "--gitignore", type=str, help="choose a gitignore template")
        self.parser.add_argument("-c", "--config", type=argparse.FileType('r'), help="enter a config.ini file")

        self.args = self.parser.parse_args()


    def get_args_from_config_file_and_overwrite_old_args(self):
        filename = self.args.config
        config = configparser.ConfigParser()
        config.read_file(filename)

        self.args.local_repo_only = bool(int(config['ARGUMENTS'].get("local_repo_only", self.args.local_repo_only)))
        self.args.repository_name = str(config['ARGUMENTS'].get("repository_name", self.args.repository_name))
        self.args.local_directory_path = str(config['ARGUMENTS'].get("local_directory_path", self.args.local_directory_path))
        self.args.no_venv = bool(int(config['ARGUMENTS'].get("no_venv", self.args.no_venv)))
        self.args.no_docs = bool(int(config['ARGUMENTS'].get("no_docs", self.args.no_docs)))
        self.args.no_logs = bool(int(config['ARGUMENTS'].get("no_logs", self.args.no_logs)))
        self.args.no_notes = bool(int(config['ARGUMENTS'].get("no_notes", self.args.no_notes)))
        self.args.no_src = bool(int(config['ARGUMENTS'].get("no_src", self.args.no_src)))
        self.args.no_tests = bool(int(config['ARGUMENTS'].get("no_tests", self.args.no_tests)))
        self.args.no_requirements = bool(int(config['ARGUMENTS'].get("no_requirements", self.args.no_requirements)))
        self.args.gitignore = str(config['ARGUMENTS'].get("gitignore", self.args.gitignore))


    @staticmethod
    def generate_repository_name_based_upon_cwd():
        parent_directory_folder_name = os.path.basename(os.getcwd())
        parent_directory_folder_name = parent_directory_folder_name.lower().replace(" ", "_")
        return parent_directory_folder_name