from my_github import MyGithub
import os


class ProjectCreator:

    def __init__(self, **kwargs):
        self.gh = MyGithub()

        self.local_repo_only = kwargs["local_repo_only"] if "local_repo_only" in kwargs else False
        self.repository_name = kwargs["repository_name"] if "repository_name" in kwargs else None
        self.local_directory_path = kwargs["local_directory_path"] if "local_directory_path" in kwargs else None
        self.no_venv = kwargs["no_venv"] if "no_venv" in kwargs else False
        self.no_docs = kwargs["no_docs"] if "no_docs" in kwargs else False
        self.no_logs = kwargs["no_logs"] if "no_logs" in kwargs else False
        self.no_notes = kwargs["no_notes"] if "no_notes" in kwargs else False
        self.no_src = kwargs["no_src"] if "no_src" in kwargs else False
        self.no_tests = kwargs["no_tests"] if "no_tests" in kwargs else False
        self.no_requirements = kwargs["no_requirements"] if "no_requirements" in kwargs else False
        self.gitignore = kwargs["gitignore"] if "gitignore" in kwargs else None


    def create_project(self):
        if self.local_directory_path and os.path.exists(self.local_directory_path):
            os.chdir(self.local_directory_path)
        else:
            raise Exception("Error: Please provide a valid path to the directory in which you want to create your local repository")

        if self.repository_name:
            self.create_venv_if_user_agrees()
            self.create_docs_dir_if_user_agrees()
            self.create_logs_dir_if_user_agrees()
            self.create_notes_dir_if_user_agrees()
            self.create_src_dir_if_user_agrees()
            self.create_tests_dir_if_user_agrees()
            self.create_requirements_file_if_user_agrees()
            self.create_specified_gitignore_file_if_any()

            # self.init_local_git_repository()
            # self.create_remote_repo_if_user_agrees()
            # self.push_local_repository_to_remote()

        else:
            raise Exception("Error: Please provide a repository name")


    def init_local_git_repository(self):
        os.system(f'echo # {self.repository_name} >> README.md')
        os.system("git init")
        os.system("git add .")
        os.system('git commit -m "initial commit"')


    def create_remote_repo_if_user_agrees(self):
        if not(self.local_repo_only):
            print("creating new remote github repository...")
            self.gh.create_github_repository(self.repository_name)

    
    def push_local_repository_to_remote(self):
        if not(self.local_repo_only):
            os.system(f"git remote add origin https://github.com/{self.gh.user.login}/{self.repository_name}.git")
            os.system("git push -u origin master")


    def create_venv_if_user_agrees(self): # TODO change name to reflect code block
        if not(self.no_venv):
            print("creating venv...")
            os.system("python -m venv .venv")

            with open(".venv.bat", "w") as f:
                f.write("@echo off")
                f.write("\n\n")
                f.write('".venv/Scripts/activate"')

            with open(".venv.sh", "w") as f:
                f.write("#!/bin/bash")
                f.write("\n\n")
                f.write("source .venv/Scripts/activate")


    def create_docs_dir_if_user_agrees(self):
        if not(self.no_docs):
            print("creating docs directory...")
            os.system("mkdir docs")


    def create_logs_dir_if_user_agrees(self):
        if not(self.no_logs):
            print("creating logs directory...")
            os.system("mkdir logs")


    def create_notes_dir_if_user_agrees(self):
        if not(self.no_notes):
            print("creating notes directory...")
            os.system("mkdir notes")


    def create_src_dir_if_user_agrees(self):
        if not(self.no_src):
            print("creating src directory...")
            os.system("mkdir src")


    def create_tests_dir_if_user_agrees(self):
        if not(self.no_tests):
            print("creating tests directory...")
            os.system("mkdir tests")


    def create_requirements_file_if_user_agrees(self):
        if not(self.no_requirements):
            print("creating requirements.txt file...")
            with open("requirements.txt", "w") as f:
                pass


    def create_specified_gitignore_file_if_any(self):
        if self.gitignore:
            gitignore_template = self.gh.get_specific_gitignore_template(self.gitignore)

            if gitignore_template == None:
                print(f"Error: could not find the '{self.gitignore}' gitignore template")

            print("creating .gitignore file...")

            with open(".gitignore", "w") as f:
                f.write(gitignore_template) if gitignore_template != None else None
                f.write("\n\n") if gitignore_template != None else None
                f.write("# extras generated by the 'automate github project start' script\n")
                f.write(".venv.bat\n")
                f.write(".venv.sh\n")