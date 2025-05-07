# Setup

In order to successfully launch C5-DEC CAD, simply unpack the "C5DEC-setup" folder and rename it as you see fit; the folder name does not play a role in the correct execution of C5-DEC CAD, but for the sake of this guide, we assume the folder is simply named "c5dec".

See the [installation page](./installation.md) for details on how to deploy C5-DEC and [use](./start.md) its features.

## Git repository

C5-DEC CAD assumes the presence of an existing git repository within its installation folder (i.e., the unpacked folder). Therefore, please remember to run `git init .` from within the project folder, at the root level of the folder.

## Usage assumptions

For a successful usage of C5-DEC, the following assumptions hold:

- There is a compatible Docker engine/desktop available for your platform.
- There is a single git repository within the unpacked/unzipped C5-DEC folder. You can initialize one using from the project folder: `git init .`
- The poetry environment has been activated upon either connecting to a C5-DEC interactive session (`c5dec.sh session`) or once the project is opened via the `C5-DEC CAD dev container` in VS Code. You can do this using the following command in the terminal: `poetry shell`