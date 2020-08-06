import os
import configparser


class MyGuiOptions:

    def __init__(self):
        self.GUI_CONFIG_FILE = "../config/gui_defaults.ini"
        self.config = configparser.ConfigParser()


    def get_default_options_from_config_file(self):
        self.config.read(self.GUI_CONFIG_FILE)

        self.default_options = dict()
        self.default_options["local_repo_only"] = bool(int(self.config['DEFAULTS'].get("local_repo_only", False)))
        self.default_options["venv"] = bool(int(self.config['DEFAULTS'].get("venv", True)))
        self.default_options["docs"] = bool(int(self.config['DEFAULTS'].get("docs", True)))
        self.default_options["logs"] = bool(int(self.config['DEFAULTS'].get("logs", True)))
        self.default_options["notes"] = bool(int(self.config['DEFAULTS'].get("notes", True)))
        self.default_options["src"] = bool(int(self.config['DEFAULTS'].get("src", True)))
        self.default_options["tests"] = bool(int(self.config['DEFAULTS'].get("tests", True)))
        self.default_options["images"] = bool(int(self.config['DEFAULTS'].get("images", True)))
        self.default_options["config"] = bool(int(self.config['DEFAULTS'].get("config", True)))
        self.default_options["requirements"] = bool(int(self.config['DEFAULTS'].get("requirements", True)))
        self.default_options["gitignore"] = str(self.config['DEFAULTS'].get("gitignore", "None"))
        self.default_options["open_vscode"] = str(self.config['DEFAULTS'].get("open_vscode", False))

    @staticmethod
    def generate_name_based_upon_directory_name(directory_path):
        parent_directory_folder_name = os.path.basename(directory_path)
        parent_directory_folder_name = parent_directory_folder_name.lower().replace(" ", "_")
        return parent_directory_folder_name