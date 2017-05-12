import abc
import csv
import json
from lxml import etree


def calc_market_percentage(prices):
    """
    Calculate the market percentage for a given set of prices.

    :param prices: Prices in cents used for the market percentage calculation.
    :type prices: iterable of :class:`int`
    :returns: Market price.
    :rtype: :class:`float`
    """
    value = 0.0

    for price in prices:
      value = value + 1.0 / price

    return value


class IStatsParser(object):
    """
    Interface for a stats parser.
    """
    metaclass=abc.ABCMeta

    def __init__(self):
        self.data = None

    @abc.abstractmethod
    def parse(self, fh):
        """
        Parse the file handler.

        :param fh: File to parse.
        :type fh: :class:`file`
        """
        pass

    @abc.abstractmethod
    def option_count(self):
        """
        Count how many options are available.

        :returns: Total available options.
        :rtype" :class:`int`
        """
        pass

    @abc.abstractmethod
    def get_competition(self, name):
        """
        Get all the competitions by name.

        :param name: Competition name you are filtering for.
        :type name: :class:`str`
        :returns: All the competitions found that match the provided name.
        :rtype" iterable of :class:`~.Competition`
        """
        pass


class Selection(object):
    """
    Selection is a competition selection.

    :param number: Number of the selection.
    :type number: :class:`int`
    :param name: Selection name.
    :type name: :class:`str`
    :param odds: Selection odds.
    :type odds: :class:`int`
    :param status: Selection status. Eg: OK
    :type status: :class:`str`
    """
    def __init__(self, number, name, odds, status):
        self.number = number
        self.name = name
        self.odds = odds
        self.status = status

    def __str__(self):
        return (
            "<{}> Number: {}, Odds: {}, Status: {}".format(
                self.__class__.__name__,
                self.number,
                self.odds,
                self.status,
            )
        )

    def __repr__(self):
        return self.__str__()


class Competition(object):
    """
    Competition is a object containing information about a competition.

    :param venue: Venue of the competition.
    :type venue: :class:`str`
    :param competition: Competition name.
    :type competition: :class:`str`
    :param closes: Date and time string when the competition closes.
    :type closes: :class:`str`
    :param name: Name.
    :type name: :class:`str`
    :param number: Number of the competition.
    :type number: :class:`int`
    :param sport: Type of sport played for the competition.
    :type sport: :class:`str`
    :param game: Team versing each other.
    :type game: :class:`str`
    :param selections: Selection bets.
    :type selections: iterable of :class:`~.Selection`
    """
    def __init__(self, venue, competition, closes, name, number, sport, game):
        self.venue = venue
        self.competition = competition
        self.closes = closes
        self.name = name
        self.number = number
        self.sport = sport
        self.game = game
        self.selections = set()

    def add_selection(self, selection):
        """
        Add a new selection to the competition.

        :param selection: Selection being added to the competition.
        :type selections: :class:`~.Selection`
        """
        self.selections.add(selection)

    def get_selections(self, key=None):
        """
        Get all the selections for the competition.

        :param key: Callable that takes a single value and returns a
            boolean value. This callable is used for sorting. If key is
            omitted then the default sorted algorithm is used.
        :type key: callable which takes a single argument and returns
            a :class:`bool`
        :returns: Iterable of selections for the compatition.
        :rtype: iterable of :class:`Selection`
        """
        if key is None:
            key = lambda x: x.number
        return sorted(self.selections, key=key)


class JSONParser(IStatsParser):
    """
    JSON stats file parser.
    """
    def parse(self, fh):
        self.data = json.load(fh, parse_float=True)

    def option_count(self):
        options = self.data.get("options", {})
        return len(options.get("option", []))

    def get_competitions(self, name):
        for each in self.data.get("options", {}).get("option", []):
            if each.get("competition", "") != name:
                continue

            comp = Competition(
                venue=each.get("venue"),
                competition=each.get("competition"),
                closes=each.get("closes"),
                name=each.get("name"),
                number=int(each.get("number", 0)),
                sport=each.get("sport"),
                game=each.get("game"),
            )

            for sel in each.get("selections", {}).get("selection", []):
                selection = Selection(
                    number=int(sel.get("number", 0)),
                    name=sel.get("name"),
                    odds=int(sel.get("odds", 0)),
                    status=sel.get("status"),
                )

                comp.add_selection(selection)

            yield comp


