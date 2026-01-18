"""From database to Dublin Core

"""

from xml.etree.ElementTree import Element, SubElement, tostring

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


def from_data_to_dublin_core(record_data, reference_data, authors_data):
    title = reference_data.get("titre", "")
    creators = ", ".join([
        f"{a.get('first_name', '').strip()} {a.get('family_name', '').strip()}".strip()
        for a in authors_data
        if a
    ])
    subject = record_data.get("aide_a_la_recherche", "")
    description = reference_data.get("description", "")
    publisher = reference_data.get("editeur", "")
    contributor = ""
    date_pub = str(reference_data.get("annee", "")) if reference_data.get("annee") is not None else ""
    type_ = "Text"
    nb_page = reference_data.get("nb_page")
    format_ = f"{nb_page} pages" if nb_page else ""
    identifiers = []
    if reference_data.get("ark_name"):
        identifiers.append(f"ark:/{reference_data.get('ark_name')}")
    if record_data.get("record_ark_name"):
        identifiers.append(f"ark:/{record_data.get('record_ark_name')}")
    if record_data.get("cote"):
        identifiers.append(f"cote:{record_data.get('cote')}")
    identifier = "; ".join([i for i in identifiers if i])
    source = ""
    language = record_data.get("langue", "") or reference_data.get("langue", "") or ""
    relation = ""
    coverage = reference_data.get("lieu_edition", "")
    rights = ""
    return dict(Title=title,
                Creator=creators,
                Subject=subject,
                Description=description,
                Publisher=publisher,
                Contributor=contributor,
                Date=date_pub,
                Type=type_,
                Format=format_,
                Identifier=identifier,
                Source=source,
                Language=language,
                Relation=relation,
                Coverage=coverage,
                Rights=rights)


def dublin_core_dict_to_xml(dc: dict) -> str:
    """Build a simple Dublin Core XML (oai_dc) from the given dict.

    Keys expected: Title, Creator, Subject, Description, Publisher, Contributor,
    Date, Type, Format, Identifier, Source, Language, Relation, Coverage, Rights
    """
    # Namespaces
    NS_OAI_DC = "http://www.openarchives.org/OAI/2.0/oai_dc/"
    NS_DC = "http://purl.org/dc/elements/1.1/"
    NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"

    def qname(ns, tag):
        return f"{{{ns}}}{tag}"

    root = Element(qname(NS_OAI_DC, "dc"), attrib={
        qname(NS_XSI, "schemaLocation"): f"{NS_OAI_DC} {NS_OAI_DC}oai_dc.xsd"
    })
    # Set xmlns declarations (ElementTree handles them when using QName-like notation on subelements)
    root.set("xmlns:oai_dc", NS_OAI_DC)
    root.set("xmlns:dc", NS_DC)
    root.set("xmlns:xsi", NS_XSI)

    mapping = {
        "Title": "title",
        "Creator": "creator",
        "Subject": "subject",
        "Description": "description",
        "Publisher": "publisher",
        "Contributor": "contributor",
        "Date": "date",
        "Type": "type",
        "Format": "format",
        "Identifier": "identifier",
        "Source": "source",
        "Language": "language",
        "Relation": "relation",
        "Coverage": "coverage",
        "Rights": "rights",
    }

    for key, dc_tag in mapping.items():
        val = dc.get(key)
        if not val:
            continue
        # If the field contains multiple values separated by ';', split and create multiple elements
        values = [v.strip() for v in str(val).split(";") if v.strip()] if key in ("Creator", "Identifier", "Subject") else [str(val)]
        for v in values:
            SubElement(root, qname(NS_DC, dc_tag)).text = v

    # Serialize to string with XML declaration
    xml_bytes = tostring(root, encoding="utf-8", xml_declaration=True, method="xml")
    return xml_bytes.decode("utf-8")
