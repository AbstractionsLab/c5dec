# Setup

In order to successfully launch C5-DEC CAD, simply unpack the "C5DEC-setup" folder and rename it as you see fit; the folder name does not play a role in the correct execution of C5-DEC CAD, but for the sake of this guide, we assume the folder is simply named "c5dec". 

The unzipped archive comes with an "assets" folder containing:
- a series of configuration files
- a Common Criteria wiki
- the entire Common Criteria data stored in dedicated YAML files, with the content encoded in Markdown and all these files being in turn managed by doorstop under the hood.

For the current Alpha release, the user is expected to launch the `c5dec` command from within the unpacked folder, i.e., changing directory to the unpacked (and possibly renamed) folder and then running the `c5dec` command. 

We intend to add an installer in a future release to automate the above mentioned steps.

## Git repository

C5-DEC CAD assumes the presence of an existing git repository within its installation folder (i.e., the unpacked folder). For convenience, we include an already prepared repository that comes with the same zip archive.

## Usage assumptions

For the Alpha version of the C5-DEC release, the following assumptions hold:

- There is a single git repository within the C5-DEC CAD installation folder.