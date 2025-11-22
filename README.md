# Ren'Py Demo Game – GitHub Actions Build & Spellcheck Demo

This repository contains the demo game included with the Ren’Py SDK.  
Its purpose is to demonstrate:

-   **How to build a Ren’Py game using GitHub Actions**
    
-   **How to run a simple Python-based spellchecker on in-game dialogs** (also integrated into GitHub Actions)

## Automated Builds with GitHub Actions

The workflow located in `.github/workflows/build.yml` configures how GitHub builds the project.

The most important command in the workflow is:

`./renpy.sh launcher distribute .. --destination dist --package win`

-   The `--package` option defines which platforms to build for (e.g., `win`, `mac`, `linux`, `android`).
    
-   Build artifacts are placed into the `renpy-sdk/dist/` directory.

## Spellchecking Dialogs via Python

The repository includes a simple Python script that validates the structure of the project and performs spellchecking on dialogs.

In the GitHub Actions workflow, the spellchecker is prepared and executed using:
```
- name: Install pyenchant
  run: |
    sudo apt-get update && sudo apt-get install -y enchant-2
    pip install pyenchant

- name: Validate project structure
  run: python3 validate.py
```
This installs the required `enchant-2` library, adds the `pyenchant` Python wrapper, and runs the validation script.

## Notes

-   This repository is aimed at developers exploring automation for Ren’Py projects.
    
-   You can extend the workflow to build for multiple platforms or add more types of validation.
    
-   The example `validate.py` script can be expanded to include custom linting, dialog analysis, or other development tools.