class XMLParser(IStatsParser):
    """
    XML stats file parser.
    """
    def parse(self, fh):
        self.data = etree.parse(fh).getroot()

    def option_count(self):
        return int(self.data.xpath("count(//options/option)"))

    def get_competitions(self, name):
        for each in self.data.xpath("//options/option"):
            kwargs = {}
            for key, value in each.items():
                kwargs[key] = value

            if kwargs.get("competition", "") != name:
                continue

            comp = Competition(
                venue=kwargs.get("venue"),
                competition=kwargs.get("competition"),
                closes=kwargs.get("closes"),
                name=kwargs.get("name"),
                number=int(kwargs.get("number", 0)),
                sport=kwargs.get("sport"),
                game=kwargs.get("game"),
            )

            for sel in each.xpath("selections/selection"):
                sel_kwargs = {}
                for key, value in sel.items():
                    sel_kwargs[key] = value

                selection = Selection(
                    number=int(sel.get("number", 0)),
                    name=sel.get("name"),
                    odds=int(sel.get("odds", 0)),
                    status=sel.get("status"),
                )

                comp.add_selection(selection)

            yield comp


class Reporter(object):
    """
    Reporter generates a stats summary report.

    :param parser: Parser used for parser stats files.
    :type parser: :class:`IStatsParser`
    """
    def __init__(self, parser):
        self.parser = parser

    def load(self, fh):
        """
        Load and parse the given file.

        :param fh: File being parsed.
        :type fh: :class:`file`
        """
        self.parser.parse(fh)

    def option_count(self):
        """
        Return the total amount of options available.

        :returns: Total option count.
        :rtype: :class:`int`
        """
        return self.parser.option_count()

    def dump_compentition_market_prices(self, name, fh):
        """
        Dump a competitions market prices to a CSV formatted file.

        .. note::

            CSV fields are:
            Game,Closes,Name,Calculated Market Percentage

        :param name: Competition name that you are dumping market stats for.
        :type name: :class:`str`
        :param fh: Write file handler to write to.
        :type fh: :class:`file`
        """
        fieldnames = [
            "Game",
            "Closes",
            "Name",
            "Calculated Market Percentage",
        ]

        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        comps = sorted(
            self.parser.get_competitions(name),
            key=lambda x: x.closes
        )
        for each in comps:
            market_price = calc_market_percentage(
                sel.odds
                for sel in each.get_selections()
                if sel.odds > 0
            )
            writer.writerow(
                {
                    "Game": each.game,
                    "Closes": each.closes,
                    "Name": each.name,
                    "Calculated Market Percentage": market_price,
                }
            )

    def summary(self):
        return (
            "Available options: {options_count}".format(
                options_count=self.option_count(),
            )
        )


if __name__ == "__main__":
    import argparse
    import os
    import sys

    args = argparse.ArgumentParser(
        description="Generate a stat reports."
    )

    args.add_argument(
        "filename",
        metavar="FILENAME",
        type=argparse.FileType(),
        help="File containing statics. Supported files as JSON and XML."
    )

    args.add_argument(
        "--comp-dump",
        metavar="FILENAME",
        type=argparse.FileType("w"),
        help="File to dump competition market prices to. --comp must "
             "be given for dump to work."
    )

    args.add_argument(
        "--comp",
        metavar="NAME",
        help="Competition name to search for."
    )

    args.add_argument(
        "--options",
        action="store_true",
        help="Show how many options are available."
    )

    ns = args.parse_args()

    if ns.comp_dump and not ns.comp:
        print("Missing `--comp` argument.")
        sys.exit(os.EX_USAGE)

    # work out what type of parser we need to use.
    if ns.filename.name.endswith(".json"):
        parser = JSONParser()
    elif ns.filename.name.endswith(".xml"):
        parser = XMLParser()
    else:
        print("Unsupported file format for {!r}".format(ns.filename.name))
        sys.exit(os.EX_DATAERR)

    reporter = Reporter(parser=parser)
    reporter.load(ns.filename)

    # bump market stats
    if ns.comp and ns.comp_dump:
        reporter.dump_compentition_market_prices(ns.comp, ns.comp_dump)

    # Print out the option count.
    if ns.options is True:
        print("Available options: {}".format(reporter.option_count()))
