# Installation

C5-DEC CAD requires Python 3 and Git, the distributed version control system. Once Python is installed, install C5-DEC CAD using one of the following methods.

## Requirements

- [Python 3](https://www.python.org/)
- [git](https://git-scm.com/), the distributed version control system

### Optional

- Doorstop (recommended to install via `pipx`)

Strictly speaking, a Doorstop installation is not required; nevertheless, we strongly recommend installing Doorstop such that it can be used in combination with C5-DEC CAD. This is mainly due to the fact that the SSDLC module in the current implementation of C5-DEC CAD does not provide a full coverage of the Doorstop API, which is why users may find it easier to carry out certain complementary operations using Doorstop.

To install Doorstop, we recommend the following method using [pipx](https://pypa.github.io/pipx/) as it is rather straightforward. Once `pipx` is installed, simply run the following command:
```sh
$ pipx install doorstop==3.0b10
```

## GNU/Linux

On most modern GNU/Linux distributions Python 3.8 or above comes already preinstalled.

Open a terminal (e.g., bash, Zsh) and execute the following commands:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

### Install C5-DEC using pipx

Open a terminal and run the following command, assuming that the Wheel distribution file (.whl) is placed in the current directory:
```sh
pipx install ./c5dec-<version>-py3-none-any.whl
```

where <version> can be in the following form: X.Y[.Z], e.g., 0.1, 0.2, 1.0, 1.1.2, 2.0, 2.2.1, etc.

### Launching C5-DEC

You can start C5-DEC CAD by simply entering “c5dec” in an open terminal, with the current directory being an unpacked copy of the C5-DEC CAD [project folder]().

## MacOS

Install Python 3.8 or above if not already available.

Open a terminal (e.g., bash, Zsh) and execute the following commands:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

### Install C5-DEC using pipx

Open a terminal and run the following command, assuming that the Wheel distribution file (.whl) is placed in the current directory:

```sh
pipx install ./c5dec-<version>-py3-none-any.whl
```

where <version> can be in the following form: X.Y[.Z], e.g., 0.1, 0.2, 1.0, 1.1.2, 2.0, 2.2.1, etc.

### Launching C5-DEC

You can start C5-DEC CAD by simply entering “c5dec” in an open terminal, with the current directory being an unpacked copy of the C5-DEC CAD [project folder]().

## Windows

### Install Python

1. Launch the “Microsoft Store” application from the Windows Start Menu.
1. Search for Python in the Microsoft Store search bar and select Python 3.8, or any version higher than or equal to 3.8 and smaller than Python 3.12.
1. Press the “Get” or “Install” button as shown in the screenshot below.

![Installing Python 3.8 on Windows via Microsoft Store](./_figures/Python3-8-WindowsStore.png)


### Install pipx

Open a terminal and execute the following commands:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

### Install C5-DEC using pipx

Open a terminal and run the following command, assuming that the Wheel distribution file (.whl) is placed in the current directory:

```sh
pipx install .\c5dec-<version>-py3-none-any.whl
```

where <version> can be in the following form: X.Y[.Z], e.g., 0.1, 0.2, 1.0, 1.1.2, 2.0, 2.2.1, etc.

You can download the latest distribution file (.whl) from the GitHub repository of C5-DEC CAD.

### Launching C5-DEC

You can simply start C5-DEC by entering “c5dec” in an open terminal or by double-clicking the “run-c5dec” batch file found in the C5-DEC distribution folder.



## Setting up the C5-DEC containerized environment

See the _Getting started_ section in the [README](../../README.md#getting-started) page.