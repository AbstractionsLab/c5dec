from c5dec.frontend.tui.foundation.menu import BaseView
from c5dec.frontend.tui.foundation.builder import Builder
from c5dec.frontend.tui.foundation.menu import Menu
import c5dec.settings as c5settings
import c5dec.common as common
from c5dec.frontend.tui.application import Application
import c5dec.core.ssdlc as ssdlc
from i18n import t as translate

class ArtifactModel:
    """Parent class for all artifact related models.
    """
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        self.project_root = c5settings.PROJECT_ROOT

    def get_project_root(self):
        return self.project_root

class RepositoryManagementModel(ArtifactModel):
    """The model of the REM management submodule.
    """
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(RepositoryManagementModel, self).__init__()
    
    def create_repository(self, repo_prefix, path=None, parent_prefix=None):
        ssdlc.create_artifact_repository(repo_prefix=repo_prefix, path=path, parent_prefix=parent_prefix)
    
    def delete_repository(self, repo_prefix):
        ssdlc.delete_artifact_repository(repo_prefix=repo_prefix)    

class RepositoryManagementView(BaseView):
    """The view of the REM management module.
    """
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view.

        The REM module provides automation,  
        abstractions and workflows on top of Doorstop.

        :param screen: the screen that displays this function       
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        app: Application = root_menu.get_ref_to_app()

        builder = Builder("Manage artifact repositories")
        builder.addLayout([100])

        # Input
        self.repo_name = builder.addText("Artifact repository PREFIX:", "reponame", gap=False)
        self.repo_parent_name = builder.addText("Parent repository PREFIX:", "parentreponame", gap=False)

        self.repo_path = builder.addPath("Path to artifact repository directory:")
        self.repo_path.value = c5settings.PROJECT_ROOT
        
        builder.addButton("Create artifact repository", self.handle_create_artifact_repo_event, gap=False, 
            gap_height=1)
        builder.addButton("Delete artifact repository", self.handle_delete_artifact_repo_event, gap=True, gap_height=1)
        
        builder.addButton("Reset fields", self.clear_fields)
        
        # Output
        builder.addLayout([100], True)
        self.statusbar = builder.addStatusBar()
        super(RepositoryManagementView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: RepositoryManagementModel = self.data_model

    def handle_create_artifact_repo_event(self):
        with common.Capture(catch=True) as success:
            self.data_model.create_repository(self.repo_name.value, self.repo_path.value, self.repo_parent_name.value)
            self.statusbar.value = "Repository created"
        if not success:
            self.statusbar.value = "Something went wrong..."

    def handle_delete_artifact_repo_event(self):
        with common.Capture(catch=True) as success:
            self.data_model.delete_repository(self.repo_name.value)
            self.statusbar.value = "Repository deleted"
        if not success:
            self.statusbar.value = "Something went wrong..."

    def clear_fields(self):
        self.repo_name.value = ""
        self.repo_parent_name.value = ""
        self.repo_path.value = self.data_model.get_project_root()

class ItemManagementModel(ArtifactModel):
    """The model of the REM item management submodule.
    """
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(ItemManagementModel, self).__init__()
    
    def add_item(self, repo_prefix, path=None, parent_prefix=None):
        pass
    
    def remove_item(self, repo_prefix):
        pass

class ItemManagementView(BaseView):
    """The view of the REM artifact management module.
    """
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view.

        The REM module provides automation and 
        abstractions over doorstop.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        app: Application = root_menu.get_ref_to_app()

        builder = Builder("Manage artifact items")
        builder.addLayout([100])

        # Input
        self.repo_name = builder.addText("Enter artifact repository PREFIX:", "reponame")
        
        builder.addButton("Add artifact item", self.handle_add_item_event, gap=True, 
            gap_height=1)
        
        self.item_id = builder.addText("ID of item to edit or remove:", "removeitemid", gap=False, gap_height=1)
        
        builder.addButton("Show item text", self.handle_edit_item_event, gap=False, gap_height=1)
        self.textbox = builder.add_textbox("Item content:", "itemtext", gap=True, gap_height=1)
        builder.addButton("Save item text", self.handle_save_item_text_event, gap=False, gap_height=1)

        builder.addButton("Remove item", self.handle_remove_item_event, gap=True, gap_height=1)
        
        builder.addButton("Reset fields", self.clear_fields)
        
        # Output
        builder.addLayout([100], True)
        self.statusbar = builder.addStatusBar()
        super(ItemManagementView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: ItemManagementModel = self.data_model

    def handle_add_item_event(self):
        with common.Capture(catch=True) as success:
            ssdlc.add_item(self.repo_name.value)
            self.statusbar.value = "Item added"
        if not success:
            self.statusbar.value = "Something went wrong..."

    def handle_edit_item_event(self):
        with common.Capture(catch=True) as success:
            text = ssdlc.get_item_text(self.item_id.value)
            self.textbox.value = text
        if not success:
            self.statusbar.value = "Something went wrong..."
    
    def handle_save_item_text_event(self):
        new_text = self.textbox.value
        with common.Capture(catch=True) as success:
            ssdlc.set_item_text(self.item_id.value, new_text)
        if not success:
            self.statusbar.value = "Something went wrong..."

    def handle_remove_item_event(self):
        with common.Capture(catch=True) as success:
            ssdlc.remove_item(self.item_id.value)
        if not success:
            self.statusbar.value = "Something went wrong..."

    def clear_fields(self):
        self.repo_name.value = ""
        self.item_id.value = ""
        self.item_id.value = ""

class ItemRelationModel(ArtifactModel):
    """The model of the REM item management submodule.
    """
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(ItemRelationModel, self).__init__()
    
    def add_item(self, repo_prefix, path=None, parent_prefix=None):
        pass
    
    def remove_item(self, repo_prefix):
        pass

class ItemRelationManagementView(BaseView):
    """The view of the REM artifact management module.
    """
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view.

        The REM module provides automation and 
        abstractions over doorstop.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        app: Application = root_menu.get_ref_to_app()

        builder = Builder("Manage item relations")
        builder.addLayout([100])

        # Input
        self.child_item_id = builder.addText("Child item ID:", "childitemid")
        self.parent_item_id = builder.addText("Parent item ID:", "parentitemid")
        
        builder.addButton("Create link", self.handle_create_link_event, gap=True, 
            gap_height=1)
        builder.addButton("Remove link", self.handle_remove_link_event, gap=True, 
            gap_height=1)
        
        builder.addButton("Show child item links", self.handle_show_link_event, gap=False, gap_height=1)

        builder.addLayout([1,1], True)
        self.links_to_parents_listbox = builder.addListBox(
            "linkslevel1", "max", [], on_change=self.handle_link_list_selection_event, position=0)
        self.textbox = builder.add_textbox("Item content:", "itemtext", position=1)
        
        builder.addButton("Reset fields", self.clear_fields)
        
        # Output
        # builder.addLayout([100], True)
        self.statusbar = builder.addStatusBar()
        super(ItemRelationManagementView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: ItemRelationManagementView = self.data_model

    def handle_create_link_event(self):
        with common.Capture(catch=True) as success:
            ssdlc.link_child_item_to_parent(self.child_item_id.value, self.parent_item_id.value)
            self.statusbar.value = "Link added."
            self.refresh_listbox_of_linked_items()
        if not success:
            self.statusbar.value = "Something went wrong..."

    def handle_remove_link_event(self):
        with common.Capture(catch=True) as success:
            ssdlc.unlink_child_item_to_parent(self.child_item_id.value, self.parent_item_id.value)
            self.statusbar.value = "Link removed."
            self.refresh_listbox_of_linked_items()
        if not success:
            self.statusbar.value = "Something went wrong..."

    def handle_show_link_event(self):
        with common.Capture(catch=True) as success:
            link_list = ssdlc.get_item_links(self.child_item_id.value)
            self.links_to_parents_listbox.options = self.builder.zipOfList(link_list)
            self.statusbar.value = "Links retrieved."
        if not success:
            self.statusbar.value = "Something went wrong..."

    def handle_link_list_selection_event(self):
        index = self.links_to_parents_listbox.value
        with common.Capture(catch=True) as success:
            if index is not None:
                item_id = self.links_to_parents_listbox.options[index][0]
                item_text = ssdlc.get_item_text(item_id)
                self.textbox.value = item_text
                self.statusbar.value = "Linked item {} text retrieved.".format(item_id)
        if not success:
            self.statusbar.value = "Something went wrong..."

    def refresh_listbox_of_linked_items(self):
        with common.Capture(catch=True) as success:
            link_list = ssdlc.get_item_links(self.child_item_id.value)
            self.links_to_parents_listbox.options = self.builder.zipOfList(link_list)
            self.statusbar.value = "Links retrieved."
        if not success:
            self.statusbar.value = "Something went wrong..."

    def clear_fields(self):
        self.clear_text_fields([self.child_item_id, self.parent_item_id])

class ArtifactStatusManagementModel(ArtifactModel):
    """The model of the SSDLC status management submodule.
    """
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(ArtifactStatusManagementModel, self).__init__()
    
class ArtifactStatusManagementView(BaseView):
    """The view of the SSDLC status management submodule.
    """
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view.

        The SSDLC artifact status module provides ...

        :param screen: the screen that displays this function       
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        app: Application = root_menu.get_ref_to_app()

        builder = Builder("Manage repository structure and item status")
        builder.addLayout([100], True)

        # Input

        self.repo_name = builder.addText("Artifact repository PREFIX:", "reponame", gap=False)
        builder.addButton("Reorder artifact repository", self.handle_reorder_repository_event, gap=True, gap_height=1)

        self.label_type = builder.addChoose(
            "LabelType", ["item UID", "repository prefix"], self.handle_label_change_event, gap=True, gap_height=1)
        
        self.label_choice = builder.addText("Repository PREFIX or item ID:", "reponame", gap=False)
        builder.addButton("Clear: absolve of suspect link status", self.handle_clear_event, gap=False, gap_height=1)
        builder.addButton("Review: absolve of unreviewed status", self.handle_review_event, gap=True, gap_height=2)
        
        builder.addButton("Reset fields", self.clear_fields)
        
        # Output
        builder.addLayout([100])
        self.statusbar = builder.addStatusBar()
        super(ArtifactStatusManagementView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: ArtifactStatusManagementModel = self.data_model

    def handle_reorder_repository_event(self):
        with common.Capture(catch=True) as success:
            ssdlc.reorder_artifact_repository(repo_prefix=self.repo_name.value) 
            self.statusbar.value = "Repository reordered."
        if not success:
            self.statusbar.value = "Something went wrong..."

    def handle_label_change_event(self):
        pass

    def handle_clear_event(self):
        with common.Capture(catch=True) as success:
            label_type = self.label_type.value
            if label_type == 0:
                ssdlc.clear_item(self.label_choice.value)
                self.statusbar.value = "Item cleared."
            else:
                ssdlc.clear_repository(self.label_choice.value)
                self.statusbar.value = "Repository cleared."
        if not success:
            self.statusbar.value = "Something went wrong..."

    def handle_review_event(self):
        with common.Capture(catch=True) as success:
            label_type = self.label_type.value
            if label_type == 0:
                ssdlc.review_item(self.label_choice.value)
                self.statusbar.value = "Item reviewed."
            else:
                ssdlc.review_repository(self.label_choice.value)
                self.statusbar.value = "Repository reviewed."
        if not success:
            self.statusbar.value = "Something went wrong..."


    def clear_fields(self):
        self.repo_name.value = ""
        self.label_choice.value = ""