import os
import argparse
import configparser


class MyArgs:

    def __init__(self):
        pass


    def get_args_from_terminal(self):
        self.parser = argparse.ArgumentParser(description="A script used to automatically setup a remote github repository and then setup your local repository with all the things that you require, such as a virtual env, src directory, .gitignore file, etc")
        
        self.parser.add_argument("--no_remote_repository", action="store_true", help="do not create a remote github repository, only create a local repository")
        self.parser.add_argument("-n", "--repository_name", metavar="name", type=str, default=type(self).generate_repository_name_based_upon_cwd(), help="choose a name for your remote github repository, defaults to name of cwd, note that this requires the --no_remote_repository flag not to be used")
        self.parser.add_argument("-d", "--local_directory", metavar="path", type=str, default=os.getcwd(), help="create local repository in chosen path, defaults to cwd if flag is not specified")
        self.parser.add_argument("-v", "--venv", action="store_true", help="create a venv")
        self.parser.add_argument("--docs", action="store_true", help="create a docs directory")
        self.parser.add_argument("--logs", action="store_true", help="create a logs directory")
        self.parser.add_argument("--notes", action="store_true", help="create a notes directory")
        self.parser.add_argument("--src", action="store_true", help="create a src directory")
        self.parser.add_argument("--tests", action="store_true", help="create a tests directory")
        self.parser.add_argument("--requirements", action="store_true", help="create a requirements.txt file")
        self.parser.add_argument("--gitignore", type=str, help="choose a gitignore template")
        self.parser.add_argument("-c", "--config", type=argparse.FileType('r'), help="enter a config.ini file")

        self.args = parser.parse_args()


    def get_args_from_config_file_and_overwrite_old_args(self):
        filename = self.args.config
        config = configparser.ConfigParser()
        config.read_file(filename)

        self.args.no_remote_repository = bool(config['ARGUMENTS'].get("no_remote_repository", self.args.no_remote_repository))
        self.args.venv = bool(config['ARGUMENTS'].get("venv", self.args.venv))
        self.args.docs = bool(config['ARGUMENTS'].get("docs", self.args.docs))
        self.args.logs = bool(config['ARGUMENTS'].get("logs", self.args.logs))
        self.args.notes = bool(config['ARGUMENTS'].get("notes", self.args.notes))
        self.args.src = bool(config['ARGUMENTS'].get("src", self.args.src))
        self.args.tests = bool(config['ARGUMENTS'].get("tests", self.args.tests))
        self.args.gitignore = str(config['ARGUMENTS'].get("gitignore", self.args.gitignore))
        self.args.repository_name = str(config['ARGUMENTS'].get("repository_name", self.args.repository_name))
        self.args.local_directory = str(config['ARGUMENTS'].get("local_directory", self.args.local_directory))


    @staticmethod
    def generate_repository_name_based_upon_cwd():
        parent_directory_folder_name = os.path.basename(os.getcwd())
        parent_directory_folder_name = parent_directory_folder_name.lower().replace(" ", "_")
        return parent_directory_folder_name