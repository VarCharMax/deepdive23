"""_summary_

Returns:
    _type_: _description_
"""

# pylint: disable=W0641

import html.entities
import html.parser


class BaseHTMLProcessor(html.parser.HTMLParser):
    """_summary_

    Args:
        HTMLParser (_type_): _description_
    """

    def reset(self) -> None:
        """_summary_"""
        # extend (called by HTMLParser.__init__)
        self.pieces = []
        html.parser.HTMLParser.reset(self)

    def handle_starttag(self, tag, attrs) -> None:
        """called for each start tag
        # attrs is a list of (attr, value) tuples
        # e.g. for <pre class="screen">, tag="pre", attrs=[("class", "screen")]
        # Ideally we would like to reconstruct original tag and attributes, but
        # we may end up quoting attribute values that weren't quoted in the source
        # document, or we may change the type of quotes around the attribute value
        # (single to double quotes).
        # Note that improperly embedded non-HTML code (like client-side Javascript)
        # may be parsed incorrectly by the ancestor, causing runtime script errors.
        # All non-HTML code must be enclosed in HTML comment tags (<!-- code -->)
        # to ensure that it will pass through this parser unaltered (in handle_comment).
        """
        strattrs = "".join([f' {key}="{value}"' for key, value in attrs])
        self.pieces.append(f"<{locals()['tag']}{locals()['strattrs']}>")

    def handle_endtag(self, tag) -> None:
        """
        # called for each end tag, e.g. for </pre>, tag will be "pre"

        Args:
            tag (_type_): _description_
        """
        # Reconstruct the original end tag.
        self.pieces.append(f"</{locals()['tag']}>")

    def handle_charref(self, name) -> None:
        """
        called for each character reference, e.g. for "&#160;", ref will be "160"

        Args:
            ref (_type_): _description_
        """

        # Reconstruct the original character reference.
        self.pieces.append(f"&#{locals()['name']};")

    def handle_entityref(self, name) -> None:
        """called for each entity reference, e.g. for "&copy;", name will be "copy"""
        # Reconstruct the original entity reference.
        self.pieces.append(f"&{locals()['name']}")
        # standard HTML entities are closed with a semicolon; other entities are not
        if name in html.entities.html5:
            self.pieces.append(";")

    def handle_data(self, data) -> None:
        """called for each block of plain text, i.e. outside of any tag and
        # not containing any character or entity references"""
        # Store the original text verbatim.
        self.pieces.append(data)

    def handle_comment(self, data) -> None:
        """called for each HTML comment, e.g. <!-- insert Javascript code here -->
        # Reconstruct the original comment.
        # It is especially important that the source document enclose client−side
        # code (like Javascript) within comments so it can pass through this
        # processor undisturbed; see comments in unknown_starttag for details."""
        self.pieces.append(f"<!--{locals()['data']}-->")

    def handle_pi(self, data) -> None:
        """called for each processing instruction, e.g. <?instruction>"""
        # Reconstruct original processing instruction.
        self.pieces.append(f"<?{locals()['data']}>")

    def handle_decl(self, decl) -> None:
        """
        called for the DOCTYPE, if present, e.g.
        <!DOCTYPE html PUBLIC "−//W3C//DTD HTML 4.01 Transitional//EN"
          "http://www.w3.org/TR/html4/loose.dtd">
        """
        # Reconstruct original DOCTYPE
        self.pieces.append(f"<!{locals()['decl']}>")

    def output(self) -> str:
        """Return processed HTML as a single string"""
        return "".join(self.pieces)
