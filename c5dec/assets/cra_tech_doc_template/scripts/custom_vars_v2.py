"""
Enhanced custom_vars.py with automatic LaTeX conversion for changelog entries.

This version allows users to write changelog modifications in clean YAML format:
- Simple strings for single items
- Lists for multiple items (auto-converted to LaTeX itemize)
- Dict format with description and items
- Backward compatible with existing LaTeX format
"""

import yaml
import re

TEX_CUSTOMIZATION_FOLDER_NAME = "tex"

def escape_latex(text):
    """
    Escape special LaTeX characters in text.
    
    Args:
        text: String to escape
        
    Returns:
        Escaped string safe for LaTeX
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Don't escape if already contains LaTeX commands
    if '\\' in text:
        return text
    
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

def format_changelog_modifications(modifications):
    """
    Convert various changelog modification formats to LaTeX.
    
    Supports:
    1. Simple string: "First release"
    2. List of strings: ["Item 1", "Item 2", "Item 3"]
    3. Dict with description and items: {"description": "Changes:", "items": [...]}
    4. Legacy LaTeX format (passes through unchanged)
    
    Args:
        modifications: The modifications in various formats
        
    Returns:
        LaTeX-formatted string
    """
    # Legacy format: already contains LaTeX
    if isinstance(modifications, str) and '\\begin{itemize}' in modifications:
        return modifications
    
    # Simple string
    if isinstance(modifications, str):
        # Check if it contains semicolons or newlines indicating multiple items
        if ';' in modifications or '\n' in modifications:
            items = [item.strip() for item in re.split(r'[;\n]', modifications) if item.strip()]
            if len(items) > 1:
                latex_items = '\n      '.join([f'\\item {escape_latex(item)}' for item in items])
                return f'\\begin{{itemize}}\n      {latex_items}\n      \\end{{itemize}}'
        return escape_latex(modifications)
    
    # List format - clean YAML list of changes
    if isinstance(modifications, list):
        if len(modifications) == 0:
            return ""
        if len(modifications) == 1:
            return escape_latex(str(modifications[0]))
        
        # Multiple items - create itemize environment
        latex_items = '\n      '.join([f'\\item {escape_latex(str(item))}' for item in modifications])
        return f'\\begin{{itemize}}\n      {latex_items}\n      \\end{{itemize}}'
    
    # Dict format with optional description and items
    if isinstance(modifications, dict):
        description = modifications.get('description', '')
        items = modifications.get('items', [])
        
        if items:
            latex_items = '\n      '.join([f'\\item {escape_latex(str(item))}' for item in items])
            if description:
                result = f'{escape_latex(description)} \\begin{{itemize}}\n      {latex_items}\n      \\end{{itemize}}'
            else:
                result = f'\\begin{{itemize}}\n      {latex_items}\n      \\end{{itemize}}'
            return result
        return escape_latex(description) if description else ""
    
    # Fallback
    return escape_latex(str(modifications))

def load_quarto_config(quarto_config_path="_quarto.yml"):
    """
    Load Quarto configuration and extract relevant metadata.
    
    Args:
        quarto_config_path: Path to _quarto.yml file
        
    Returns:
        Dictionary with date, title, and subtitle values
    """
    with open(quarto_config_path, 'r') as file:
        try:
            quarto_config = yaml.safe_load(file)
            book_config = quarto_config.get('book', {})
            return {
                'date': book_config.get('date', ''),
                'title': book_config.get('title', ''),
                'subtitle': book_config.get('subtitle', '')
            }
        except yaml.YAMLError as exc:
            print(f"Error parsing Quarto config: {exc}")
            return {'date': '', 'title': '', 'subtitle': ''}

def resolve_quarto_placeholders(config, quarto_values):
    """
    Replace Quarto placeholders in config with actual values from _quarto.yml.
    
    Replaces:
    - <_quarto.yml date> with actual date
    - <_quarto.yml title> with actual title
    - <_quarto.yml subtitle> with actual subtitle
    
    Args:
        config: Configuration dictionary from c5dec_config_v2.yml
        quarto_values: Dictionary with date, title, subtitle from _quarto.yml
        
    Returns:
        Modified config dictionary with placeholders resolved
    """
    # Replace application-date placeholder
    if 'cover' in config and 'application-date' in config['cover']:
        if '<_quarto.yml date>' in str(config['cover']['application-date']):
            config['cover']['application-date'] = quarto_values['date']
            print(f"  ✓ Resolved application-date: {quarto_values['date']}")
    
    # Replace activity (subtitle) placeholder
    if 'meta' in config and 'activity' in config['meta']:
        if '<_quarto.yml subtitle>' in str(config['meta']['activity']):
            config['meta']['activity'] = quarto_values['subtitle']
            print(f"  ✓ Resolved activity: {quarto_values['subtitle']}")
    
    # Replace title placeholder
    if 'meta' in config and 'title' in config['meta']:
        if '<_quarto.yml title>' in str(config['meta']['title']):
            config['meta']['title'] = quarto_values['title']
            print(f"  ✓ Resolved title: {quarto_values['title']}")
    
    return config

def assign_var_in_dependency_file(file, var_mapping):
    """
    Replace placeholders in LaTeX template files with actual values.
    
    Args:
        file: Path to the output file
        var_mapping: Dictionary mapping placeholders to values
    """
    OUTPUT_FILE_PATH: str = file

    print("Updating custom variables in " + OUTPUT_FILE_PATH)

    with open(OUTPUT_FILE_PATH, 'r') as file:
        md = file.read()

    for k, v in var_mapping.items():
        if "!-- </doc-changelog> -->" in str(k):
            # Enhanced changelog processing with automatic LaTeX conversion
            latex_table_body = ""
            for i, r in enumerate(v):
                hline = "\\hline" if i < len(v)-1 else ""
                version, date, author, modifications = r[0], r[1], r[2], r[3]
                
                # Convert modifications to LaTeX format
                formatted_mods = format_changelog_modifications(modifications)
                
                latex_table_row = f"{version} & {date} & {author} & {formatted_mods} \\\\ {hline}\n    "
                latex_table_body += latex_table_row
            md = md.replace(k, latex_table_body.rstrip())
            
        elif "!-- </doc-approval> -->" in str(k):
            # Keep existing approval processing (no changes needed)
            latex_table_body = ""
            for i, r in enumerate(v):
                hline = "\\hline" if i < len(v)-1 else ""
                latex_table_row = "{} & {} & {} & {} \\\\ {} ".format(r[0], r[1], r[2], r[3], hline)
                latex_table_body += latex_table_row
            md = md.replace(k, latex_table_body)
            
        else:
            # Simple string replacement
            md = md.replace(k, v)

    with open(OUTPUT_FILE_PATH, 'w') as file:
        file.write(md)

    print("Done.")

if __name__ == "__main__":
    import os

    if not os.getenv("QUARTO_PROJECT_RENDER_ALL"):
        exit()

    print(f"Running enhanced parameter replacement pre-render script (v2)...")

    INPUT_FILENAME: str = "c5dec_config_v2.yml"  # Use v2 config file
    OUTPUT_FILENAME: str = "before-body.tex"

    INPUT_FILE_PATH = INPUT_FILENAME
    OUTPUT_FILE_PATH = os.path.join(TEX_CUSTOMIZATION_FOLDER_NAME, OUTPUT_FILENAME)

    with open(INPUT_FILE_PATH, 'r') as file:
        try:
            config = yaml.safe_load(file)
            print("Configuration loaded successfully")

        except yaml.YAMLError as exc:
            print("Error parsing YAML:")
            print(exc)
            exit(1)
    
    # Load Quarto configuration and resolve placeholders
    print("\nResolving Quarto placeholders...")
    quarto_values = load_quarto_config("_quarto.yml")
    config = resolve_quarto_placeholders(config, quarto_values)
    print("Quarto placeholders resolved\n")

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
