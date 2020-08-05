from my_github import MyGithub
import os
import time


class ProjectCreator:

    def __init__(self, **kwargs):
        self.errors = list()
        self.create_mygithub()
        self.set_all_options(**kwargs)


    def create_mygithub(self):
        try:
            self.gh = MyGithub()
        except Exception as e:
            print(e)
            self.errors.append(e)
            self.gh = None


    def set_all_options(self, **kwargs):
        self.local_repo_only = kwargs["local_repo_only"] if "local_repo_only" in kwargs else False
        self.repository_name = kwargs["repository_name"] if "repository_name" in kwargs and kwargs["repository_name"] != "" else None
        self.local_directory_path = kwargs["local_directory_path"] if "local_directory_path" in kwargs and kwargs["local_directory_path"] != "" else None
        self.venv = kwargs["venv"] if "venv" in kwargs else False
        self.docs = kwargs["docs"] if "docs" in kwargs else False
        self.logs = kwargs["logs"] if "logs" in kwargs else False
        self.notes = kwargs["notes"] if "notes" in kwargs else False
        self.src = kwargs["src"] if "src" in kwargs else False
        self.tests = kwargs["tests"] if "tests" in kwargs else False
        self.images = kwargs["images"] if "images" in kwargs else False
        self.config = kwargs["config"] if "config" in kwargs else False
        self.requirements = kwargs["requirements"] if "requirements" in kwargs else False
        self.gitignore = kwargs["gitignore"] if "gitignore" in kwargs and kwargs["gitignore"] != "" else None
        self.open_vscode = kwargs["open_vscode"] if "open_vscode" in kwargs else False


    def create_project(self):
        if type(self.local_directory_path) == str and os.path.exists(self.local_directory_path):
            os.chdir(self.local_directory_path)
        else:
            raise Exception("Please provide a valid path to the directory in which you want to create your local repository")

        if type(self.repository_name) == str:
            self.create_venv_with_shortcuts_if_user_agrees()
            self.create_docs_dir_if_user_agrees()
            self.create_logs_dir_if_user_agrees()
            self.create_notes_dir_if_user_agrees()
            self.create_src_dir_if_user_agrees()
            self.create_tests_dir_if_user_agrees()
            self.create_images_dir_if_user_agrees()
            self.create_config_dir_if_user_agrees()
            self.create_requirements_file_if_user_agrees()
            self.create_specified_gitignore_file_if_any()

            self.init_local_git_repository()
            self.create_remote_repo_if_user_agrees()
            self.push_local_repository_to_remote()

            self.create_error_txt_file_if_errors_occur()
            self.open_vscode_if_user_agrees()

        else:
            raise Exception("Please provide a repository name")


    def init_local_git_repository(self):
        os.system(f'echo # {self.repository_name} >> README.md')
        os.system("git init")
        os.system("git add .")
        os.system('git commit -m "initial commit"')


    def create_remote_repo_if_user_agrees(self):
        if not(self.local_repo_only):
            print("creating new remote github repository...")
            try:
                self.gh.create_github_repository(self.repository_name)
            except Exception as e:
                print(e)
                self.errors.append(e)
            else:
                time.sleep(1)

    
    def push_local_repository_to_remote(self):
        if not(self.local_repo_only):
            print("pushing local repository to remote Github repository...")
            try:
                os.system(f"git remote add origin https://github.com/{self.gh.user.login}/{self.repository_name}.git")
                os.system("git push -u origin master")
            except:
                error = "Could not push local repository to the remote Github repository"
                print(error)
                self.errors.append(error)


    def create_venv_with_shortcuts_if_user_agrees(self):
        if self.venv:
            print("creating venv...")
            os.system("python -m venv .venv")

            # creating batch and bash file to provide shortcut access to activating venv
            with open(".venv.bat", "w") as f:
                f.write("@echo off")
                f.write("\n\n")
                f.write('".venv/Scripts/activate"')

            with open(".venv.bash", "w") as f:
                f.write("#!/bin/bash")
                f.write("\n\n")
                f.write("source .venv/Scripts/activate")


    def create_docs_dir_if_user_agrees(self):
        if self.docs:
            print("creating docs directory...")
            os.system("mkdir docs")


    def create_logs_dir_if_user_agrees(self):
        if self.logs:
            print("creating logs directory...")
            os.system("mkdir logs")


    def create_notes_dir_if_user_agrees(self):
        if self.notes:
            print("creating notes directory...")
            os.system("mkdir notes")


    def create_src_dir_if_user_agrees(self):
        if self.src:
            print("creating src directory...")
            os.system("mkdir src")


    def create_tests_dir_if_user_agrees(self):
        if self.tests:
            print("creating tests directory...")
            os.system("mkdir tests")


    def create_images_dir_if_user_agrees(self):
        if self.images:
            print("creating images directory...")
            os.system("mkdir images")


    def create_config_dir_if_user_agrees(self):
        if self.config:
            print("creating config directory...")
            os.system("mkdir config")


    def create_requirements_file_if_user_agrees(self):
        if self.requirements:
            print("creating requirements.txt file...")
            with open("requirements.txt", "w") as f:
                pass


    def create_specified_gitignore_file_if_any(self):
        if self.gitignore:
            try:
                gitignore_template = MyGithub.get_specific_gitignore_template(self.gitignore)
            except Exception as e:
                print(e)
                self.errors.append(e)
                gitignore_template = None

            print("creating .gitignore file...")

            with open(".gitignore", "w") as f:
                f.write(f"{gitignore_template}\n") if gitignore_template != None else None
                f.write("# extras generated by the 'automate github project start' script\n")
                f.write(".venv.bat\n")
                f.write(".venv.bash\n")

    
    def open_vscode_if_user_agrees(self):
        if self.open_vscode:
            print("opening vscode...")
            os.system("code .")

    def create_error_txt_file_if_errors_occur(self):
        if len(self.errors) != 0:
            if len(self.errors) == 1:
                print("Warning: An error has occurred in the creation of your project. Please check the 'errors.txt' file.")
            elif len(self.errors) > 1:
                print("Warning: Multiple errors have occurred in the creation of your project. Please check the 'errors.txt' file.")

            with open("errors.txt", "w") as f:
                f.writelines([f"{error}\n" for error in self.errors[:-1]])
                f.write(self.errors[-1])