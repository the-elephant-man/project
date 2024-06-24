import rdflib
from rdflib import Namespace, URIRef, Literal, Graph
from rdflib.namespace import RDF, OWL, DCTERMS, FOAF, SKOS
import pandas as pd
import re

internal_root = "https://w3id.org/the-elephant-man/"

namespace_mappings = {
    "SCHEMA": Namespace("https://schema.org/"),
    "MO": Namespace("http://musicontology.com/"),
    "DBO": Namespace("https://dbpedia.org/ontology/"),
    "VIR": Namespace("http://w3id.org/vir"),
    "FRBR": Namespace("http://purl.org/vocab/frbr/core"),
    "SWC": Namespace("http://data.semanticweb.org/ns/swc/ontology"),
    "FABIO": Namespace("http://purl.org/spar/fabio/"),
    "CRM": Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "GNDO": Namespace("http://d-nb.info/standards/elementset/gnd"),
    "MADS": Namespace("http://www.loc.gov/mads/rdf/v1#"),
    "GVP": Namespace("http://vocab.getty.edu/ontology"),
    "FRAPO": Namespace("http://purl.org/cerif/frapo"),
    "WD": Namespace("http://www.wikidata.org/entity"),
    "BIBO": Namespace("http://purl.org/ontology/bibo/"),
    "CWRC": Namespace("https://sparql.cwrc.ca/ontologies/cwrc.html#"),
    "RDF": RDF,
    "OWL": OWL,
    "DCTERMS": DCTERMS,
    "FOAF": FOAF,
    "SKOS": SKOS,
}

# creating the graph
g = Graph()

# binding prefixes
for prefix, namespace in namespace_mappings.items():
    g.bind(prefix.lower(), namespace)


# Function to resolve prefixed properties to full URIRefs
def resolve_prefixed_property(prefixed_property):
    namespace, local_name = prefixed_property.split(":")
    # crm case
    if namespace == "crm":
        local_name = local_name.split(" ")[0]
    namespace = namespace_mappings[namespace.upper()]

    return namespace[local_name]


# match functions
# to match internal uris
def matches_internal_uri(input_string):
    pattern = r"[a-z]+:\w+"
    return bool(re.match(pattern, input_string))


# to match dates
def matches_dates(input_string):
    pattern = r"\d{4}(\/\d{2}(\/\d{1,2})?)?"
    return bool(re.match(pattern, input_string))


# Access csv
csv_files_list = [
    "Merrick.csv",
    "Artifact.csv",
    "JournalArticle.csv",
    "Letter.csv",
    "Model.csv",
    "Movie.csv",
    "Portrait.csv",
    "Screenplay.csv",
    "Book.csv",
    "Hospital.csv",
    "Song.csv",
    "rel_complete.csv",
]
csv_folder_path = "././items-csv/"

# internal uris types
internal_uri_types = [
    "person/",
    "item/",
    "place/",
    "time/",
    "concept/",
    "language",
    "organization",
    "occupation",
]

# iterating over the csvs files
for csv_file in csv_files_list:
    df = pd.read_csv(csv_folder_path + csv_file, delimiter=";")
    for _, row in df.iterrows():
        # subject
        s = URIRef(internal_root + row.iloc[0].replace(" ", "-"))
        # predicate
        p = resolve_prefixed_property(row.iloc[1])
        # object
        o = row.iloc[2]
        # check if object contains part of the internal uri
        if any(uri_type in o for uri_type in internal_uri_types):
            # internal uri object
            o = URIRef(internal_root + o.replace(" ", "-"))
        # check if the object is an external entity
        elif matches_internal_uri(o):
            o = resolve_prefixed_property(o)
        # check authorities
        elif "http://" in o or "https://" in o:
            o = URIRef(o)
        # literals
        else:
            # dates
            if matches_dates(o):
                o = Literal(o, datatype=namespace_mappings["SCHEMA"].Date)
            else:
                # normal literals
                o = Literal(o)
        # add triple to the graph
        g.add((s, p, o))

    turtle_str = g.serialize(format="turtle", base=internal_root, encoding="utf-8")
    with open("turtle-serialization.ttl", "wb") as f:
        f.write(turtle_str)
