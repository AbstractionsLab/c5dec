# Secure Software Development Life Cycle

Since the SSDLC mini app exposed via the C5-DEC CAD TUI makes use of the doorstop API, it is strongly recommended to consult the official [doorstop documentation](https://doorstop.readthedocs.io/en/latest/) to gain a better understanding of the underlying concepts that the SSDLC module builds on. 

The secure software development life cycle (SSDLC) module supports three main functions by building on top of the open-source doorstop API:

- Software artifact management such as repository creation, editing, deletion, e.g., separate and dedicated doorstop documents for storing mission requirements, technical specifications, source code, test case specifications, test report items (test execution result), etc.

- Artifact item management including artifact creation, editing and deletion, e.g., for individual requirements, test case (TC) specifications and source code files in their corresponding documents

- Artifact item relation management allowing the creation and removal of links between arbitrary items (e.g., TC to requirement, TC to source code), as well as browsing linked items and their content, for a selected artifact item

- Managing artifact repository structure such as suspect link resolution, and review status updates

## Quick start guide

Once you have installed C5-DEC, the SSDLC module can be accessed via the TUI, i.e., by simplifying entering `c5dec` via the terminal, without any additional parameters.

In order to access the SSDLC functionality, navigate to the corresponding menu item shown on the landing page of C5-DEC CAD, namely "2 - SSDLC: secure software development life cycle", as shown in the screenshot below.

![C5-DEC CAD SSDLC - menu.](./_figures/c5dec-cad-ssdlc.png)

## Managing artifact collections

Select the "Manage artifact repositories" submenu to access its artifact collection/repository creation and deletion features, shown below.

![SSDLC - submenu view.](./_figures/ssdlc-manage-artifact-document.png)

Once the artifact management submenu is loaded, you can enter a prefix for the document/repository and also specify a parent prefix in case the document you are about to create should be considered a child node in the artifact document tree.

In the example shown below, we specify `srs` for system/software requirements specification, which is a child document of `mrs`, which is short for Mission Requirements Specifications. This means that the artifact items added to `srs` will be linked to parent `mrs` items.

![SSDLC artifact document management - submenu view.](./_figures/ssdlc-create-delete-artifact-document.png)

The create and delete buttons depicted in the screenshot are self-explanatory; the reset fields button acts as a shortcut for quickly clearing the content of the text fields.

## Managing artifact items

Once the artifact management submenu is loaded, the user can create new artifact items and edit existing ones. Artifact items can range from requirement specifications to test cases, test report items and design diagrams.

![SSDLC artifact management - submenu view.](./_figures/ssdlc-manage-artifact-items.png)

By simply entering a document prefix, e.g., `mrs` referring to mission requirements specification, new `mrs` items can be created, with an ID being generated and assigned to the created item automatically. In the example shown here, the user can edit the content of `mrs1` by entering its ID and pressing the "Show item text" button. Once the content has been modified, the user must press the "Save item text" for the change to be saved to disk.

## Managing relations

The "Manage item relations" submenu allows the user to create new relations between artifact items, e.g., linking an `mrs` item to an `srs` one, or linking a test case to its corresponding requirements. The same submenu also allows the user to remove or delete existing links. Moreover, the "Show child item links" button prints out the existing child items of a given parent artifact item.

### Creating and removing links

To create a new link, simply enter the IDs of the child and parent item, respectively, and press the "create link" or "remove link" buttons to confirm the desired operation.

![SSDLC artifact link management - submenu view.](./_figures/ssdlc-create-item-link.png)

### Viewing existing child items

Pressing the "Show child item links" button results in retrieving items linked to an item specified via its ID, as shown below. Upon selecting a linked item, its content is displayed in the right-hand side text box.

![SSDLC artifact link management - submenu view.](./_figures/ssdlc-view-child-items.png)

## Managing artifact document structure and item status

This submenu, shown below, allows the user to trigger the doorstop operations for reordering, clearing and reviewing; see the official doorstop documentation for its [reordering](https://doorstop.readthedocs.io/en/latest/cli/reordering/) and [validation](https://doorstop.readthedocs.io/en/latest/cli/validation/) commands.

![SSDLC document structure management - submenu view.](./_figures/ssdlc-manage-document-structure.png)

### C5-DEC DocEngine for report generation

A new feature made available as part of the beta release deals with the creation of reports, based on a robust publishing solution, namely Quarto. To this end, we have provided a complete Quarto template (found at `assets/report`).

This baseline report template can be used out of the box without any adjustments other than including your content. Our template provides a series of LaTeX customizations enhancing the fully Markdown-based experience, hiding away all such technical changes in a dedicated `tex` subfolder, which includes all the `.tex` files we use to customize our report template. We also group raw document content in a dedicated `chapters` folder, which in turn can and in our case does include sub-folders for a better separation of specifics subparts.

![C5-DEC CAD SSDLC - DocEngine baseline report based on Quarto.](./_figures/c5dec-cad-DocEngine-report.png)

Moreover, we provide pre-rendering and post-rendering code (`etr_template/scripts`) that provides various types of automation in the form of an easy-to-understand pipeline. In particular, our pre-render scripts allow the user to define all the meta data used in the cover page, as well as the headers and footers of the output report, via a dedicated YAML configuration file `c5dec_config.yml` found at the root of the `report` folder.

Using the same input format, the user can easily compile the report to several well-known and widely-used formats such as PDF, docx, and HTML, available at `assets/report/_output`. Our main enhancements focus on the PDF version as some of the specific features of Quarto itself are also better supported in this format, e.g., text call-outs.

This can be done either via the dedicated VS Code extension for Quarto, accessible using the VS Code Command Palette (Cmd/Ctr+Shift+P) and selecting the `Quarto: Render Document` option or simply via the command line, e.g.,

```sh
$ quarto render ./c5dec/assets/report/index.qmd --to pdf
```

This would then generate a PDF document stored under the `_output` folder, with an example shown below:

![C5-DEC CAD SSDLC - DocEngine compiled report example.](./_figures/c5dec-cad-DocEngine-compiled-report.png)

For exporting to `docx`, we have also provided a reference template document that Quarto uses to adjust various aspects of the generated report such as heading and table styles, but the user can and is encouraged to update this reference template or replace it with their own version. Note that most features of the conversion to `docx` work rather well out of the box, but the user needs to manually copy their cover page into the automatically generated report.