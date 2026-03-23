import doorstop
import os
import shutil
import c5dec.settings as c5settings
import c5dec.common as common
import warnings
from datetime import datetime

log = common.logger(__name__)
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

log.setLevel(common.logging.INFO)

logHandler = common.logging.FileHandler(c5settings.PM_LOG_FILE, mode='a')
formatter = common.logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s", "%Y-%m-%d %H:%M:%S")
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

def create_new_c5dec_project(project="myproject", user="user"):
    """
    Create a new project repository based on a predefined template.

    This function performs the following steps:
    1. Copies a project template folder to a new destination.
    2. Renames nested folders and files to match the user-defined project name.
    3. Updates configuration files (e.g., devcontainer.json, Dockerfiles, scripts) 
       with the specified project name and user.
    4. Renames specific files (e.g., template_doorstop.yml) to their final names.
    5. Generates a ZIP archive of the created project.
    6. Deletes the copied project folder after archiving.

    Args:
        project (str): The name of the new project. Defaults to "myproject".
        user (str): The username to be used in configuration files. Defaults to "user".

    Returns:
        None: The function logs the progress and creates a ZIP archive of the project.
    """
    """Create a new project repository."""
    # Convert the project name to lowercase
    project = project.lower()
    # Define the source and destination paths
    source_path = os.path.abspath(os.path.join(os.getcwd(), 'assets', 'templates', 'project'))
    destination_path = os.path.abspath(os.path.join(os.getcwd(), '..', project))

    # Copy the project folder to the new location
    if os.path.exists(destination_path):
        log.error(f"Destination folder {destination_path} already exists.")
        return

    import shutil
    shutil.copytree(source_path, destination_path)
    log.info(f"Copied project folder to {destination_path}")

    # Rename nested project folder to user-defined name
    os.rename(os.path.abspath(os.path.join(os.getcwd(), '..', project, 'myproject')), os.path.abspath(os.path.join(os.getcwd(), '..', project, project)))

    # Rename the devcontainer folder and JSON file inside it
    devcontainer_path = os.path.join(destination_path, 'devcontainer')
    if os.path.exists(devcontainer_path):
        new_devcontainer_path = os.path.join(destination_path, f'.devcontainer')
        os.rename(devcontainer_path, new_devcontainer_path)
        log.info(f"Renamed devcontainer folder to {new_devcontainer_path}")

        # Rename the devcontainer.json file
        devcontainer_json_path = os.path.join(new_devcontainer_path, 'template_devcontainer.json')
        if os.path.exists(devcontainer_json_path):
            new_devcontainer_json_path = os.path.join(new_devcontainer_path, f'devcontainer.json')
            os.rename(devcontainer_json_path, new_devcontainer_json_path)
            log.info(f"Renamed template_devcontainer.json to {new_devcontainer_json_path}")

            with open(new_devcontainer_json_path, 'r') as file:
                content = file.read()

                updated_content = content.replace('/home/alab/c5dec', f'/home/{user}/{project}')
                updated_content = updated_content.replace('c5dec dev container', f'{project} dev container')

            with open(new_devcontainer_json_path, 'w') as file:
                file.write(updated_content)

            log.info(f"Updated {new_devcontainer_json_path} with user={user}")
        else:
            log.warning(f"{devcontainer_json_path} not found in {destination_path}")

    # Update the user ENV variable in dev.Dockerfile and Dockerfile
    dockerfiles = ['dev.Dockerfile', 'Dockerfile']
    for dockerfile in dockerfiles:
        dockerfile_path = os.path.join(destination_path, dockerfile)
        if os.path.exists(dockerfile_path):
            with open(dockerfile_path, 'r') as file:
                content = file.read()

            updated_content = content.replace('ENV user=alab', f'ENV user={user}')
            updated_content = updated_content.replace('ENV c5folder=c5dec', f'ENV c5folder={project}')

            with open(dockerfile_path, 'w') as file:
                file.write(updated_content)

            log.info(f"Updated {dockerfile_path} with user={user}")
        else:
            log.warning(f"{dockerfile} not found in {destination_path}")

    # Update the variables in build-c5dec.sh, c5dec.sh and pyproject.toml
    scripts = ['build-c5dec.sh', 'c5dec.sh', 'pyproject.toml']
    for script in scripts:
        script_path = os.path.join(destination_path, script)
        if os.path.exists(script_path):
            with open(script_path, 'r') as file:
                content = file.read()

            updated_content = content.replace('c5dec', f'{project}')
            updated_content = updated_content.replace('USER=alab', f'USER={user}')

            with open(script_path, 'w') as file:
                file.write(updated_content)

            log.info(f"Updated {script_path} with username {user} and project name {project}")

            new_script_name = script.replace('c5dec', f'{project}')
            new_script_path = os.path.join(destination_path, f'{new_script_name}')
            os.rename(script_path, new_script_path)
            log.info(f"Renamed script {script_path} to {new_script_path}")
        else:
            log.warning(f"{script} not found in {destination_path}")

    # Rename all template_doorstop.yml files in docs/specs/ to .doorstop.yml
    specs_path = os.path.join(destination_path, 'docs', 'specs')
    if os.path.exists(specs_path):
        for root, _, files in os.walk(specs_path):
            for file in files:
                if file == 'template_doorstop.yml':
                    old_file_path = os.path.join(root, file)
                    new_file_path = os.path.join(root, '.doorstop.yml')
                    os.rename(old_file_path, new_file_path)
                    log.info(f"Renamed {old_file_path} to {new_file_path}")
    else:
        log.warning(f"{specs_path} not found in {destination_path}")

    # Generate a ZIP archive of the created project
    zip_path = os.path.abspath(os.path.join(os.getcwd(), '..', project))
    shutil.make_archive(zip_path, 'zip', destination_path)

    # Delete the copied project folder
    shutil.rmtree(destination_path)
    log.info(f"Deleted the copied project folder {destination_path}")
    # Return the path to the ZIP archive
    zip_path = os.path.abspath(os.path.join(os.getcwd(), '..', f'{project}.zip'))
    log.info(f"Created ZIP archive at {zip_path}")

