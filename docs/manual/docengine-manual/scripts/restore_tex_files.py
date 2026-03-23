import yaml

TEX_CUSTOMIZATION_FOLDER_NAME = "tex"

def restore_file(source, target):

    print(f"Running post-render script...")
    print("Restoring TeX file " + target)

    with open(source, 'r') as source_file:
        try:
            input = source_file.read()

        except yaml.YAMLError as exc:
            print(exc)

        f = open(target, "w")
        f.write(input)

if __name__ == "__main__":
    import os

    if not os.getenv("QUARTO_PROJECT_RENDER_ALL"):
        exit()

    INPUT_FILENAME: str = "before-body-source.tex"
    OUTPUT_FILENAME: str = "before-body.tex"

    INPUT_FILE_PATH = os.path.join(TEX_CUSTOMIZATION_FOLDER_NAME, INPUT_FILENAME)
    OUTPUT_FILE_PATH = os.path.join(TEX_CUSTOMIZATION_FOLDER_NAME, OUTPUT_FILENAME)

    restore_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)

    INPUT_FILENAME: str = "include-in-header-source.tex"
    OUTPUT_FILENAME: str = "include-in-header.tex"

    INPUT_FILE_PATH = os.path.join(TEX_CUSTOMIZATION_FOLDER_NAME, INPUT_FILENAME)
    OUTPUT_FILE_PATH = os.path.join(TEX_CUSTOMIZATION_FOLDER_NAME, OUTPUT_FILENAME)

    restore_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)

    