import os
import stats
import unittest
import lxml.etree

from io import StringIO


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


class TestFunctions(unittest.TestCase):
    def test_calc_market_percentage(self):
        self.assertEqual(
            1.0006253908692935,
            stats.calc_market_percentage(
                [
                    1.95,
                    2.05,
                ]
            ),
        )

        self.assertEqual(
            1.1636844407287503,
            stats.calc_market_percentage(
                [
                    1.30,
                    7.90,
                    14.65,
                    5.90,
                    33.20,
                ]
            ),
        )



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

    def test_get_competitions_by_name(self):
        # based on the sample output.json
        self.assertEqual(
            69,
            len(list(self.parser.get_competitions_by_name("Super Rugby"))),
        )

        self.assertIsInstance(
            list(self.parser.get_competitions_by_name("Super Rugby"))[0],
            stats.Competition,
        )

    def test_get_competitions(self):
        # based on the sample output.json
        self.assertEqual(
            543,
            len(list(self.parser.get_competitions())),
        )

        self.assertIsInstance(
            list(self.parser.get_competitions())[0],
            stats.Competition,
        )


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

    def test_option_count(self):
        self.assertEqual(
            543,
            self.reporter.option_count(),
        )

    def test_least_market_percentage(self):
        self.assertEqual(
            "NBA Playoffs-Rd 1 Series",
            self.reporter.least_market_percentage(),
        )

    def test_largest_market_percentage(self):
        self.assertEqual(
            "Super Rugby",
            self.reporter.largest_market_percentage(),
        )

    def test_dump_compentition_market_prices(self):
        fh = StringIO()
        self.reporter.dump_compentition_market_prices("Super Rugby", fh)
        fh.seek(0)

        self.assertEqual(
            "Game,Closes,Name,Calculated Market Percentage",
            fh.readlines()[0].strip(),
        )

    @unittest.skip("Not really testable.")
    def test_summary(self):
        pass

class TestCompetition(unittest.TestCase):
    def test_add_selection(self):
        comp = stats.Competition(
            venue="Dunedin",
            competition="Super Rugby",
            closes="2016-04-22 19:35:00",
            name="Tri-Bet",
            number=2023,
            sport="Rugby Union",
            game="Highlanders v Sharks",
        )

        sel = stats.Selection(
            number=1,
            name="Highlanders 8 & Over",
            odds=170,
            status="OK",
        )

        comp.add_selection(sel)
        self.assertEqual(1, len(comp.selections))
        self.assertEqual(set([sel]), comp.selections)

        # no doulbe ups should happen
        comp.add_selection(sel)
        self.assertEqual(set([sel]), comp.selections)

    def test_get_selections(self):
        comp = stats.Competition(
            venue="Dunedin",
            competition="Super Rugby",
            closes="2016-04-22 19:35:00",
            name="Tri-Bet",
            number=2023,
            sport="Rugby Union",
            game="Highlanders v Sharks",
        )

        sel1 = stats.Selection(
            number=1,
            name="Highlanders 8 & Over",
            odds=170,
            status="OK",
        )

        sel2 = stats.Selection(
            number=2,
            name="Sharks 8 & Over",
            odds=700,
            status="OK",
        )

        sel3 = stats.Selection(
            number=3,
            name="Either 7 & Under/Draw",
            odds=260,
            status="OK",
        )

        comp.add_selection(sel1)
        comp.add_selection(sel2)
        comp.add_selection(sel3)

        self.assertEqual(
            [
                sel1,
                sel2,
                sel3,
            ],
            comp.get_selections(),
        )

        self.assertEqual(
            [
                sel1,
                sel3,
                sel2,
            ],
            comp.get_selections(key=lambda x: x.odds),
        )
