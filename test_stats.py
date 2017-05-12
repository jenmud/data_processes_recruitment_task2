import os
import stats
import unittest
import lxml.etree


JSONFILE = os.path.join(
    os.path.dirname(__file__),
    "options.json"
)

XMLFILE = os.path.join(
    os.path.dirname(__file__),
    "options.xml"
)


def make_json_reporter():
    parser = stats.JSONParser()
    return stats.Reporter(parser=parser)


def make_json_loaded_reporter():
    reporter = make_json_reporter()
    with open(JSONFILE) as fh:
        reporter.load(fh)
    return reporter


def make_xml_reporter():
    parser = stats.XMLParser()
    return stats.Reporter(parser=parser)


def make_xml_loaded_reporter():
    reporter = make_json_reporter()
    with open(XMLFILE) as fh:
        reporter.load(fh)
    return reporter


class TestJSONParser(unittest.TestCase):
    def setUp(self):
        self.parser = stats.JSONParser()
        with open(JSONFILE) as fh:
            self.parser.parse(fh)

    def test_parse(self):
        # rese the paser to get the parsing of data
        self.paser = stats.JSONParser()
        with open(JSONFILE) as fh:
            self.parser.parse(fh)

        self.assertIsNotNone(self.parser.data)
        self.assertIsInstance(self.parser.data, dict)

    def test_option_count(self):
        # based on the sample output.json
        self.assertEqual(543, self.parser.option_count())


class TestXMLParser(TestJSONParser):
    def setUp(self):
        self.parser = stats.XMLParser()
        with open(XMLFILE) as fh:
            self.parser.parse(fh)

    def test_parse(self):
        # rese the paser to get the parsing of data
        self.parser = stats.XMLParser()
        with open(XMLFILE) as fh:
            self.parser.parse(fh)

        self.assertIsNotNone(self.parser.data)
        self.assertIsInstance(
            self.parser.data,
            lxml.etree._Element,
        )



class TestReporter(unittest.TestCase):
    def setUp(self):
        self.reporter = make_json_loaded_reporter()

    def test_load_json(self):
        reporter = make_json_reporter()

        with open(JSONFILE) as fh:
            reporter.load(fh)

        self.assertIsNotNone(reporter.parser.data)
        self.assertIsInstance(reporter.parser.data, dict)

    def test_load_xml(self):
        reporter = make_xml_reporter()

        with open(XMLFILE) as fh:
            reporter.load(fh)

        self.assertIsNotNone(reporter.parser.data)
        self.assertIsInstance(
            reporter.parser.data,
            lxml.etree._Element,
        )

    def test_summary(self):
        self.assertEqual(
            "Available options: 543",
            self.reporter.summary(),
        )
