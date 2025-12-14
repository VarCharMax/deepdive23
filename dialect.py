"""_summary_"""

import os
import re
import sys
import webbrowser
import requests
from basehtmlprocessor import BaseHTMLProcessor


class Dialectizer(BaseHTMLProcessor):
    """_summary_

    Args:
        BaseHTMLProcessor (_type_): _description_

    Returns:
        _type_: _description_
    """

    # tuple consisting of one or more tuples with two str members.
    subs: tuple[tuple[str, str], ...] = ()

    def reset(self) -> None:
        """extend (called from __init__ in ancestor)"""
        # Reset all data attributes
        self.verbatim = 0
        BaseHTMLProcessor.reset(self)

    def start_pre(self, attrs) -> None:
        """called for every <pre> tag in HTML source"""
        # Increment verbatim mode count, then handle tag like normal
        self.verbatim += 1
        self.handle_starttag("pre", attrs)

    def end_pre(self):
        """called for every </pre> tag in HTML source"""
        # Decrement verbatim mode count
        self.handle_endtag("pre")
        self.verbatim -= 1

    def handle_data(self, data) -> None:
        """
        override
        called for every block of text in HTML source
        """

        def process(text) -> str:
            """called from handle_data"""
            # Process text block by performing series of regular expression
            # substitutions (actual substitions are defined in descendant)
            for frompattern, topattern in self.subs:
                text = re.sub(frompattern, topattern, text)
            return text

        # If in verbatim mode, or processing a script, save text unaltered;
        # otherwise process the text with a series of substitutions
        self.pieces.append((self.verbatim or self.in_script) and data or process(data))


class ChefDialectizer(Dialectizer):
    """
    convert HTML to Swedish Chef-speak
    based on the classic chef.x, copyright (c) 1992, 1993 John Hagerman
    """

    subs = (
        (r"a([nu])", r"u\1"),
        (r"A([nu])", r"U\1"),
        (r"a\B", r"e"),
        (r"A\B", r"E"),
        (r"en\b", r"ee"),
        (r"\Bew", r"oo"),
        (r"\Be\b", r"e-a"),
        (r"\be", r"i"),
        (r"\bE", r"I"),
        (r"\Bf", r"ff"),
        (r"\Bir", r"ur"),
        (r"(\w*?)i(\w*?)$", r"\1ee\2"),
        (r"\bow", r"oo"),
        (r"\bo", r"oo"),
        (r"\bO", r"Oo"),
        (r"the", r"zee"),
        (r"The", r"Zee"),
        (r"th\b", r"t"),
        (r"\Btion", r"shun"),
        (r"\Bu", r"oo"),
        (r"\BU", r"Oo"),
        (r"v", r"f"),
        (r"V", r"F"),
        (r"w", r"w"),
        (r"W", r"W"),
        (r"([a-z])[.]", r"\1. Bork Bork Bork!"),
    )


class FuddDialectizer(Dialectizer):
    """convert HTML to Elmer Fudd-speak"""

    subs = (
        (r"[rl]", r"w"),
        (r"qu", r"qw"),
        (r"th\b", r"f"),
        (r"th", r"d"),
        (r"n[.]", r"n, uh-hah-hah-hah."),
    )


class OldeDialectizer(Dialectizer):
    """convert HTML to mock Middle English"""

    subs = (
        (r"i([bcdfghjklmnpqrstvwxyz])e\b", r"y\1"),
        (r"i([bcdfghjklmnpqrstvwxyz])e", r"y\1\1e"),
        (r"ick\b", r"yk"),
        (r"ia([bcdfghjklmnpqrstvwxyz])", r"e\1e"),
        (r"e[ea]([bcdfghjklmnpqrstvwxyz])", r"e\1e"),
        (r"([bcdfghjklmnpqrstvwxyz])y", r"\1ee"),
        (r"([bcdfghjklmnpqrstvwxyz])er", r"\1re"),
        (r"([aeiou])re\b", r"\1r"),
        (r"ia([bcdfghjklmnpqrstvwxyz])", r"i\1e"),
        (r"tion\b", r"cioun"),
        (r"ion\b", r"ioun"),
        (r"aid", r"ayde"),
        (r"ai", r"ey"),
        (r"ay\b", r"y"),
        (r"ay", r"ey"),
        (r"ant", r"aunt"),
        (r"ea", r"ee"),
        (r"oa", r"oo"),
        (r"ue", r"e"),
        (r"oe", r"o"),
        (r"ou", r"ow"),
        (r"ow", r"ou"),
        (r"\bhe", r"hi"),
        (r"ve\b", r"veth"),
        (r"se\b", r"e"),
        (r"'s\b", r"es"),
        (r"ic\b", r"ick"),
        (r"ics\b", r"icc"),
        (r"ical\b", r"ick"),
        (r"tle\b", r"til"),
        (r"ll\b", r"l"),
        (r"ould\b", r"olde"),
        (r"own\b", r"oune"),
        (r"un\b", r"onne"),
        (r"rry\b", r"rye"),
        (r"est\b", r"este"),
        (r"pt\b", r"pte"),
        (r"th\b", r"the"),
        (r"ch\b", r"che"),
        (r"ss\b", r"sse"),
        (r"([wybdp])\b", r"\1e"),
        (r"([rnt])\b", r"\1\1e"),
        (r"from", r"fro"),
        (r"when", r"whan"),
    )


def translate(url, dialectname="chef") -> str:
    """
    fetch URL and translate using dialect
    dialect in ("chef", "fudd", "olde")
    """

    html = ""
    try:
        response = requests.get(url, timeout=30)
        html = response.text
    except (requests.ConnectionError, requests.RequestException) as e:
        print(f"Connection error: {e.__doc__}")
        sys.exit()

    if html:
        parsername = f"{dialectname.capitalize()}Dialectizer"
        parserclass = globals()[parsername]
        parser = parserclass(convert_charrefs=False)
        parser.feed(html)
        parser.close()
        return parser.output()

    print("URL contains no data.")
    return html


def test(url) -> None:
    """test all dialects against URL"""
    for dialect in ("chef", "fudd", "olde"):
        outfile = f"{dialect}.html"
        with open(outfile, "w", encoding="utf-8") as fsock:
            fsock.write(translate(url, dialect))
        try:
            if os.name == "posix":
                chrome_path = "open -na /Applications/Google\\ Chrome.app --args %s"
                # safari_path = "open -na /Applications/Safari.app %s"
                browser = webbrowser.get(chrome_path)
                outfile = "file://" + os.path.abspath(outfile)
                browser.open_new_tab(outfile)
            else:
                webbrowser.open_new(outfile)
        except webbrowser.Error:
            pass


if __name__ == "__main__":
    test("https://modartt.com/")
