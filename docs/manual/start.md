# Quick start

In order to launch the application, either type “c5dec” in the terminal or if you are using Windows, simply double-click the “run-c5dec” batch file found in the distribution folder.

Users can interact with C5-DEC CAD through three different interfaces, namely a native textual user interface (TUI) and command line interface (CLI) provided by C5-DEC CAD, along with various graphical user interfaces (GUI) such as VS Code, any web browser (Mozilla Firefox, Google Chrome, etc.) or Zettlr.

By design, C5-DEC CAD uses open data formats and specifications, thereby allowing the use of a wide range of already existing open-source tools. For instance, by building on top of open-source solutions such as doorstop and pandoc and non-proprietary data storage formats such as YAML, Markdown, LaTeX, PlantUML, JSON, csv, etc. project files maintained and processed using C5-DEC CAD can be also edited, formatted, exported and viewed using existing tools such as web browsers and VS Code.

## TUI: Textual User Interface

Most of the features of C5-DEC CAD are currently exposed via its TUI. To launch the TUI, simply either run the `c5dec` command from the terminal or if you are using Windows, double-click the “run-c5dec” batch file.

This would launch the TUI front-end, shown below.

![C5-DEC CAD TUI](./_figures/c5dec-cad-tui.png)

### Navigating the TUI

You can navigate the TUI and move between menus and submenus using the mouse or the keyboard as follows:

- Arrow keys (left, down, up, right): to change the current selection, i.e., for menus, buttons, text fields, etc.
- Tab key: to hop from one widget or visual object to another, e.g., in the CCT browser, to move the focus from the explorer to other buttons
- Enter key: press enter/return to confirm the current selection

## CLI: Command Line Interface

To run the CLI, simply append the command (and subcommands) to the C5-DEC launch command. You can access the help/manual of the CLI by using the -h parameter.

```sh
c5dec -h
```

This would print out a help menu similar to the one shown below.

![C5-DEC CAD CLI](./_figures/c5dec-cli.png)

## GUI: Graphical User Interface

While there may be many GUI candidates, we recommend the following options:

### Visual Studio Code

The popular, open-source and lightweight source code editor [Visual Studio (VS) Code](https://code.visualstudio.com/) by Microsoft is a natural candidate when it comes to choosing a graphical front-end. This is largely motivated by the following observations:

- Highly extensible: The VS Code Extensions feature allows it to provide dedicated support for several features of C5-DEC CAD, e.g., Markdown and YAML editing, linters, diagramming plugins
- Built-in source control support for git
- Built-in Markdown viewers
- Official extension by Microsoft for containerized development, making further development of C5-DEC CAD quite straightforward given the already existing configuration files provided by the C5-DEC CAD repository

The screenshot below provides an example of how VS Code can be used to enhance the C5-DEC experience: the project files processed using C5-DEC CAD are easily accessible and can be navigated via the VS Code explorer, documentation in Markdown previewed by the viewer on the right and an instance of C5-DEC CAD itself executed and running through the VS Code terminal, allowing the user to make changes using VS Code tools and extensions together with C5-DEC CAD.

![C5-DEC CAD enhanced usage through VS Code](./_figures/c5dec-cad-vscode-gui.png)

### Zettlr

While there are many knowledge-base management and note taking tools using Markdown as the underlying storage format, we recommend [Zettlr](https://www.zettlr.com/) due to its being entirely open source and integration with other technologies and formats being central to C5-DEC, namely its integration of pandoc powering its import and export features and support for LaTeX and linking capabilities.

![C5-DEC CAD Markdown, knowledge-base maintenance and export via Zettlr](./_figures/c5dec-cad-zettlr-gui.png)


Thanks to its native usage of pandoc, Zettlr can provide a more accessible interface for converting and exporting to various formats such as LaTeX, docx,etc.

### Firefox

While any web browser can be used to view the published outcomes of C5-DEC CAD, which in turn invokes the native publishing command of doorstop, we recommend Mozilla Firefox.