from my_args import MyArgs
from project_creator import ProjectCreator


if __name__ == "__main__":
    args = MyArgs()
    args.get_args_from_terminal_and_config_file_in_correct_form()

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
        gitignore=args.args.gitignore,
        open_vscode=args.args.open_vscode
    )

    try:
        project.create_project()
    except Exception as e:
        print(e)