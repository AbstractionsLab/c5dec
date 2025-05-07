import pandas as pd

CHAPTERS_FOLDER_NAME = "chapters"
INPUT_FOLDER_NAME = "input"
OUTPUT_FOLDER_NAME = "generated-input"
TABLE_EXPORT_FILE_NAME = "table.md"

def dataframe_to_markdown(df, grid=False):
    if grid:
        markdown = df.to_markdown(index=False, tablefmt="grid")
    else:
        markdown = df.to_markdown(index=False)
    return markdown

def dataframe_to_markdown_file(df, output_name, grid=False):
    df_in_markdown = dataframe_to_markdown(df, grid=grid)

    output_file_path = os.path.join(CHAPTERS_FOLDER_NAME, OUTPUT_FOLDER_NAME, output_name + "-" + TABLE_EXPORT_FILE_NAME)
    table_writer = open(output_file_path, 'w+')
    table_writer.write(df_in_markdown)
    table_writer.close()

def spreadsheet_table_to_markdown_table(input_file_path, sheet_number, output_name, grid=False):
    df = pd.read_excel(input_file_path, sheet_name=sheet_number)
    dataframe_to_markdown_file(df, output_name, grid=grid)

if __name__ == "__main__":
    import os

    if not os.getenv("QUARTO_PROJECT_RENDER_ALL"):
        exit()

    print(f"Running table generation pre-render script...")

    tables_list = ["DocStruct", "Acronyms", "Glossary", "EvalOverviewPP"]

    tables_input_file_path = os.path.join(CHAPTERS_FOLDER_NAME, INPUT_FOLDER_NAME, "tables.xlsx")
    for table in tables_list:
        try:
            spreadsheet_table_to_markdown_table(tables_input_file_path, table, table)
        except Exception as e:
            print(e)

    ict_tables_list = ["ChangeLog"]

    tables_input_file_path = os.path.join(CHAPTERS_FOLDER_NAME, INPUT_FOLDER_NAME, "fancy-tables.xlsx")
    for table in ict_tables_list:
        try:
            spreadsheet_table_to_markdown_table(tables_input_file_path, table, table, grid=True)
        except Exception as e:
            print(e)
