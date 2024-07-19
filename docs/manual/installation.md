# Installation

C5-DEC CAD requires Python 3 and Git, the distributed version control system. Once Python is installed, install C5-DEC CAD using one of the following methods.

## Installing C5-DEC CAD via Docker and our scripts

The fastest and most reliable way to deploy and run C5-DEC CAD is to use our already existing Docker definition file, with the build and execution scripts found in the repository.

Simply clone the repository or download a ZIP archive of the project, and then proceed as follows: 

- make sure Docker engine is running;
- unzip the archive, switch to the extracted directory and make the two shell scripts executable, i.e., `chmod +x script-name.sh`;
- run the `build-c5dec.sh` script to build the image;
- run `c5dec.sh` to launch C5-DEC CAD, which by default runs the CLI with no arguments and shows the help menu.

## Installing via pipx and C5-DEC distribution package

While starting from the beta release we strongly recommend the previously described installation method relying on Docker and our scripts, the alternative installation using `pipx` and our distribution package containing a `wheel` file along with dependency assets remains possible. Below we describe how to perform the installation using this approach covering different platforms.

#### Requirements

- [Python 3](https://www.python.org/)
- [git](https://git-scm.com/), the distributed version control system

##### Optional

- [Doorstop](https://github.com/doorstop-dev/doorstop) (recommended to install via `pipx`)

Strictly speaking, a Doorstop installation is not required; nevertheless, we strongly recommend installing Doorstop such that it can be used in combination with C5-DEC CAD. This is mainly due to the fact that the SSDLC module in the current Alpha implementation does not provide a full coverage of the Doorstop API, which is why users may find it easier to carry out certain complementary operations using Doorstop.

###### Installing Doorstop (optional)

To install Doorstop, we recommend the following method using [pipx](https://pypa.github.io/pipx/) as it is rather straightforward. On a GNU/Linux distribution, MacOS or Windows Subsystem for Linux (WSL), simply open a terminal (e.g., bash, Zsh) and execute the following commands:

1. Install `pipx` if not already installed:
```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

2. Once `pipx` is installed, use it to install Doorstop:
```sh
pipx install doorstop==3.0b10
```

#### Installing C5-DEC CAD using the distribution wheel file

1. Unpack the [c5dec-cad-\<release\>.zip](https://github.com/AbstractionsLab/c5dec/releases) distribution;
1. Change working directory to the unpacked folder containing the wheel distribution file (.whl), and use pipx to install C5-DEC CAD. Considering the `<release>` where `release` can be `alpha`, `beta`, etc:

```sh
cd c5dec-cad-<release>
pipx install ./c5dec-<version>-py3-none-any.whl
```

### GNU/Linux

On most modern GNU/Linux distributions Python 3.8 or above comes already preinstalled.

Open a terminal (e.g., bash, Zsh) and execute the following commands:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

#### Install C5-DEC using pipx

Open a terminal and run the following command, assuming that the Wheel distribution file (.whl) is placed in the current directory:
```sh
pipx install ./c5dec-<version>-py3-none-any.whl
```

where <version> can be in the following form: X.Y[.Z], e.g., 0.1, 0.2, 1.0, 1.1.2, 2.0, 2.2.1, etc.

#### Launching C5-DEC

You can start C5-DEC CAD by simply entering “c5dec” in an open terminal, with the current directory being an unpacked copy of the C5-DEC CAD [project folder]().

### MacOS

Install Python 3.8 or above if not already available.

Open a terminal (e.g., bash, Zsh) and execute the following commands:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

#### Install C5-DEC using pipx

Open a terminal and run the following command, assuming that the Wheel distribution file (.whl) is placed in the current directory:

```sh
pipx install ./c5dec-<version>-py3-none-any.whl
```

where <version> can be in the following form: X.Y[.Z], e.g., 0.1, 0.2, 1.0, 1.1.2, 2.0, 2.2.1, etc.

#### Launching C5-DEC

You can start C5-DEC CAD by simply entering “c5dec” in an open terminal, with the current directory being an unpacked copy of the C5-DEC CAD [project folder]().

### Windows

#### Install Python

1. Launch the “Microsoft Store” application from the Windows Start Menu.
1. Search for Python in the Microsoft Store search bar and select Python 3.8, or any version higher than or equal to 3.8 and smaller than Python 3.12.
1. Press the “Get” or “Install” button as shown in the screenshot below.

![Installing Python 3.8 on Windows via Microsoft Store](./_figures/Python3-8-WindowsStore.png)


#### Install pipx

Open a terminal and execute the following commands:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

#### Install C5-DEC using pipx

Open a terminal and run the following command, assuming that the Wheel distribution file (.whl) is placed in the current directory:

```sh
pipx install .\c5dec-<version>-py3-none-any.whl
```

where <version> can be in the following form: X.Y[.Z], e.g., 0.1, 0.2, 1.0, 1.1.2, 2.0, 2.2.1, etc.

You can download the latest distribution file (.whl) from the GitHub repository of C5-DEC CAD.

#### Launching C5-DEC

You can simply start C5-DEC by entering “c5dec” in an open terminal or by double-clicking the “run-c5dec” batch file found in the C5-DEC distribution folder.

### Usage via the pipx installation method

To start C5-DEC CAD through your GNU/Linux/MacOS/WSL terminal, first change your current working directory to the one containing an unpacked copy of the [c5dec-cad-release.zip](https://github.com/AbstractionsLab/c5dec/releases) distribution file. For the sake of this example, we assume that the zip archive is unpacked at the following path `/home/user/c5dec-cad-release`:
```sh
$ cd /home/user/c5dec-cad-release
```
Then, simply enter one command from the options below and press return.
#### Launching C5-DEC CAD command line interface (CLI)

```sh
c5dec -h
```
This would then display the help menu of the CLI, as shown below. You can then choose one of the available subcommands to execute the desired operation.

![C5-DEC CAD CLI](./_figures/c5dec-cli.png)

#### Launching C5-DEC CAD textual user interface (TUI)

```sh
c5dec
```
This would launch the TUI by default, as shown below.

![C5-DEC CAD TUI](./_figures/c5dec-cad-tui.png)

Alternatively, you can also launch the TUI using the `-t` parameter.

```sh
c5dec -t
```

#### Launching C5-DEC CAD graphical user interface (GUI)

```sh
c5dec -g
```
This would launch the GUI by default, as shown below.

![C5-DEC CAD GUI](./_figures/c5dec-cad-gui-cct-browser.png)

## Installation in a containerized development environment

The easiest and recommended way to get a local copy of the development environment up and running is described next. 

### Requirements

The following pieces of software are necessary for setting up the C5-DEC CAD containerized environment.

* A local installation of [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Visual Studio Code](https://code.visualstudio.com/) (VS Code)
* The [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for VS Code by Microsoft

### Installation

1. Clone this repository:
```sh
git clone https://github.com/AbstractionsLab/c5dec.git 
```
2. Start Docker Desktop if not already running;
3. Open the project folder in VS Code;
4. Select the "Reopen in Container" option in the notification that pops up in VS Code. This will create and run the project inside a Docker container; alternatively, the same command for reopening the project in a container can be selected and invoked from the VS Code command palette;

Note that the local file system is automatically mapped to that of the GNU/Linux container.

_**Hint:**_ to resolve warnings in the code related to missing imports, select the Python interpreter installed by poetry. This can be done by clicking on the light bulb that appears next to the warnings.

While this should no longer occur, in the even that a poetry-related error message is observed when launching `c5dec` via the VS Code terminal, use the same terminal instance and run the following command in the GNU/Linux (Ubuntu) container to install all dependencies:

```sh
poetry install
```

### Usage

Once installed, the C5-DEC CAD tool can be launched from the VS Code terminal in any of the three modes of operation (CLI, TUI, GUI). From the project root folder (/home/alab/c5dec), change to the c5dec folder and run the corresponding command as described below:

```sh
cd /home/alab/c5dec/c5dec
```

#### Textual User Interface (TUI)

```sh
poetry run c5dec
```

#### Command Line Interface (CLI)

```sh
$ poetry run c5dec <command>
```
To see the available commands, run:
```sh
poetry run c5dec -h
```

#### Graphical user interface (GUI)

```sh
poetry run c5dec -g
```
or
```sh
poetry run c5dec --gui
```

Alternatively, the tool can be executed from Docker Desktop:

1. In the left-side menu, go to the tab "Containers";
2. Open the container associated to C5-DEC CAD (the image name starts with "vsc-cad");
3. Go to the "Exec" tab;
4. Run the same commands as above.

_**Remark:**_ For a more accessible Common Criteria browsing experience, we recommend using the TUI or the GUI for functionality related to the CCT feature.