# Automate Github Project Start

### Setup:
> git clone "https://github.com/murtaza135/automate_github_project_start.git"
> cd automate_github_project_start
> pip install -r requirements.txt
>
> ###### create environment variables:
> TOKEN from github: automate_github_project_start_token
> add "automate_github_project_start/src" directory to environment path variable

### Usage (cmd):
> The program creates multiple directories and files that may be of use to you
> Type "agps -h" into cmd to get a list of all of the directories and files that the program can create
> If you do not a specific directory or file to be created, type eg. "agps --no_venv"
> A full list is found when you type "agps -h"
> 
> typing "agps" without any flags will create the new project in the current directory, and use the name of the current directory to name the remote repository on github
> typing "agps -n NAME" will call the remote repository on github your chosen name
> typing "agps -d PATH" will create the project on your local machine in the specified path
> typing "agps -l" will only create the project locally on your machine with a git init, but will not create a remote repository on github
> typing "agps -c" will use the config file: config/cmd_defaults.ini to automatically set the arguments by default
> you may set the default values of all args in cmd_defailts.ini to your preference

### Usage (gui):
> run agps_gui.bat or gui.py to open the gui
> change whatever options you wish, then click "create project"
> once the project has finished setting up, you may click the "Open VS Code" button to close the program and open vscode
>
> you may set the default values of all the options in config/gui_defaults.ini