import yaml

TEX_CUSTOMIZATION_FOLDER_NAME = "tex"

def assign_var_in_dependency_file(file, var_mapping):

    OUTPUT_FILE_PATH: str = file

    print("Updating custom variables in " + OUTPUT_FILE_PATH)

    with open(OUTPUT_FILE_PATH, 'r') as file:
        md = file.read()

    for k, v in var_mapping.items():
        if not(("!-- </doc-changelog> -->" in str(k)) or ("!-- </doc-approval> -->" in str(k))):
            md = md.replace(k, v)
        else:
            latex_table_body = ""
            for i, r in enumerate(v):
                hline = ""
                if i < len(v)-1:
                    hline = "\\hline"
                latex_table_row = "{} & {} & {} & {} \\\\ {} ".format(r[0], r[1], r[2], r[3], hline)
                latex_table_body += latex_table_row
            md = md.replace(k, latex_table_body)

    with open(OUTPUT_FILE_PATH, 'w') as file:
        file.write(md)

    print("Done.")

if __name__ == "__main__":
    import os

    if not os.getenv("QUARTO_PROJECT_RENDER_ALL"):
        exit()

    print(f"Running parameter replacement pre-render script...")

    INPUT_FILENAME: str = "c5dec_config.yml"
    OUTPUT_FILENAME: str = "before-body.tex"

    INPUT_FILE_PATH = INPUT_FILENAME
    OUTPUT_FILE_PATH = os.path.join(TEX_CUSTOMIZATION_FOLDER_NAME, OUTPUT_FILENAME)

    with open(INPUT_FILE_PATH, 'r') as file:
        try:
            config = yaml.safe_load(file)
            print(config)

        except yaml.YAMLError as exc:
            print(exc)

    var_mapping = dict({
        "<!-- </co-name> -->": config['cover']['company'],
        "<!-- </project-name> -->": config['cover']['project'],
        "<!-- </doc-type> -->": config['cover']['type'],
        "<!-- </doc-ref> -->": config['cover']['reference'],
        "<!-- </doc-ver> -->": config['cover']['version'],
        "<!-- </doc-state> -->": config['cover']['state'],
        "<!-- </doc-owner> -->": config['cover']['owner'],
        "<!-- </doc-authors> -->": config['cover']['authors'],
        "<!-- </doc-application-date> -->": config['cover']['application-date'],
        "<!-- </doc-classification> -->": config['cover']['classification'],
        "<!-- </doc-bottom-text> -->": config['cover']['bottom-text'],
        "<!-- </doc-approval> -->": config['meta']['approval'],
        "<!-- </doc-changelog> -->": config['meta']['changelog']
        })

    assign_var_in_dependency_file(OUTPUT_FILE_PATH, var_mapping)

    OUTPUT_FILENAME: str = "include-in-header.tex"

    OUTPUT_FILE_PATH = os.path.join(TEX_CUSTOMIZATION_FOLDER_NAME, OUTPUT_FILENAME)

    var_mapping = dict({
        "<!-- </doc-type> -->": config['meta']['type'],
        "<!-- </doc-activity> -->": config['meta']['activity'],
        "<!-- </doc-title> -->": config['meta']['title'],
        "<!-- </doc-classification> -->": config['cover']['classification'],
        "<!-- </doc-fullname> -->": config['cover']['reference']+"\_"+config['meta']['type']+"\_"+config['meta']['fullname']+"\_v"+config['cover']['version']
        })

    assign_var_in_dependency_file(OUTPUT_FILE_PATH, var_mapping)