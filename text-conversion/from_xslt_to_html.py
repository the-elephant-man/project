from lxml import etree

tei_file = etree.parse("tei_xml")
xsli_file = etree.parse("xml_to_xslt.xslt")

transform = etree.XSLT(xsli_file)
result_tree = transform(tei_file)

with open("Elephant.html", "wb") as f:
    f.write(etree.tostring(result_tree, pretty_print=True))