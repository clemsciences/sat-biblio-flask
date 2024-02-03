"""

"""

from lxml import etree
import requests

from sat_biblio_server.data.models import Author, ReferenceBibliographiqueLivre


class BnfSruManager:
    BASE_URL = "https://catalogue.bnf.fr/api"

    @classmethod
    def search_from_query(cls, query: str):
        """

        :param query: in already formatted form
        :return:
        """
        # print(f"la requête: {query}")
        return cls._post(query)

    @classmethod
    def search_author(cls, author: Author):
        return cls._post(f"bib.author all \"{author}\"")

    @classmethod
    def search_book_ref(cls, book_ref: ReferenceBibliographiqueLivre):
        return cls._post(f"bib.title all \"{book_ref}\"")

    @classmethod
    def _get(cls, query):
        # recordSchema ["unimarcXchange","unimarcXchange-anl","intermarcXchange","intermarcXchange-anl","dublincore"]
        response = requests.get(f"{cls.BASE_URL}/SRU",
                                dict(version="1.2",
                                     operation="searchRetrieve",
                                     query=query,
                                     recordSchema="dublincore",
                                     maximumRecords=100,
                                     startRecord=1,
                                     ))
        if response.status_code == 200:
            return response
        return None

    @classmethod
    def _post(cls, query):
        response = requests.post(f"{cls.BASE_URL}/SRU",
                                 dict(version="1.2",
                                      operation="searchRetrieve",
                                      query=query,
                                      # recordSchema="unimarcXchange",
                                      recordSchema="dublincore",
                                      maximumRecords=100,
                                      startRecord=1,
                                      ))
        # print(response.url)
        if response.status_code == 200:
            r = RequestResult(response.content)
            return r
            # print("youhou")
        return None


class RequestResult:

    def __init__(self, result: str):
        self.result = result
        self.parser = etree.XMLParser(no_network=False, encoding="utf-8")
        root = etree.fromstring(result, parser=self.parser)
        self.version = ""
        self.number_of_records = -1
        self.echoed_search_retrieve_request = ""
        self.records = []
        self.diagnostics = ""
        self.parse(root)

        # self.properties = result.get("properties")
        # self.records = result.get("records")

    def parse(self, root):
        namespaces = {"srw": "{http://www.loc.gov/zing/srw/}"}
        self.records = []
        for node in root:
            if node.tag == f"{namespaces['srw']}version":
                # print(f"{namespaces['srw']}version")
                self.version = node.text
                # print(self.version)
            elif node.tag == f"{namespaces['srw']}numberOfRecords":
                self.number_of_records = node.text
            elif node.tag == f"{namespaces['srw']}echoedSearchRetrieveRequest":
                self.echoed_search_retrieve_request = node.text
            elif node.tag == f"{namespaces['srw']}records":
                # print("RECORDS")
                for n in node:
                    # print(etree.tostring(n))
                    record = Record(etree.tostring(n))
                    self.records.append(record)
                # print("taille", len(self.records))
            elif node.tag == f"{namespaces['srw']}diagnostics":
                self.diagnostics = node.text
                # print(self.diagnostics)
        # print(self.number_of_records)

    def to_dict(self):
        return dict(records=[r.to_dict() for r in self.records],
                    diagnostics=self.diagnostics,
                    number=self.number_of_records,
                    version=self.version)


class Record:
    def __init__(self, result):
        # print("record")
        namespaces = {"srw": "{http://www.loc.gov/zing/srw/}"}
        parser = etree.XMLParser(no_network=False, encoding="utf-8")
        root = etree.fromstring(result, parser=parser)
        self.record_schema = None
        self.record_packing = None
        self.record_data = None
        self.record_identifier = None
        self.record_position = None
        self.extra_record_data = None
        self.parse(root)

    def parse(self, root):
        namespaces = {"srw": "{http://www.loc.gov/zing/srw/}",
                      "mxc": ""}
        for node in root:
            # print(node.tag)
            if node.tag == f"{namespaces['srw']}recordSchema":
                # print(f"recordSchema {namespaces['srw']}recordSchema")
                # print(self.record_schema)
                self.record_schema = node.text
            elif node.tag == f"{namespaces['srw']}recordPacking":
                self.record_packing = node.text
            elif node.tag == f"{namespaces['srw']}recordData":
                self.record_data = node.text
                # print(self.record_data)
                if self.record_schema == "dc":
                    d = DublinCoreResult(node)
                    self.record_data = d
                elif self.record_schema == "marcexchange":
                    d = IntermarcResult(node)
                    # print(d)
                    self.record_data = d
            elif node.tag == f"{namespaces['srw']}recordIdentifier":
                self.record_identifier = node.text
            elif node.tag == f"{namespaces['srw']}recordPosition":
                self.record_position = node.text
            elif node.tag == f"{namespaces['srw']}extraRecordData":
                self.extra_record_data = node.text

    def to_dict(self):
        return dict(extraRecordData=self.extra_record_data,
                    recordPosition=self.record_position,
                    recordIdentifier=self.record_identifier,
                    recordData=self.record_data.to_dict(),
                    recordPacking=self.record_packing,
                    recordSchema=self.record_schema)


class DublinCoreResult:
    namespaces = {
        "dc": "http://purl.org/dc/elements/1.1/",
        # should be changed depending on the namespace
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"}

    def __init__(self, node):
        self.node = node
        self.identifier = node.xpath("//dc:identifier/text()", namespaces=DublinCoreResult.namespaces)
        self.title = node.xpath("//dc:title/text()", namespaces=DublinCoreResult.namespaces)
        self.description = node.xpath("//dc:description/text()", namespaces=DublinCoreResult.namespaces)
        self.creator = node.xpath("//dc:creator/text()", namespaces=DublinCoreResult.namespaces)
        self.publisher = node.xpath("//dc:publisher/text()", namespaces=DublinCoreResult.namespaces)
        self.date = node.xpath("//dc:date/text()", namespaces=DublinCoreResult.namespaces)
        self.language = node.xpath("//dc:language/text()", namespaces=DublinCoreResult.namespaces)
        self.subject = node.xpath("//dc:subject/text()", namespaces=DublinCoreResult.namespaces)
        self.type = node.xpath("//dc:type/text()", namespaces=DublinCoreResult.namespaces)
        self.format = node.xpath("//dc:format/text()", namespaces=DublinCoreResult.namespaces)
        self.source = node.xpath("//dc:source/text()", namespaces=DublinCoreResult.namespaces)
        self.relation = node.xpath("//dc:relation/text()", namespaces=DublinCoreResult.namespaces)
        self.rights = node.xpath("//dc:rights/text()", namespaces=DublinCoreResult.namespaces)

    def to_dict(self):
        return dict(identifier=" ".join(self.identifier),
                    title=" ".join(self.title),
                    description=" ".join(self.description),
                    creator=" ".join(self.creator),
                    publisher=" ".join(self.publisher),
                    date=" ".join(self.date),
                    language=" ".join(self.language),
                    subject=" ".join(self.subject),
                    type=" ".join(self.type),
                    format=" ".join(self.format),
                    source=" ".join(self.source),
                    relation=" ".join(self.relation),
                    rights=" ".join(self.rights))


class IntermarcResult:
    def __init__(self, node):
        self.node = node

    def to_dict(self):
        return dict()


if __name__ == "__main__":
    BnfSruManager.search_author(Author(first_name="Jean-Michel", family_name="Besnier"))
