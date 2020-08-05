import os
import argparse
import configparser


class MyArgs:

    def __init__(self):
        pass


    def get_args_from_terminal(self):
        self.parser = argparse.ArgumentParser(description="A script used to automatically setup a remote github repository and then setup your local repository with all the things that you require, such as a virtual env, src directory, .gitignore file, etc")
        
        self.parser.add_argument("-l", "--local_repo_only", action="store_true", help="do not create a remote github repository, only create a local repository")
        self.parser.add_argument("-n", "--repository_name", metavar="name", type=str, default=None, help="choose a name for your remote github repository, defaults to name of cwd, note that this requires the --local_repo_only flag not to be used")
        self.parser.add_argument("-d", "--local_directory_path", metavar="path", type=str, default=os.getcwd(), help="choose path to create local repository, defaults to cwd if flag is not specified")
        self.parser.add_argument("--no_venv", action="store_true", help="do not create a venv")
        self.parser.add_argument("--no_docs", action="store_true", help="do not create a docs directory")
        self.parser.add_argument("--no_logs", action="store_true", help="do not create a logs directory")
        self.parser.add_argument("--no_notes", action="store_true", help="do not create a notes directory")
        self.parser.add_argument("--no_src", action="store_true", help="do not create a src directory")
        self.parser.add_argument("--no_tests", action="store_true", help="do not create a tests directory")
        self.parser.add_argument("--no_images", action="store_true", help="do not create an images directory")
        self.parser.add_argument("--no_config", action="store_true", help="do not create a config directory")
        self.parser.add_argument("--no_requirements", action="store_true", help="create a requirements.txt file")
        self.parser.add_argument("--open_vscode", action="store_true", help="open vscode")
        self.parser.add_argument("-g", "--gitignore", type=str, help="choose a gitignore template")
        self.parser.add_argument("-c", "--config", action="store_true", help="use default values from config file (cmd_defaults.ini)")

        self.args = self.parser.parse_args()

        self.args.local_directory_path = os.path.abspath(self.args.local_directory_path)
        if self.args.repository_name == None or self.args.repository_name == "":
            self.generate_repository_name_based_upon_directory_name()


    def get_args_from_config_file_and_overwrite_old_args(self):
        # CONFIG_FILE = "../config/cmd_defaults.ini"
        CONFIG_FILE = "config/cmd_defaults.ini"
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        self.args.local_repo_only = bool(int(config['ARGUMENTS'].get("local_repo_only", self.args.local_repo_only)))
        self.args.no_venv = bool(int(config['ARGUMENTS'].get("no_venv", self.args.no_venv)))
        self.args.no_docs = bool(int(config['ARGUMENTS'].get("no_docs", self.args.no_docs)))
        self.args.no_logs = bool(int(config['ARGUMENTS'].get("no_logs", self.args.no_logs)))
        self.args.no_notes = bool(int(config['ARGUMENTS'].get("no_notes", self.args.no_notes)))
        self.args.no_src = bool(int(config['ARGUMENTS'].get("no_src", self.args.no_src)))
        self.args.no_tests = bool(int(config['ARGUMENTS'].get("no_tests", self.args.no_tests)))
        self.args.no_images = bool(int(config['ARGUMENTS'].get("no_images", self.args.no_images)))
        self.args.no_config = bool(int(config['ARGUMENTS'].get("no_config", self.args.no_config)))
        self.args.open_vscode = bool(int(config['ARGUMENTS'].get("open_vscode", self.args.open_vscode)))
        self.args.no_requirements = bool(int(config['ARGUMENTS'].get("no_requirements", self.args.no_requirements)))
        self.args.gitignore = str(config['ARGUMENTS'].get("gitignore", self.args.gitignore))

        if self.args.gitignore == "": self.args.gitignore = None


    def generate_repository_name_based_upon_directory_name(self):
        if os.path.exists(self.args.local_directory_path):
            path = os.path.abspath(self.args.local_directory_path)
            parent_directory_folder_name = os.path.basename(path)
            parent_directory_folder_name = parent_directory_folder_name.lower().replace(" ", "_")
            self.args.repository_name = parent_directory_folder_name
        else:
            self.args.repository_name = None