from my_args import MyArgs
from my_github import MyGithub
import os




if __name__ == "__main__":
    args = MyArgs()
    args.get_args_from_terminal()
    gh = MyGithub()

    if args.args.config:
        args.get_args_from_config_file_and_overwrite_old_args()

    if not(args.args.no_remote_repository):
        pass
        # gh.create_github_repository(args.repository_name)

    if args.args.venv:
        os.system("python -m venv .venv")

    if args.args.docs:
        pass
        # create doc dir

    if args.args.logs:
        pass
        # create logs dir

    if args.args.notes:
        pass
        # create notes dir

    if args.args.src:
        pass
        # creates src dir

    if args.args.tests:
        pass
        # create tests dir

    if args.args.requirements:
        pass
        # create requirements.txt

    # if args.args.gitignore:
    #     gh.get_specific_gitignore_template(args.args.gitignore)













    print(args.args.no_remote_repository)
    print(args.args.venv)
    print(args.args.docs)
    print(args.args.logs)
    print(args.args.notes)
    print(args.args.src)
    print(args.args.tests)
    print(args.args.gitignore)
    print(args.args.repository_name)
    print(args.args.local_directory)
    print()