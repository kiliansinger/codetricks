#install with:
# linux/win     sudo apt update
#               sudo apt install curl
#               curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
#               bash Miniforge3-$(uname)-$(uname -m).sh
#                  accept and say yes to everything...
#                  ...
#                  Do you wish to update your shell profile to automatically initialize conda?
#                  This will activate conda on startup and change the command prompt when activated.
#                  If you'd prefer that conda's base environment not be activated on startup,
#                  run the following command when conda is activated:
#                  conda config --set auto_activate_base false
#                  You can undo this by running `conda init --reverse $SHELL`? [yes|no]
#                  [no] >>> yes
# you need to close the terminal and reopen it for conda to work
#osx:           brew install --cask miniforge
#               conda create -n exp3 python=3.12.0
#activate:      conda activate exp3
#run:           python3 hello.py

print("Hello World!")