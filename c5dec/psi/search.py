from lxml import etree as etree_
from lxml import objectify
import lxml.etree as ET
import markdown

def retrieve_by_xpath(xml_file, dtd_file):
    # print(xml_file,dtd_file)
    otree = None
    # Load the DTD file
    with open(dtd_file, 'r') as dtd_f:
        dtd = etree_.DTD(dtd_f)

    # Parse the XML file
    parser = etree_.XMLParser(dtd_validation=False)
    with open(xml_file, 'r') as xml_f:
        try:
            doc = etree_.parse(xml_f, parser)
            # otree = objectify.parse(xml_f)
            print("XML is well-formed and valid according to the DTD")
        except etree_.XMLSyntaxError as e:
            print(f"XML Validation Error: {e}")
        
    # Perform operations on the parsed XML doc here
    
    # print root element name
    # print("Root element:", doc.getroot().tag)
    
    # query_result = doc.xpath("/cc/a-class[@id='alc']/a-family[@id='alc_cmc']/af-objectives/para[1]/text()")

    # Get all SFR class IDs
    # query_result = [e for e in doc.xpath("/cc/f-class/@id")]
    # print(query_result)

    # Get all family IDs for a given SFR class ID
    # query_result = [e for e in doc.xpath("/cc/f-class[@id='fdp']/f-family/@id")]
    # print(query_result)

    # Get all component IDs for a given SFR family ID
    # query_result = [e for e in doc.xpath("/cc/*/f-family[@id='fdp_iff']/f-component/@id")]
    # print(query_result)

    # Get all element IDs for a given SFR component ID
    # query_result = [e for e in doc.xpath("/cc/*/*/f-component[@id='fdp_iff.6']/f-element/@id")]
    # print(query_result)

    query_result = doc.xpath("/cc/*/*/f-component[@id='fdp_iff.6']/f-element")
    for e in query_result:
        print(e.text)
        for se in e.getchildren():
            print(se.tag)
            for assignment in se.getchildren():
                print(assignment.text)