from flask import Flask, render_template, jsonify, request, Response, make_response, session, redirect, url_for, flash
import c5dec.core.cct as cct
import c5dec.settings as c5settings
app = Flask(__name__)
app.secret_key = 'TEST_SECRET_KEY'

project_root = c5settings.PROJECT_ROOT
cc_version = c5settings.SELECTED_CC_VERSION

_index = cct.Index()

@app.errorhandler(404)
def render_page_not_found(e):
    flash('The requested page does not exist.')
    error = True
    return render_template('ccbrowser.html', error=error, page="ccbrowser"), 404

@app.route('/')
def index():
    resp = make_response(render_template('ccbrowser.html', page="ccbrowser", req_type=["SFR", "SAR"], classes=[], cc_version=c5settings.SELECTED_CC_VERSION))
    resp.cache_control.no_cache = True
    return resp

@app.route('/ccbrowser')
def ccbrowser():
    try:
        cc_object = cct.FClass
        cc_classes = _index.yield_obj(cc_object)
        class_ids = [cc_class._id.upper() for cc_class in cc_classes]
    except Exception as e:
        print(e)
    
    resp = make_response(render_template('ccbrowser.html', page="ccbrowser", req_type=["SFR", "SAR"], classes=class_ids, cc_version=c5settings.SELECTED_CC_VERSION))
    resp.cache_control.no_cache = True
    return resp

@app.route('/async_cc_req_type')
def async_cc_req_type():
    choice = request.args.get('part', 0, type=str)
    try:
        if choice == "SFR":
            class_ids = [cc_class._id.upper() for cc_class in _index.yield_obj(cct.FClass)]
        else:
            class_ids = [cc_class._id.upper() for cc_class in _index.yield_obj(cct.AClass)] 
    except Exception as e:
        print(e)
    return jsonify(result=class_ids)

@app.route('/async_cc_class')
def async_cc_class():
    class_choice = request.args.get('class', 0, type=str)
    preview_text = ""
    try:
       item_obj = _index.get(class_choice)
       preview_text = item_obj.get_formatted_text()

       children_ids = [child._id.upper() for child in item_obj.children]
       children_options = [option for i, option in enumerate(children_ids)]
    except Exception as e:
        print(e)

    return jsonify(previewText=preview_text, childrenFamilies=children_options)

@app.route('/async_cc_family')
def async_cc_family():
    family_choice = request.args.get('family', 0, type=str)
    preview_text = ""
    try:
       item_obj = _index.get(family_choice)
       preview_text = item_obj.get_formatted_text()

       children_ids = [child._id.upper() for child in item_obj.children]
       children_options = [option for i, option in enumerate(children_ids)]
    except Exception as e:
        print(e)

    return jsonify(previewText=preview_text, childrenFamilies=children_options)

@app.route('/async_cc_component')
def async_cc_component():
    component_choice = request.args.get('component', 0, type=str)
    preview_text = ""
    try:
       item_obj = _index.get(component_choice)
       preview_text = item_obj.get_formatted_text()

       children_ids = [child._id.upper() for child in item_obj.children]
       children_options = [option for i, option in enumerate(children_ids)]
    except Exception as e:
        print(e)

    return jsonify(previewText=preview_text, childrenFamilies=children_options)

@app.route('/async_cc_element')
def async_cc_element():
    element_choice = request.args.get('element', 0, type=str)
    preview_text = ""
    try:
       item_obj = _index.get(element_choice)
       preview_text = item_obj.get_formatted_text()
    except Exception as e:
        print(e)

    return jsonify(previewText=preview_text)

@app.route('/async_export')
def async_export():
    choice = request.args.get('choice', 0, type=str)
    if choice == "SFR" or choice == "SAR" or choice == "No CC item currently selected.":
        return jsonify(exportText="Selection invalid: you tried to export a part (SFR/SAR); choose a class/family/component/element instead.")
    try:
       item_obj = _index.get(choice)
       preview_text = item_obj.get_formatted_text()
    except Exception as e:
        print(e)

    explicit = item_obj.get_formatted_text()
    ancestors = item_obj.get_ancestors()
    descendants = item_obj.get_descendants()
    for descendant in descendants:
        header_level = (len(descendant.get_ancestors()) - len(ancestors)) + 1
        explicit += descendant.get_formatted_text(header_level)

    return jsonify(exportText=explicit)

@app.route('/cclab')
def cclab():
    resp = make_response(render_template('cclab.html', page="cclab"))
    resp.cache_control.no_cache = True
    return resp

@app.route('/documentation')
def documentation():
    resp = make_response(render_template('documentation.html', page="documentation"))
    resp.cache_control.no_cache = True
    return resp

@app.route('/about')
def about():
    resp = make_response(render_template('about.html', page="about"))
    resp.cache_control.no_cache = True
    return resp

@app.route('/submit', methods=['POST'])
def submit():
    cc_version = request.form.get('ccVersionSelect')
    cc_class = request.form.get('ccClassSelect')
    checklist_name = "chklist"

    if cc_class == "ALL-CLASSES":
        cct.ChecklistBuilder(checklist_name=checklist_name, cc_version=cc_version).export_eval_checklist(class_id_vector=None, component_id_vector=None)
    else:
        cct.ChecklistBuilder(checklist_name=checklist_name, cc_version=cc_version).export_eval_checklist(class_id_vector=[cc_class], component_id_vector=None) 

    flash("Checklist for assurance class {} and CC version {} exported to the following folder: {}".format(cc_class, cc_version, c5settings.EXPORT_FOLDER))
    resp = make_response(render_template('cclab.html', page="cclab", error=False))

    resp.cache_control.no_cache = True
    return resp

def main(args=None, cwd=None):
    c5settings.EXECUTION_MODE = "GUI"
    cct.load_cc_xml(version=cc_version)
    app.run(debug=True, host='0.0.0.0', port=5432)

if __name__ == '__main__':
    main()    
