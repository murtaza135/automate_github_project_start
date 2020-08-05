import os
import configparser


class MyGuiOptions:

    def __init__(self):
        # self.GUI_CONFIG_FILE = "../config/gui_defaults.ini"
        self.GUI_CONFIG_FILE = "config/gui_defaults.ini"
        self.config = configparser.ConfigParser()


    def get_default_options_from_config_file(self):
        self.config.read(self.GUI_CONFIG_FILE)

        self.default_options = dict()
        self.default_options["local_repo_only"] = bool(int(self.config['ARGUMENTS'].get("local_repo_only", False)))
        self.default_options["venv"] = bool(int(self.config['ARGUMENTS'].get("venv", True)))
        self.default_options["docs"] = bool(int(self.config['ARGUMENTS'].get("docs", True)))
        self.default_options["logs"] = bool(int(self.config['ARGUMENTS'].get("logs", True)))
        self.default_options["notes"] = bool(int(self.config['ARGUMENTS'].get("notes", True)))
        self.default_options["src"] = bool(int(self.config['ARGUMENTS'].get("src", True)))
        self.default_options["tests"] = bool(int(self.config['ARGUMENTS'].get("tests", True)))
        self.default_options["images"] = bool(int(self.config['ARGUMENTS'].get("images", True)))
        self.default_options["config"] = bool(int(self.config['ARGUMENTS'].get("config", True)))
        self.default_options["requirements"] = bool(int(self.config['ARGUMENTS'].get("requirements", True)))
        self.default_options["gitignore"] = str(self.config['ARGUMENTS'].get("gitignore", "None"))
        self.default_options["open_vscode"] = str(self.config['ARGUMENTS'].get("open_vscode", False))