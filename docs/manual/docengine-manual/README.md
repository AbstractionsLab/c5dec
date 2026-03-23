# How to compile a C5DEC DocEngine report 

### Prerequisites

#### Containerized development environment

There is nothing to be done if you are using the C5-DEC containerized development environment in VS Code, as described in the setup page.

If you wish to use any other fonts, in the C5-DEC container accessed via the VS Code terminal, simply download the font and add a copy of the `.ttf` files to the `.fonts` folder, stored under the home repository, e.g.,

```sh
cp ./ubuntu-font-family-0.83/*.ttf /home/alab/.fonts/ubuntu/
```

and then run

```sh
fc-cache -fv
```

#### Local non-containerized setup

If you are simply using the C5-DEC DocEngine template locally using your own Quarto installation, please download the [Ubuntu font](https://fonts.google.com/specimen/Ubuntu) and install it on your system. Otherwise, choose another font in the `_quarto.yml` file as the main font.

## Installation (bash/zsh)

### Containerized development environment

Simply activate the poetry environment:

```sh
poetry shell
```

**Note**: Quarto must use the same Python interpreter as the active Poetry environment. If Quarto picks up a different Python, set the `QUARTO_PYTHON` environment variable to the Poetry environment's Python executable. After running `poetry shell`, obtain the path with `which python` and export it:

```sh
export QUARTO_PYTHON=$(which python)
```

then either use the Quarto VS Code extension (Command Palette → `Quarto: Render Document`) or the command line:

```sh
quarto render ./docengine/<name>/index.qmd --to pdf
```

and compile your report as follows

```sh
quarto render ./docengine/end-user-manual/index.qmd --to pdf
```

### Local non-containerized setup

If you are simply using the C5-DEC DocEngine template locally using your own Quarto installation, please proceed as follows.

- Open the project folder in VS Code and open/toggle the lower pane/panel to access the VS Code terminal;
- Create and activate a virtual environment (here 'myenv'):

```sh
python3 -m venv myenv
source myenv/bin/activate
```

Once in the environment, install the requirements stored under `c5dec/assets/etr/etr_template/scripts`:

```sh
pip install -r ./docengine/end-user-manual/scripts/requirements.txt 
```

## Usage

Run the quarto render command:

```sh
quarto render ./docengine/end-user-manual/index.qmd --to pdf
```