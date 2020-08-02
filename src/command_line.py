from my_args import MyArgs
from my_github import MyGithub
import os




if __name__ == "__main__":
    args = MyArgs()
    args.get_args_from_terminal()
    print(args.args.requirements)

    if args.args.config:
        args.get_args_from_config_file_and_overwrite_old_args()

    if not(args.args.no_remote_repository):
        gh = MyGithub()
        # gh.create_github_repository(args.repository_name)

    if args.args.venv:
        print("creating venv...")
        os.system("python -m venv .venv")
        os.system("touch .venv.bat")
        os.system("touch .venv.sh")

        with open(".venv.bat", "w") as f:
            f.write("@echo off")
            f.write("\n\n")
            f.write('".venv/Scripts/activate"')

        with open(".venv.sh", "w") as f:
            f.write("#!/bin/bash")
            f.write("\n\n")
            f.write("source .venv/Scripts/activate")

    if args.args.docs:
        print("creating docs directory...")
        os.system("mkdir docs")

    if args.args.logs:
        print("creating logs directory...")
        os.system("mkdir logs")

    if args.args.notes:
        print("creating notes directory...")
        os.system("mkdir notes")

    if args.args.src:
        print("creating src directory...")
        os.system("mkdir src")

    if args.args.tests:
        print("creating tests directory...")
        os.system("mkdir tests")

    if args.args.requirements:
        print("creating requirements.txt file...")
        os.system("touch requirements.txt")

    # if args.args.gitignore:
    #     gh.get_specific_gitignore_template(args.args.gitignore)













    # print(args.args.no_remote_repository)
    # print(args.args.venv)
    # print(args.args.docs)
    # print(args.args.logs)
    # print(args.args.notes)
    # print(args.args.src)
    # print(args.args.tests)
    # print(args.args.gitignore)
    # print(args.args.repository_name)
    # print(args.args.local_directory)
    # print()