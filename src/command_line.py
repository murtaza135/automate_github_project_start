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

    # if args.args.venv:
    #     os.system("python -m venv .venv")

    if args.args.docs:
        print("docs")
        os.system("mkdir docs")

    if args.args.logs:
        print("logs")
        os.system("mkdir logs")

    if args.args.notes:
        print("notes")
        os.system("mkdir notes")

    if args.args.src:
        print("src")
        os.system("mkdir src")

    if args.args.tests:
        print("tests")
        os.system("mkdir tests")

    if args.args.requirements:
        print("requirements")
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