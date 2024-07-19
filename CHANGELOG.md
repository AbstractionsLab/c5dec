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