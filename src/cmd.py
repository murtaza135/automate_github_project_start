from my_args import MyArgs
from project_creator import ProjectCreator


if __name__ == "__main__":
    args = MyArgs()
    args.get_args_from_terminal()

    config_file = args.args.config
    if config_file:
        args.get_args_from_config_file_and_overwrite_old_args()


    project = ProjectCreator(
        local_repo_only=args.args.local_repo_only,
        repository_name=args.args.repository_name,
        local_directory_path=args.args.local_directory_path,
        venv=not(args.args.no_venv),
        docs=not(args.args.no_docs),
        logs=not(args.args.no_logs),
        notes=not(args.args.no_notes),
        src=not(args.args.no_src),
        tests=not(args.args.no_tests),
        images=not(args.args.no_images),
        config=not(args.args.no_config),
        requirements=not(args.args.no_requirements),
        gitignore=args.args.gitignore
    )

    try:
        project.create_project()
    except Exception as e:
        print(e)