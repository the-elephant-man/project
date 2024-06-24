import xml.etree.ElementTree as ET
import rdflib
from rdflib import Namespace, URIRef, Literal, Graph
from rdflib.namespace import RDF, FOAF, RDFS, DC, DCTERMS, OWL
from pathlib import Path

filepath = Path(__file__).parent / "xml_text.xml"

tree = ET.parse(filepath)

# ontologies
internal_root = "https://w3id.org/the-elephant-man/"
SCHEMA = Namespace("https://schema.org/")
FABIO = Namespace("http://purl.org/spar/fabio/")
BIBTEX = Namespace("http://purl.oclc.org/NET/nknouf/ns/bibtex#")

# graph
g = Graph()
g.bind('SCHEMA', SCHEMA)
g.bind("FABIO", FABIO)
g.bind("BIBTEX", BIBTEX)

# namespace
namespace = {"tei": "http://www.tei-c.org/ns/1.0"}


# Internal URIs
local_uri_dict = {}
# Elements
author_el = tree.find(".//tei:author", namespaces=namespace)
merrick_el = tree.find('.//tei:[id="Merrick"]', namespaces=namespace)


# book
local_uri_dict['book'] = URIRef(internal_root + 'Book')
title = Literal(tree.find(".//tei:title", namespaces=namespace).text)
author = URIRef(internal_root + author_el.text.replace(' ', '-'))

publication_date = Literal(
    tree.find(".//tei:biblStruct/tei:monogr/tei:imprint/tei:date", namespaces=namespace).text
)
publication_place = Literal(
    tree.find(
        ".//tei:biblStruct/tei:monogr/tei:imprint/tei:pubPlace", namespaces=namespace
    ).text
)
publisher = URIRef(
    tree.find(
        ".//tei:biblStruct/tei:monogr/tei:imprint/tei:publisher", namespaces=namespace
    ).get("sameAs")
)
setting_place = Literal(
    tree.find(".//tei:name", namespaces=namespace).text
)
setting_time = Literal(
    tree.find(".//tei:time", namespaces=namespace).text
)


# ebook
local_uri_dict["ebook"] = URIRef(internal_root + "Ebook")
publisher_ebook = Literal(
    tree.findall(
        ".//tei:publisher", namespaces=namespace
    )[0].text
)
extent = Literal(tree.find(".//tei:extent", namespaces=namespace).text)
publication_place = Literal(
    tree.find(
        ".//tei:pubPlace", namespaces=namespace
    ).text
)
publication_date_ebook = Literal(
    tree.find(".//tei:publicationStmt/tei:date", namespaces=namespace).text
)
identifier_ebook = Literal(
    tree.find(".//tei:publicationStmt/tei:idno", namespaces=namespace).text)


g.add((local_uri_dict["book"], DCTERMS.title, title))
g.add((local_uri_dict["book"], DCTERMS.creator, author))
g.add((local_uri_dict["book"], SCHEMA.datePublished, publication_date))
g.add((local_uri_dict["book"], FABIO.hasPlaceOfPublication, publication_place))
g.add((local_uri_dict["book"], DCTERMS.publisher, publisher))
g.add((local_uri_dict["book"], SCHEMA.contentLocation, setting_place))
g.add((local_uri_dict["book"], SCHEMA.temporalCoverage, setting_time))
g.add((local_uri_dict["book"], BIBTEX.has_edition, local_uri_dict["ebook"]))

g.add((local_uri_dict["ebook"], DCTERMS.extent, extent))
g.add((local_uri_dict["ebook"], DCTERMS.publisher, publisher_ebook))
g.add((local_uri_dict["ebook"], SCHEMA.datePublished, publication_date_ebook))
g.add((local_uri_dict["ebook"], SCHEMA.identifier, identifier_ebook))


# Loop through each person element
for person in tree.findall(".//tei:listPerson/tei:person", namespaces=namespace):
    xml_id = person.get(
        "{http://www.w3.org/XML/1998/namespace}id"
    )  # Get the value of xml:id attribute
    same_as = person.get("sameAs")  # Get the value of sameAs attribute
    # Find and print forename, surname, and nickname (addName type="nickname")
    forename_elem = person.find("./tei:persName/tei:forename", namespaces=namespace)
    surname_elem = person.find("./tei:persName/tei:surname", namespaces=namespace)
    nickname_elem = person.find(
        "./tei:persName/tei:addName[@type='nickname']", namespaces=namespace
    )
    occupation_elem = person.find(
        "./tei:occupation", namespaces=namespace
    )

    forename = forename_elem.text if forename_elem is not None else None
    surname = surname_elem.text if surname_elem is not None else None
    nickname = nickname_elem.text if nickname_elem is not None else None
    occupation = occupation_elem.text if occupation_elem is not None else None

    if surname:
        local_uri_dict[xml_id] = URIRef(internal_root + forename + '-' + surname)
    else:
        local_uri_dict[xml_id] = URIRef(internal_root + nickname)

    # FOAF:name
    g.add((local_uri_dict[xml_id], FOAF.name, Literal(f'{forename} {surname if surname is not None else ''}')))
    # OWL:sameAs
    g.add((local_uri_dict[xml_id], OWL.sameAs, URIRef(same_as)))
    if occupation: 
        g.add((local_uri_dict[xml_id], SCHEMA.hasOccupation, Literal(occupation)))
    if nickname:
        g.add((local_uri_dict[xml_id], FOAF.nick, Literal(nickname)))


turtle_str = g.serialize(format="turtle", base=internal_root, encoding="utf-8")
with open("TEI-to-RDF-turtle-serialization.ttl", "wb") as f:
        f.write(turtle_str)
