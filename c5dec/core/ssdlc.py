import doorstop
import os
import c5dec.settings as c5settings
import c5dec.common as common

log = common.logger(__name__)

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