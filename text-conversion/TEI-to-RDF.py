import xml.etree.ElementTree as ET
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, FOAF, RDFS, DC, DCTERMS

tree = ET.parse("xml_text.xml")

namespace = {"tei": "http://www.tei-c.org/ns/1.0"}

title_elem = tree.find(".//tei:title", namespaces=namespace)

if title_elem is not None:
    print("Title:", title_elem.text)
else:
    print("Title element not found.")
