import abc
import json
from lxml import etree


class IStatsParser(object):
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


class JSONParser(IStatsParser):
    """
    JSON stats file parser.
    """
    def parse(self, fh):
        self.data = json.load(fh, parse_float=True)

    def option_count(self):
        options = self.data.get("options", {})
        return len(options.get("option", []))


class XMLParser(IStatsParser):
    """
    XML stats file parser.
    """
    def parse(self, fh):
        self.data = etree.parse(fh).getroot()

    def option_count(self):
        return int(self.data.xpath("count(//options/option)"))


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

    def summary(self):
        options = self.parser.option_count()
        return (
            "Available options: {options_count}".format(
                options_count=options,
            )
        )


if __name__ == "__main__":
    import argparse

    args = argparse.ArgumentParser(
        description="Generate a stat reports."
    )

    args.add_argument(
        "filename",
        metavar="FILENAME",
        type=argparse.FileType(),
        help="File containing statics. Supported files as JSON and XML."
    )

    ns = args.parse_args()

    if ns.filename.name.endswith(".json"):
        parser = JSONParser()
    elif ns.filename.name.endswith(".xml"):
        parser = XMLParser()
    else:
        print("Unsupported file format for {!r}".format(ns.filename.name))
        sys.exit(os.EX_DATAERR)

    reporter = Reporter(parser=parser)
    reporter.load(ns.filename)

    print(reporter.summary())
