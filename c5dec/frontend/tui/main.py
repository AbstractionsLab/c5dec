from c5dec.frontend.tui.application import Application
from c5dec.frontend.tui.miniapps.ssdlcapp import (
    RepositoryManagementModel, 
    RepositoryManagementView, 
    ItemManagementModel, 
    ItemManagementView,
    ItemRelationModel,
    ItemRelationManagementView,
    ArtifactStatusManagementModel,
    ArtifactStatusManagementView
)
from c5dec.frontend.tui.miniapps.transformerapp import (
    ImportModel,
    ImportView,
    ExportModel,
    ExportView,
    PublisherModel,
    PublisherView,
    ConverterModel,
    ConverterView
)
from c5dec.frontend.tui.miniapps.ismsapp import (
    ActivityReportModel,
    ActivityReportView,
    DocListAssistantModel,
    DocListAssistantView,
    MSWordTagProcessingModel,
    MSWordTagProcessingView,
)
from c5dec.frontend.tui.miniapps.pmapp import (
    TimeReportModel,
    OpenProjectTimeReportAssistantView,
    TimeReportAssistantView
)
from c5dec.frontend.tui.miniapps.cctapp import (
    CCBrowserModel,
    CCBrowserView,
    CreateChecklistModel,
    CreateChecklistView,
    WorkUnitModel,
    WorkUnitView
)
from c5dec.frontend.tui.miniapps.miniappbase import (
    MiniAppPlaceholderModel,
    MiniAppPlaceholderView
)
import c5dec.common as common
import c5dec.settings as c5settings


def add_function_to_tui(app, app_name, function_name, view, model):
    app.get_submenu(app_name).add_function(
        function_name, view, model)

@common.feature_flag('ON')
def add_ssdlc_module(app, name):
    SSDLC_app_name = name
    app.add_menu(SSDLC_app_name)
    app.get_submenu(SSDLC_app_name).add_function(
        "Manage artifact repositories", RepositoryManagementView, RepositoryManagementModel())
    app.get_submenu(SSDLC_app_name).add_function(
        "Manage artifact items", ItemManagementView, ItemManagementModel())
    app.get_submenu(SSDLC_app_name).add_function(
        "Manage item relations", ItemRelationManagementView, ItemRelationModel())
    app.get_submenu(SSDLC_app_name).add_function(
        "Manage repository structure and item status", ArtifactStatusManagementView, ArtifactStatusManagementModel())

@common.feature_flag('ON')
def add_cryptography_module(app, name):
    cryptography_app_name = name
    app.add_menu(cryptography_app_name)
    app.get_submenu(cryptography_app_name).add_function(
         "PQC public-key encryption (not implemented, on the roadmap)", MiniAppPlaceholderView, MiniAppPlaceholderModel)
    app.get_submenu(cryptography_app_name).add_function(
         "PQC digital signature (not implemented, on the roadmap)", MiniAppPlaceholderView, MiniAppPlaceholderModel)

@common.feature_flag('ON')
def add_cct_module(app, name):
    CCT_app_name = name
    app.add_menu(CCT_app_name)
    app.get_submenu(CCT_app_name).add_function(
        "Browse Common Criteria", CCBrowserView, CCBrowserModel())
    app.get_submenu(CCT_app_name).add_function(
        "Create Evaluation Checklist", CreateChecklistView, CreateChecklistModel())
    app.get_submenu(CCT_app_name).add_function(
        "Evaluation Checklist", WorkUnitView, WorkUnitModel())
    
@common.feature_flag('ON')
def add_cpssa_module(app, name):
    cpssa_app_name = name
    app.add_menu(cpssa_app_name)
    app.get_submenu(cpssa_app_name).add_function(
         "Generate input for threagile (not implemented, on the roadmap)", MiniAppPlaceholderView, MiniAppPlaceholderModel)
    app.get_submenu(cpssa_app_name).add_function(
         "Generate input for TRICK Service (not implemented, on the roadmap)", MiniAppPlaceholderView, MiniAppPlaceholderModel)

@common.feature_flag('ON')
def add_transformer_module(app, name):
    transformer_app_name = name
    app.add_menu(transformer_app_name)
    app.get_submenu(transformer_app_name).add_function("Import SSDLC data", ImportView, ImportModel())
    app.get_submenu(transformer_app_name).add_function("Export SSDLC data", ExportView, ExportModel())
    app.get_submenu(transformer_app_name).add_function("Publish SSDLC data", PublisherView, PublisherModel())
    app.get_submenu(transformer_app_name).add_function("Convert data", ConverterView, ConverterModel())

@common.feature_flag('ON')
def add_isms_module(app, name):
    ISMS_app_name = name
    app.add_menu(ISMS_app_name)
    app.get_submenu(ISMS_app_name).add_function(
        "Activity Report", ActivityReportView, ActivityReportModel())
    app.get_submenu(ISMS_app_name).add_function(
        "Document list validation", DocListAssistantView, DocListAssistantModel())
    app.get_submenu(ISMS_app_name).add_function(
        "Convert Word tags to hyperlinks", MSWordTagProcessingView, MSWordTagProcessingModel())

@common.feature_flag('ON')
def add_pm_module(app, name):
    pm_app_name = name
    app.add_menu(pm_app_name)

    @common.feature_flag('ON')
    def add_openproject_assistant_submenu():
        add_function_to_tui(app, pm_app_name, "OpenProject time report assistant", OpenProjectTimeReportAssistantView, TimeReportModel())
    
    @common.feature_flag('ON')
    def add_universal_time_sheet_assistant_submenu():
        add_function_to_tui(app, pm_app_name, "Universal time report assistant", TimeReportAssistantView, TimeReportModel())
    
    add_openproject_assistant_submenu()
    add_universal_time_sheet_assistant_submenu()
    
@common.feature_flag('OFF')
def add_settings_module(app, name):
    settings_app_name = name
    app.add_menu(settings_app_name)
    app.get_submenu(settings_app_name).add_function(
        "Add SFR", RepositoryManagementView, RepositoryManagementModel())

def main(args=None, cwd=None):
    c5settings.EXECUTION_MODE = "TUI"
    app = Application()

    CCT_app_name = "1 - CCT: Common Criteria toolbox"
    SSDLC_app_name = "2 - SSDLC: secure software development life cycle"
    cryptography_app_name = "3 - Cryptography (see user manual)"
    cpssa_app_name = "4 - CPSSA: Cyber-physical system security assessment (see user manual)"
    transformer_app_name = "5 - Transformer: import, export, publish"
    ISMS_app_name = "6 - ISMS: document management"
    pm_app_name = "7 - PM: project resource management"
    settings_app_name = "8 - Settings"

    add_cct_module(app, CCT_app_name)
    add_ssdlc_module(app, SSDLC_app_name)
    add_cryptography_module(app, cryptography_app_name)
    add_cpssa_module(app, cpssa_app_name)
    add_transformer_module(app, transformer_app_name)
    add_isms_module(app, ISMS_app_name)
    add_pm_module(app, pm_app_name)
    add_settings_module(app, settings_app_name)
    
    app.run()

if __name__ == "__main__":
    main()