def create_docengine_template(template_type, name, destination=None, standalone=False):
    """
    Create a new DocEngine report or presentation from templates.

    This function performs the following steps:
    1. Validates the template type (report or presentation).
    2. Copies the template folder to a new destination in ./docengine/{name}/.
    3. Updates configuration files with the specified project name and current date.
    4. Generates a ZIP archive of the created template.
    5. Keeps both the working folder and ZIP archive.
    6. If standalone=True, also copies the .devcontainer folder, docEngine.Dockerfile,
       poetry.lock, and pyproject.toml so the template can be used independently in VS Code.

    Args:
        template_type (str): Type of template to create ("report" or "presentation").
        name (str): The name of the new template instance.
        destination (str, optional): Override default destination path. Defaults to ./docengine/{name}/.
        standalone (bool): If True, copies DevContainer, Dockerfile, and Poetry artifacts
            to the destination so DocEngine can be used without the full C5-DEC environment.

    Returns:
        None: The function logs the progress and creates both folder and ZIP archive.
    """
    # Validate template type
    valid_types = ["report", "presentation", "cra-tech-doc"]
    if template_type not in valid_types:
        log.error(f"Invalid template type '{template_type}'. Must be one of: {valid_types}")
        return False

    # Determine source path based on template type
    if template_type == "report":
        source_path = c5settings.REPORT_TEMPLATE_PATH
    elif template_type == "presentation":
        source_path = c5settings.PRESENTATION_TEMPLATE_PATH
    else:  # cra-tech-doc
        source_path = c5settings.CRA_TECH_DOC_TEMPLATE_PATH

    # Calculate destination path
    if destination is None:
        docengine_folder = os.path.abspath(os.path.join(os.getcwd(), 'docengine'))
        destination_path = os.path.abspath(os.path.join(docengine_folder, name))
        
        # Create docengine folder if it doesn't exist
        if not os.path.exists(docengine_folder):
            os.makedirs(docengine_folder)
            log.info(f"Created docengine folder at {docengine_folder}")
    else:
        destination_path = os.path.abspath(destination)

    # Check if destination exists
    if os.path.exists(destination_path):
        log.error(f"Destination folder {destination_path} already exists.")
        return False

    # Check if Quarto is installed (warning only, not blocking)
    if shutil.which("quarto") is None:
        log.warning("Quarto not detected. Install from https://quarto.org to render templates.")

    # Copy the template folder
    try:
        shutil.copytree(source_path, destination_path)
        log.info(f"Copied {template_type} template to {destination_path}")
    except Exception as e:
        log.error(f"Failed to copy template: {e}")
        return False

    # Get current date
    current_date = datetime.now().strftime("%d/%m/%Y")

    # Define files to update and their replacements
    files_to_update = {
        'c5dec_config.yml': [
            ('CyFORT', name),
            ('C5-DEC CAD', name),
        ],
        '_quarto.yml': [
            ('C5-DEC CAD DocEngine', f'{name}'),
            ('C5-DEC CAD', name),
        ],
        'index.qmd': [
            ('C5-DEC CAD', name),
        ],
        'README.md': [
            ('c5dec/assets/report', f'docengine/{name}'),
            ('c5dec/assets/presentation', f'docengine/{name}'),
            ('C5-DEC CAD', name),
        ],
    }

    # Perform variable substitutions
    for filename, replacements in files_to_update.items():
        file_path = os.path.join(destination_path, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Apply all replacements
                for old_text, new_text in replacements:
                    content = content.replace(old_text, new_text)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

                log.info(f"Updated {file_path} with project name '{name}'")
            except Exception as e:
                log.warning(f"Could not update {file_path}: {e}")
        else:
            log.warning(f"{filename} not found in {destination_path}")

    # Copy standalone artifacts if requested
    if standalone:
        root_path = str(c5settings.PROJECT_ROOT_PATH)
        standalone_items = [
            (os.path.join(root_path, '.devcontainer'), os.path.join(destination_path, '.devcontainer')),
            (os.path.join(root_path, 'docEngine.Dockerfile'), os.path.join(destination_path, 'docEngine.Dockerfile')),
            (os.path.join(root_path, 'poetry.lock'), os.path.join(destination_path, 'poetry.lock')),
            (os.path.join(root_path, 'pyproject.toml'), os.path.join(destination_path, 'pyproject.toml')),
        ]
        for src, dst in standalone_items:
            if os.path.exists(src):
                try:
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                    log.info(f"Copied standalone artifact: {src} -> {dst}")
                except Exception as e:
                    log.warning(f"Could not copy standalone artifact {src}: {e}")
            else:
                log.warning(f"Standalone artifact not found: {src}")

    # Create ZIP archive (keep both folder and archive)
    zip_base_path = os.path.join(os.path.dirname(destination_path), name)
    try:
        shutil.make_archive(zip_base_path, 'zip', destination_path)
        zip_path = f"{zip_base_path}.zip"
        log.info(f"Created ZIP archive at {zip_path}")
    except Exception as e:
        log.error(f"Failed to create ZIP archive: {e}")
        return False

    # Log success with next steps
    log.info(f"\nDocEngine {template_type} template created successfully!")
    log.info(f"Location: {destination_path}")
    log.info(f"Archive: {zip_path}")
    log.info("\nNext steps:")
    log.info(f"  1. cd {destination_path}")
    log.info(f"  2. Edit c5dec_config.yml with your project details")
    if template_type == "report":
        log.info("  3. Customize chapters/ with your content")
    else:
        log.info("  3. Customize slides/ with your content")
    log.info("  4. quarto render")
    
    return True

def get_artifact_tree():
    path = c5settings.PROJECT_ROOT
    tree = doorstop.build(cwd=os.getcwd(), root=path)
    return tree

def get_documents():
    path = c5settings.PROJECT_ROOT
    tree = doorstop.build(cwd=os.getcwd(), root=path)
    return tree.documents

def create_artifact_repository(repo_prefix, path=None, parent_prefix=None):
    if path is None:
        path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    if parent_prefix is None:
        tree.create_document(path, repo_prefix, sep=c5settings.DEFAULT_SEPARATOR)
    else:
        tree.create_document(path, repo_prefix, parent=parent_prefix, sep=c5settings.DEFAULT_SEPARATOR)

def delete_artifact_repository(repo_prefix):
    path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    document = tree.find_document(repo_prefix)

    prefix, relpath = document.prefix, document.relpath
    document.delete()

def get_artifact_repository(repo_prefix, parent_repo_prefix=None):
    tree = doorstop.build()
    document = tree.find_document(repo_prefix)
    return document

def reorder_artifact_repository(repo_prefix):
    tree = doorstop.build()
    document = tree.find_document(repo_prefix)
    document.reorder(manual=False)

def clear_repository(repo_id):
    tree = doorstop.build()
    document = tree.find_document(repo_id)
    for item in document.items:
        item.clear()

def clear_item(item_id):
    tree = get_artifact_tree()
    item = tree.find_item(item_id)
    item.clear()

def review_repository(repo_id):
    tree = doorstop.build()
    document = tree.find_document(repo_id)
    for item in document.items:
        item.review()

def review_item(item_id):
    tree = get_artifact_tree()
    item = tree.find_item(item_id)
    item.review()

def add_item(repo_prefix, level=None, count=1):
    path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    document = tree.find_document(repo_prefix)

    for _ in range(count):
        item = document.add_item(
            level=level
        )

def remove_item(item_id):
    path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    item = tree.find_item(item_id)
    item.delete()

def get_item_text(item_id):
    path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    item = tree.find_item(item_id)
    return item.text

def set_item_text(item_id, text):
    path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    item = tree.find_item(item_id)
    item.text = text

def link_child_item_to_parent(child_id, parent_id):
    path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    tree.link_items(child_id, parent_id)

def unlink_child_item_to_parent(child_id, parent_id):
    path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    tree.unlink_items(child_id, parent_id)

def get_item_links(item_id):
    path = c5settings.PROJECT_ROOT
    tree = get_artifact_tree()
    item = tree.find_item(item_id)
    links_string_list = [uid.string for uid in item.links]
    return links_string_list

def get_respository_attributes(repo_prefix):
    tree = doorstop.build()
    document = tree.find_document(repo_prefix)
    print(document.extended_reviewed)
    print(document.config)
    print(document.publish)

def generate_rtm():
    """Generate a requirements traceability matrix."""
    pass

def link_artifacts_in_batch():
    """Create item links from input table of ID mappings."""
    pass

def add_item_attribute_from_file():
    """Read attributes, default values and publish status from CSV file
    and write to Doorstop document YAML.
    """
    pass

def visualize_req_graph():
    """Visualize graph of req., specs and tests with status color coding."""
    pass


def tag_item():
    pass