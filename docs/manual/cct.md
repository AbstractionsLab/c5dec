# Common Criteria Toolbox

The Common Criteria Toolbox (CCT) submodule serves as another integrated mini-app within C5-DEC, encompassing a comprehensive suite of functionalities designed to streamline the Common Criteria certification process for both developers and evaluators. Central to the CCT's functionality is the CC database (CC-DB), a dedicated database housing the CC in a structured format that is parsed and deserialized from the XML files sourced from the [Common Criteria portal](https://commoncriteriaportal.org/). Complementing the CCT and its CC database, the CC Knowledge Base stands as another valuable resource, offering users with guidance and support in understanding the Common Criteria and its various concepts. 

## Quick start guide

The CCT can be accessed via the CLI or TUI.

### TUI

In the main menu of the TUI navigate to the 'Common Criteria Toolbox' module. The TUI can be navigated either using the arrow keys and enter or the mouse and double left-click.

![Common Criteria Toolbox - Submenu view.](./_figures/cctsubmenu.png)

#### Browse the Common Criteria

The Common Criteria Browser provides a tree-based viewing experience to browse the hierarchically structured Security Components of the Common Criteria. Select between Functional and Assurance Components to display all respective Classes. Selecting a Class will display the Class description in the 'Item Preview' as well as load all its Families. The same applies to Components and Elements.  

![Common Criteria Toolbox - Common Criteria Browser view.](./_figures/cctbrowser.png)

#### Create an Evaluation Checklist

If you want to create an Evaluation Checklist navigate to 'Create Evaluation Checklist' in the CCT's submenu. Once in the 'Evaluation Checklist - Creation' function menu you can select the set of assurance components for which an evaluation checklist shall be created. You can either select a Package under 'Packages' or create a custom set by selecting individual components under 'Select Item/s'. 

Your current selection is displayed under 'Current Selection' and it is automatically validated to ensure that all the hierarchical and dependency relationships are satisfied within the set of selected components.
The validation status is always displayed in the 'Status bar'. 

The description of the item currently selected is displayed in the 'Item Preview' section.

![Common Criteria Toolbox - Evaluation Checklist - Creation view.](./_figures/evalcreation.png)

**Search**

In the _Common Criteria Browser_ and in the _Evaluation checklist-Creation_ views, you can search for Components using the 'Search Bar'. The search is case insensitive and allows you to match entire Classes or Families, as well as individual components.

Individual Components are searched when a perfect match is found, e.g., ADV_INT.1. Classes or Families are searched when partial matches are found, e.g., searching for 'ACO' will match all the components belonging to the 'Composition' class; similarly, searching for 'ACO_DEV' will match all components belonging to the 'Composistion Development Evidence' family. 

You will be prompted to accept or decline the automatic selection of components in case of class/family matches.

**Package augmentation**

Augmenting a package is easily done by selecting the desired package and additional components under 'Select Item/s'. The selection will be automatically validated. 

**Auto complete selection** 

The 'Auto Complete Selection' feature provides a potential valid set that includes the current selection. 

**Deselect**

Components can be deselected from the 'Current Selection' using the 'Deselect' button underneath. 

**Creating the Evaluation Checklist**

Upon selection of a valid set you can create an Evaluation Checklist. The 'Create Evaluation Checklist' button will prompt a screen asking for information to uniquely identify the checklist: 
- Evaluation Identifier (`<eid>`): a folder with this name is be created to store the selected evaluation items. A file per evaluation item is created and named with the format `<eid>-<num>`, where `num` denotes a sequential number. These files contain the description of the evaluation item and are used to track the evaluation verdicts.
- Creator
- Creation Date.

After submission, a doorstop document will be created. Each item (a markdown file with yaml frontmatter) of this document corresponds to a selected evaluation item and contains the Work Units that correspond to the selected components. As an example, Work Unit ADV_ARC.1-1 is displayed below. After successfully creating the Evaluation Checklist the system will ask you to proceed to the Evaluation Checklist.

