# C5-DEC CAD

C5-DEC, short for "Common Criteria for Cybersecurity, Cryptography, Clouds – Design, Evaluation and Certification", is a sub-project of the [CyFORT](https://abstractionslab.com/index.php/research/) project, which in turn stands for "Cloud Cybersecurity Fortress of Open Resources and Tools for Resilience". 

<img src="./docs/manual/_figures/CyFORT-logo.png" alt="cyfort_logo" width="400"/>

C5-DEC CAD, the software component of C5-DEC, is a suite of tools for computer-aided design and development (CAD), mainly dealing with: the creation and evaluation of secure IT systems according to the [Common Criteria](https://www.commoncriteriaportal.org) standards, secure software development life cycle (SSDLC), and what we refer to as cyber-physical system security assessment (CPSSA).

This repository contains the source code and full documentation (requirements, technical specifications, user manual, test case specifications and test reports) of C5-DEC CAD, exemplifying the C5-DEC method, which relies on storing, interlinking and processing all software development life cycle (SDLC) artifacts in a unified manner.

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [User manual](#user-manual)
- [Getting started](#getting-started)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

## Overview

The overall goal of the C5-DEC method is to bring together and contextualize SSDLC and CPSSA within the Common Criteria framework. This means tackling the problem of building secure systems, while ensuring full traceability between system artifacts spanning the entire DLC and incorporating threat modelling and system security risk assessment into the design process, all in the context of the Common Criteria framework. 

To this end, C5-DEC CAD is aimed at assisting both system/software designers/developers as well as system security analysts with creating and evaluating secure software systems. For instance, it can be used by evaluation laboratories for the execution of impartial assessments of the security of computer systems and software according to the Common Criteria (CC), a set of internationally recognized standards (ISO/IEC 15408), and the complementary ISO/IEC 18045, dealing with a common methodology for computer security evaluation (CEM). CC certification gives users the assurance that a product satisfies the security guarantees and properties it claims to possess.

C5-DEC consists of two key elements that complement each other to form a coherent ensemble: a software component (C5-DEC CAD) and a knowledge base consisting of SSDLC and CPSSA methodologies as well as a [wiki of key CC concepts](./c5dec/assets/database/KnowledgeBase/0_MapofContent.md).

## Features

- Free/libre and open source;
- Cross platform: works on GNU/Linux, MacOS and Windows;
- Easily and highly extensible due to a modular design and architecture;
- Advanced and extensible textual user interface (TUI), powered by the open-source [asciimatics](https://github.com/peterbrittain/asciimatics) framework;
- A command-line interface (CLI) for more efficient user interactions and scripting (currently in prerelease stage);
- A comprehensive [Common Criteria](https://www.commoncriteriaportal.org) Toolbox (CCT), with a focus on efficient browsing of the CC database, creating and processing evaluation checklists, including
   - all baseline CC Security Functional Requirements (SFR) and Security Assurance Requirements (SAR);
   - built-in capabilities for assisting the process of generating technical evaluation reports (ETR), and
   - a [CC wiki](./c5dec/assets/database/KnowledgeBase/0_MapofContent.md) capturing the key concepts of Common Criteria.
- Tools for enhancing secure software development life cycle (SSDLC), powered by the open-source [Doorstop](https://github.com/doorstop-dev/doorstop) tool;
- An object-oriented model and implementation of CC concepts, with the CC database serialized and stored via Doorstop;
- Based on open data formats such as Markdown, (La)TeX, YAML, XML, JSON, CSV and HTML;
- Straightforward integration into well-known Dev(Sec)Ops platforms such as GitHub and GitLab;
- Project (resource) management functionality;
- Import/export from and to open data formats;
- Cryptography-related functionality aimed at improving SSDLC (currently not implemented, but on the roadmap and planned for [future releases](./docs/manual/cryptography.md));
- Software coupled with reports describing methods for
   - Cyber-Physical System Security Assessment (CPSSA) and related functionality (see [CPSSA](./docs/manual/cpssa.md)), and
   - Secure software development life cycle (see [SSDLC](./docs/manual/ssdlc.md)).

## User manual

Please see the [CAD user manual](./docs/manual/overview.md) to learn more about the installation, setup requirements, overall usage and specific modules of C5-DEC CAD.

## Getting Started

C5-DEC CAD can be deployed using any of the following methods:

- Installation via [pipx](https://pypa.github.io/pipx/) using the official distribution file, accessible through the [releases page](https://github.com/AbstractionsLab/c5dec/releases) (recommended for end-users);
- Installation in a containerized environment (recommended for developers);
- Installation via the official PyPI repository (**currently not available, coming soon**).

### Installing C5-DEC CAD via pipx

#### Requirements

- [Python 3](https://www.python.org/)
- [git](https://git-scm.com/), the distributed version control system

##### Optional

- [Doorstop](https://github.com/doorstop-dev/doorstop) (recommended to install via `pipx`)

Strictly speaking, a Doorstop installation is not required; nevertheless, we strongly recommend installing Doorstop such that it can be used in combination with C5-DEC CAD. This is mainly due to the fact that the SSDLC module in the current Alpha implementation does not provide a full coverage of the Doorstop API, which is why users may find it easier to carry out certain complementary operations using Doorstop.

To install Doorstop, we recommend the following method using [pipx](https://pypa.github.io/pipx/) as it is rather straightforward. On a GNU/Linux distribution, MacOS or Windows Subsystem for Linux (WSL), simply open a terminal (e.g., bash, Zsh) and execute the following commands:

1. Install `pipx` if not already installed:
```sh
$ python3 -m pip install --user pipx
$ python3 -m pipx ensurepath
```

2. Once `pipx` is installed, use it to install Doorstop:
```sh
$ pipx install doorstop==3.0b10
```

#### Installing C5-DEC CAD using the distribution wheel file

1. Unpack the [c5dec-cad-alpha.zip](https://github.com/AbstractionsLab/c5dec/releases) distribution;
1. Change working directory to the unpacked folder containing the wheel distribution file (.whl), and use pipx to install C5-DEC CAD:

```sh
$ cd c5dec-cad-alpha
$ pipx install ./c5dec-0.1-py3-none-any.whl
```

#### Launching C5-DEC CAD

To start C5-DEC CAD through your GNU/Linux/MacOS/WSL terminal, first change your current working directory to the one containing an unpacked copy of the [c5dec-cad-alpha.zip](https://github.com/AbstractionsLab/c5dec/releases) distribution file, and then simply enter “c5dec” and press return. For the sake of this example, we assume that the zip archive is unpacked at the following path `/home/user/c5dec-cad-alpha`:

```sh
$ cd /home/user/c5dec-cad-alpha
$ c5dec
```
This would then launch the TUI by default, as shown below.

![C5-DEC CAD TUI](./docs/manual/_figures/c5dec-cad-tui.png)

For more details and learning how to install C5-DEC CAD on Windows without using WSL, see the [Installation](./docs/manual/installation.md) page of the user manual.

### Installation in a containerized environment

The easiest and recommended way to get a local copy of the development environment up and running is described next.

#### Requirements

The following pieces of software are necessary for setting up the C5-DEC CAD containerized environment.

* A local installation of [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Visual Studio Code](https://code.visualstudio.com/) (VS Code)
* The [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for VS Code by Microsoft

#### Installation

1. Clone this repository:
```sh
$ git clone https://github.com/AbstractionsLab/c5dec.git 
```
2. Start Docker Desktop if not already running;
3. Open the project folder in VS Code;
4. Select the "Reopen in Container" option in the notification that pops up in VS Code. This will create and run the project inside a Docker container; alternatively, the same command for reopening the project in a container can be selected and invoked from the VS Code command palette;
4. Open a terminal in VS Code and run the following command in the GNU/Linux (Ubuntu) container to install all dependencies:
```sh
$ poetry install
```

Note that the local file system is automatically mapped to that of the Ubuntu container.

_**Hint:**_ to resolve warnings in the code related to missing imports, select the Python interpreter installed by poetry. This can be done by clicking on the light bulb that appears next to the warnings.

## Usage

The C5-DEC CAD tool has two modes of operation: a textual user interface (TUI) and a command line interface (CLI).

### Textual User Interface

Once installed, the C5-DEC CAD tool can be launched from the VS Code terminal as follows:

```sh
$ cd c5dec/c5dec
$ poetry run c5dec
```

Alternatively, the tool can be executed from Docker Desktop:

1. In the left-side menu, go to the tab "Containers";
2. Open the container associated to C5-DEC CAD (the image name starts with "vsc-cad");
3. Go to the "Exec" tab;
4. Run the same commands as above.

### Command Line Interface
In a VS Code (or Docker Desktop) terminal run:

```sh
$ cd c5dec/c5dec
$ poetry run c5dec <command>
```
To see the available commands, run:
```sh
$ poetry run c5dec -h
```

_**Disclaimer:**_ For the moment, we recommend using the TUI for functionality related to the CCT module. This note will be updated as soon as a stable version of the CLI for the referred module becomes available.

## Roadmap

For details on our roadmap and features planned for future releases, please see the [Wiki](https://github.com/AbstractionsLab/c5dec/wiki) section of this repository.

## License

Copyright (c) itrust Abstractions Lab and itrust consulting. All rights reserved.

Licensed under the [GNU Affero General Public License (AGPL) v3.0](LICENSE) license.

## Contact

If you wish to learn more about the project, feel free to contact us at Abstractions Lab: info@abstractionslab.lu