# 0.3 (2024-09-15)

## Added

- A resource management tool (RMT) and cost report computation feature to the project management (PM) module
- A dedicated RMT analysis spreadsheet for obtaining a quick overview: `c5dec/assets/costrep/c5dec-rmt-analysis.xlsx`
- A new command to the CLI for running the cost report computation feature
- RMT parameterization file (`rmt-params.xlsx`) to the `c5dec/assets/tshparams` folder
- An example time sheet input file (`tsh.xlsx`) to the `c5dec/input` folder
- Automation code to the Quarto-based C5-DEC DocEngine for generating Quarto tables from spreadsheets
- Unit tests for the time report assistant component of the PM module
- A unit test suite runner shell script
- A user manual section to the PM page describing the RMT cost report feature
- New software design schematics related to the CCT module

## Fixed

- Deployment scripts bug not allowing modification of specs: docs volume mapping
- Settings module to fix a bug preventing unit test suites to run (relative path)
- Time report assistant unit tests to compute the correct path

## Modified

- Project resource management tool (RMT) module behavior so it always picks up input files/folders from the `c5dec/input` folder
- RMT CLI commands and TUI mini apps accordingly to use the new input retrieval mechanism
- Deployment scripts to improve customization
- Updated the technical specifications and traceability HTML publication following the inclusion of previously missing SWD items

# 0.2 (2024-07-19)

## Added

- Support for parsing Common Criteria 2022 release (CC2022R1)
- Dedicated object-oriented data structures to the CCT module to handle CC 2022
- Graphical user interface (GUI) in the form of a web application
- GUIs for the CCT browser and CC evaluation laboratory submodules
- C5-DEC DocEngine publishing feature based on Quarto for both generic report and ETR generation
- Dedicated data structures and algorithms for handling evaluation checklist creation in a structured format, e.g., csv and spreadsheets
- Feature to create CEM evaluation checklist spreadsheets that can be parsed by the DocEngine (exposed via both the CLI and the GUI)
- Dedicated C5-DEC publish function exposed via the CLI as a wrapper, complementing and improving the underlying Doorstop-based mechanism to publish technical specifications in HTML and Markdown
- Docker-based deployment solution for end-users, along with build and executable scripts
- test reports to the technical specifications (`tra` and `trb` under `docs`).

## Fixed

- Bugs in the CCT module, largely rooted in inconsistent data structure tracking and life cycle management, e.g., CC XML tree loaded several times
- Bugs in the CLI checklist creation function
- Errors in the technical specifications encodings, now stored under `docs/specs`

## Modified

- The CCT module to add support for setting parameters for the ETR CLI handler and CC release selection via user-accessible YAML configuration file
- Heavily refactored and improved the CCT module, e.g., use of constants to handle paths, folders, use of `os.path.join` to ensure cross-platform path management
- The specifications folder name (`reqs` to `specs`)
- Dev container Docker file to include `pipx`, git repo creation and `poetry` installation
- technical specifications under the `docs` folder to update all schematics, requirements and test cases

## Deleted

- Rendered schematics stored under `docs/sdd/images`

# 0.1 (2023-12-01)

- Initial release of C5-DEC CAD