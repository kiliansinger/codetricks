# Scientific plotting with python: jupyter notebooks

## Installation

Install the [jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

To follow the programming tutorials you need to setup a programming environment which I describe in the next section:

## How to setup programming environment on windows and linux

### linux Debian, Ubuntu

use apt packet manager

### osx

install homebrew

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

### windows

Press ``CTRL+R`` and type cmd

```bash
wsl --install
```

![image-20241130193522349](09-Jupyterlab-Programming.assets/image-20241130193522349-1763451353114-101.png)

![image-20241130193559592](09-Jupyterlab-Programming.assets/image-20241130193559592-1763451353114-102.png)

finished:

![image-20241130194012479](09-Jupyterlab-Programming.assets/image-20241130194012479-1763451353114-103.png)

reboot

``CTRL+s`` ubuntu

![image-20241130194408742](09-Jupyterlab-Programming.assets/image-20241130194408742-1763451353114-104.png)

then it will install some stuff and ask for username and password (you can choose freely):

![image-20241130195654596](09-Jupyterlab-Programming.assets/image-20241130195654596-1763451353115-105.png)

then you can start using a linux shell

![image-20241130195816654](09-Jupyterlab-Programming.assets/image-20241130195816654-1763451353115-106.png)

you need to activate virtualization in bios when you get:

![image-20241130194748825](09-Jupyterlab-Programming.assets/image-20241130194748825-1763451353115-107.png)

or if you run it in a hyper-v virtual machine you must run an administrative powershell on the host machine and execute ``Set-VMProcessor -VMName <VMName> -ExposeVirtualizationExtensions $false``

#### Install vscode ws-extension (only for windows)

run vs-code and install wsl-extension if you run it in windows:

![image-20241130201046590](09-Jupyterlab-Programming.assets/image-20241130201046590-1763451353115-108.png)

![image-20241130201032892](09-Jupyterlab-Programming.assets/image-20241130201032892-1763451353115-109.png)

## open terminal and change directory into the helloworld folder

go into the directory:

```bash
cd helloworld
```

now you can just run:

![image-20241130201248601](09-Jupyterlab-Programming.assets/image-20241130201248601-1763451353115-110.png)

if you run it in windows it should open vs-code on the host and show that it is connected to your ubuntu:

![image-20241130203123349](09-Jupyterlab-Programming.assets/image-20241130203123349-1763451353115-111.png)

first open hello.c and install the proposed c/c++ extension.

you can open the terminal inside vs-code and execute the commands as described in the comments of hello.c

you can debug by clicking

![image-20241201190853335](09-Jupyterlab-Programming.assets/image-20241201190853335-1763451353115-112.png)

if things do not work go to  generate debug settings

when you click debug you can set breakpoints by clicking in the boarder and placing a red mark:

![image-20241130213702706](09-Jupyterlab-Programming.assets/image-20241130213702706-1763451353115-113.png)

you can use the arrows to single step through your code.

c++ you need to select g++

![image-20241201142003054](09-Jupyterlab-Programming.assets/image-20241201142003054-1763451353115-114.png)

## Python

for python install the recommended extension

![image-20241130214048668](09-Jupyterlab-Programming.assets/image-20241130214048668-1763451353115-115.png)

![image-20241130214129573](09-Jupyterlab-Programming.assets/image-20241130214129573-1763451353115-116.png)you need to close all ubuntu terminals and reopen it for conda to work

and then continue as described in the comments

## Fortran

for fortran install first install the fortran compiler:

```bash
sudo apt install gfortran gdb
```

and the modern fortran extension:

![image-20241130215130740](09-Jupyterlab-Programming.assets/image-20241130215130740-1763451353115-117.png)

you need to select the cog wheel to install it:

![image-20241130215306868](09-Jupyterlab-Programming.assets/image-20241130215306868-1763451353115-118.png)

and then

![image-20241130215333226](09-Jupyterlab-Programming.assets/image-20241130215333226-1763451353115-119.png)

after installation also install:

![image-20241130215421192](09-Jupyterlab-Programming.assets/image-20241130215421192-1763451353115-120.png)

if that message does not occur or you cannot press the button type this in command line:

```bash
sudo apt install fortls
```

for fortran debugging:

![image-20241130220233271](09-Jupyterlab-Programming.assets/image-20241130220233271-1763451353116-121.png)

## generate debug settings

open hello.c

go to \.vscode\launch.json file and only put this inside:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Fortran (gdb)",
      "type": "cppdbg",
      "request": "launch",
      "preLaunchTask": "gfbuild",
      "program": "${fileDirname}/${fileBasenameNoExtension}",
      "cwd": "${fileDirname}",
      "args": [],
      "environment": [],
      "stopAtEntry": false,
      "externalConsole": false,
      "MIMode": "gdb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for gdb",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ]
    }
  ]
}
```

press the debug triangle with the bug (4th icon on the left)

then start debugging/running:

![image-20241130211912356](09-Jupyterlab-Programming.assets/image-20241130211912356-1763451353116-122.png)

![image-20241201141648558](09-Jupyterlab-Programming.assets/image-20241201141648558-1763451353116-123.png)

generate new launch \.vscode\launch.json settings:

![image-20241201191247884](09-Jupyterlab-Programming.assets/image-20241201191247884-1763451353116-124.png)

then run or debug it:

![image-20241130213504423](09-Jupyterlab-Programming.assets/image-20241130213504423-1763451353116-125.png)

do this for c++ and python also

links:

[https://submit.mit.edu/submit-users-guide/tutorials/tutorial_5.html](https://submit.mit.edu/submit-users-guide/tutorials/tutorial_5.html)
[https://code.visualstudio.com/docs/cpp/config-wsl](https://code.visualstudio.com/docs/cpp/config-wsl)
[https://iraspa.org/blog/visual-studio-code-c-cpp-fortran-with-multiple-source-files/](https://iraspa.org/blog/visual-studio-code-c-cpp-fortran-with-multiple-source-files/)

## Setup specific python environment for multilanguage jupyter notebooks

We want to use the jupyter notebooks not only with python (typical use case) but also with C++, C, Javascript and even Fortran, and thus need to stick with a specific python version (python 3.11) for C++/C (from ROOT/Cern) and Fortran to work. As it is pretty involved to get the Fortran compiler to work on windows, we will keep using Windows subsystem for Linux to simplfy our life on Windows.
Thus open your miniforge prompt and type

### for c/c++

```bash
# Python<=3.11 is needed such that the fortran-magic works. also under wsl
# BUT THIS WAS ALREADY done above
conda config --set channel_priority strict
conda create -c conda-forge --name ROOT root python=3.11.13
conda activate ROOT
pip install ipykernel
```

The following lines are only needed if you want to rename the names of the python environment for the jupyter notebook

```
python -m ipykernel install --user --name ROOT
python -m ipykernel install --user --name ROOT --display-name "Python (py311)"
```

if you also want to run jupyter notebooks in the browser then also do:

```bash
pip install jupyter-notebook
jupyter notebook
```

In order to plot with ROOT from cern that uses c++ you can additionally install [ROOT from cern](https://root.cern/install/all_releases/) (if you work with WSL you need to install the proper Ubuntu Version which you can figure out in WSL with ``cat /etc/issue``)

If you installed root directly in windows (not recommended) then edit C:\root_v6.36.04\etc\notebook\kernels\root\kernel.json.

and write in this file:

```json
{
    "language": "python",
    "display_name": "ROOT python",
    "argv": [
       "C:\\Users\\k\\miniforge3\\envs\\py311\\python.exe",
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}"
        ],
        "env": {
            "PYTHONPATH": "c:\\root_v6.36.04\\bin"
        }
}
```

for all other platforms including wsl on windows no changes are required.

for windows do:

```bash
pip install metakernel
jupyter kernelspec install c:\root_v6.36.04\etc\notebook\kernels\root
```

otherwise do:

```bash
pip install metakernel
#note needed: jupyter kernelspec install ~/miniforge3/envs/ROOT/etc/notebook/kernels/root/
```

### for fortran

```bash
sudo apt install binutils cmake dpkg-dev g++ gcc libssl-dev git libx11-dev \libxext-dev libxft-dev libxpm-dev python3 libtbb-dev libvdt-dev libgif-dev

sudo apt install gfortran libpcre3-dev \
libglu1-mesa-dev libglew-dev libftgl-dev \
libfftw3-dev libcfitsio-dev libgraphviz-dev \
libavahi-compat-libdnssd-dev libldap2-dev \
 python3-dev python3-numpy libxml2-dev libkrb5-dev \
libgsl-dev qtwebengine5-dev nlohmann-json3-dev libmysqlclient-dev \
libgl2ps-dev \
liblzma-dev libxxhash-dev liblz4-dev libzstd-dev
```

Then open the next jupyter notebook [./jupyternotebook/P1.0-Setup.ipynb](./jupyternotebook/P1.0-Setup.ipynb) (under windows you need to start vs-code by ``code .`` from the current folder and select the ROOT python environment.

At the date of writing 19.11.2025 the vscode-notebook-renderers had a bug with javascript. I wrote a Pull Request that should be merged soon. For the impatient ones you can install the extension update from here
[vscode-notebook-renderers fix](./jupyternotebooks/ms-notebook-renderers.vsix)

Go to the extension pane and select the three dots to install it from a local source:


![](09-Jupyterlab-Programming.assets/20251119_152837_image.png)


