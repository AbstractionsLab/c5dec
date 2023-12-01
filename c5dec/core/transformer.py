import doorstop
import os
import c5dec.settings as c5settings
import c5dec.common as common
import time

log = common.logger(__name__)

project_root = c5settings.PROJECT_ROOT

def import_ssdlc_document(path, prefix, format):
    tree = doorstop.build()
    document = tree.find_document(prefix)
    doorstop.importer.import_file(path, document, format)

def export_ssdlc_document(label, path=None, format=".yml") -> str:
    tree = doorstop.build()
    if label != "all":
        document = tree.find_document(label)
        current_time = time.strftime("%Y%m%d-%H%M%S")
        if path is None:
            path = "{}/{}-export-{}{}".format(c5settings.EXPORT_FOLDER, label, current_time, format)
        doorstop.exporter.export(document, path, format)
    else:
        if path is None:
            path = "./export"
            common.create_dirname(path)
        doorstop.exporter.export(tree, path, format)
    return path

def publish_ssdlc_document(prefix, path=None, format="html"):
    tree = doorstop.build()
    if prefix != "all":
        document = tree.find_document(prefix)
        current_time = time.strftime("%Y%m%d-%H%M%S")
        if path is None:
            path = "{}/{}-publish-{}{}".format(c5settings.EXPORT_FOLDER, prefix, current_time, format)
        doorstop.publisher.publish(document, path, format)
    else:
        if path is None:
            path = "./export"
            common.create_dirname(path)
        doorstop.publisher.publish(tree, path, format)
    return path