![Evaluation item for Work Unit ADV_ARC.1-1 stored as doorstop item.](./_figures/d_evalitem.png)


#### Evaluation Checklist

When navigating to the 'Evaluation Checklist' functional menu you first have to load the Evaluation Checklist(s) using the button 'Load Evaluation Checklist/s' on the bottom left. 

Afterwards, you can select a checklist to start or proceed with your evaluation. All evaluation items are listed under 'Evaluation Item/s'. Selecting an item will display the corresponding Work Unit on the very right and the evidence (if already provided) under 'Evaluation Evidence'. 

With the buttons underneath the 'Evaluation evidence' section, a verdict (*pass*, *fail*, or *inconclusive*) can be set for the Work Unit. The changes are persisted. 

On the bottom right your progress is tracked for the current Evaluation Checklist.

![Evaluation Checklist for a mock project 'BRITE'.](./_figures/checklist.png)


*_Note - Please enter your evidence in Markdown format._*


### CLI

Note that in the following examples, we assume C5-DEC CAD to be installed via pipx using the Wheel (.whl) distribution file, but in case C5-DEC CAD is deployed and launched with the containerized environment shipped with the GitHub repository, the commands must be preceded with `poetry run` due to our use of Poetry for dependency management and packaging. Note also that the Docker Desktop Engine must also be running prior to opening the project in the containerized environment via VS Code. An example below for the usage:

Running the CLI for a pipx-based installation, i.e., C5-DEC CAD installed as an application using pipx, the following command can be used to get the help menu for the CLI:

```sh
    c5dec -h
```

which then becomes

```sh
    poetry run c5dec -h
```

in the containerized environment.

Similarly, `poetry run c5dec` simply becomes `c5dec` when the tool is [installed via pipx](./installation.md).

In the Alpha version the following commands are exposed to the CLI:

**view** 
```sh
    c5dec view <ID>
    c5dec view <ID> > <filename>.md
```
This command prints the selected CC item's content and hierarchical tree to the console in Markdown format. Output redirection can be used to save the output as a Markdown file. 

The '--version' flag allows to specify the CC version. Currently supported versions are 3R1, 3R2, 3R3, 3R4, 3R5 with 3R5 being the default version.

**validate**

```sh
    c5dec validate -d <IDs>
```

The 'validate' command currently supports only the validation/verification of the dependencies for a provided set of components both functional and/or assurance. 

In the case of an invalid selection a potential valid selection is provided. Note that the provided valid selection can be just one of many valid selections. This is particularly true for a set of functional components since these often define *or-dependencies*, i.e., the dependency is fulfilled when one of the components listed as an *or-dependency* is included in the set. 

In future releases you'll be able to blacklist *or-dependencies* you do not want to include in your project such that you'll be able to iteratively explore all the available valid options.

**checklist**

The Evaluation Checklist as described above can also be created via the CLI with

```sh
    c5dec checklist -c <prefix> --id <IDs> --info <info> 
```
This will automatically validate the provided set of components and create the checklist if and only if it is a valid selection. 

The 'prefix' corresponds to the Evaluation Identifier mentioned earlier, and the 'info' is the general information that uniquely identifies the project/TOE for which the Evaluation Checklist is created. The 'info' can be a json file.

Once an Evaluation Checklist is created you can run the following to list all created checklists, you can list all evaluation items of an Evaluation Checklist with

```sh
    c5dec checklist <prefix> -l/--list 
```

The most efficient approach to edit an Evaluation Item is using the TUI, but in case you want to edit it manually you can run the following command:
```sh
    c5dec checklist <prefix> --edit <ID> [--editor <editor>] 
```
If no 'editor' is specified if defaults to 'vim'.

After you're finished with editing the Evaluation Checklist run 
```sh
    c5dec checklist <prefix> -u/--update
```
to update the index that keeps track of the current evaluation progress. Retrieve the status of an evaluation with 
```sh
    c5dec checklist <prefix> -s/--status
```