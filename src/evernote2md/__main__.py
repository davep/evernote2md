"""Main utility code."""

##############################################################################
# Allow future magic.
from __future__ import annotations

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from typing import Final, NamedTuple

##############################################################################
# Markdownift imports.
from bs4.element import Tag
from markdownify import MarkdownConverter  # type: ignore

##############################################################################
# Timezime help.
from pytz import timezone


##############################################################################
class EvernoteConverter(MarkdownConverter):
    """Markdownify class for pulling data out of Evernote HTML files."""

    def __init__(self) -> None:
        """Initialise the object."""
        super().__init__()
        self.found_title = ""
        self.found_tags: set[str] = set()
        self.time_created = ""
        self.time_updated = ""
        self.latitide = ""
        self.longitude = ""
        self.altitude = ""
        self.photos: list[str] = []

    def convert_meta(self, el: Tag, text: str, convert_as_inline: bool) -> str:
        """Handle meta tags."""
        del text, convert_as_inline
        if not isinstance(item_property := el.get("itemprop"), str) or not isinstance(
            content := el.get("content"), str
        ):
            return ""
        if item_property == "tag":
            self.found_tags.add(content)
        elif item_property == "title":
            self.found_title = content
        elif item_property == "created":
            self.time_created = content
        elif item_property == "updated":
            self.time_updated = content
        elif item_property == "latitude":
            self.latitide = content
        elif item_property == "longitude":
            self.longitude = content
        elif item_property == "altitude":
            self.altitude = content
        return ""

    def convert_div(self, el: Tag, text: str, convert_as_inline: bool) -> str:
        """Handle div tags."""
        del convert_as_inline
        try:
            if "para" in el["class"]:
                return f"{text.strip()}\n"
        except KeyError:
            pass
        return ""

    def convert_img(self, el: Tag, text: str, convert_as_inline: bool) -> str:
        """Handle img tags."""
        try:
            self.photos += [el["src"]]
        except KeyError:
            pass
        return super().convert_img(el, text, convert_as_inline)


##############################################################################
TIMEZONE: Final[str] = "Europe/London"
"""The timezone to use when presenting times."""


##############################################################################
class EvernoteEntry(NamedTuple):
    """Holds all the details of a journal entry in Evernote."""

    title: str
    """The title for the journal entry."""
    text: str
    """The text of the journal entry."""
    tags: set[str]
    """The tags for the journal entry."""
    time_created: datetime
    """The time the journal entry was created."""
    time_updated: datetime
    """The time the journal entry was last updated."""
    latitude: float | None
    """The latitude of the journal entry."""
    longitude: float | None
    """The longitude of the journal entry."""
    altitude: float | None
    """The altitude of the journal entry."""
    photos: list[str]
    """The list of photos associated with the journal entry."""

    @classmethod
    def from_html(cls, html: str) -> EvernoteEntry:
        """Create the Evernote entry from some HTML.

        Args:
            html: The HTML that contains the Evernote journal entry.

        Returns:
            A populated `EvernoteEntry` instance.
        """
        data_parser = EvernoteConverter()
        markdown = data_parser.convert(html).strip()
        return cls(
            data_parser.found_title,
            markdown,
            data_parser.found_tags,
            datetime.strptime(data_parser.time_created, "%Y%m%dT%H%M%S%z").astimezone(
                timezone(TIMEZONE)
            ),
            datetime.strptime(data_parser.time_updated, "%Y%m%dT%H%M%S%z").astimezone(
                timezone(TIMEZONE)
            ),
            float(data_parser.latitide) if data_parser.latitide else None,
            float(data_parser.longitude) if data_parser.longitude else None,
            float(data_parser.altitude) if data_parser.altitude else None,
            data_parser.photos,
        )

    @property
    def markdown_directory(self) -> Path:
        """The directory that this entry should be created in."""
        return Path(self.time_created.strftime("%Y/%m/%d/"))

    @property
    def markdown_attachment_directory(self) -> Path:
        """The location of the attachment directory associated with this journal entry."""
        return self.markdown_directory / "attachments"

    @property
    def markdown_file(self) -> Path:
        """The path to the Markdown file that should be made for this journal."""
        return self.markdown_directory / Path(
            self.time_created.strftime("%Y-%m-%d-%H-%M-%S-%f-%Z.md")
        )


##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments.

    Returns:
        The command line arguments.
    """
    parser = ArgumentParser(
        prog="evernote2md",
        description="A tool for converting an Evernote export file into a daily-note Markdown collection",
    )

    parser.add_argument(
        "evernote_files",
        help="The directory that contains the unzipped Evernote export",
    )
    parser.add_argument(
        "target_directory",
        help="The directory where the Markdown files will be created",
    )

    return parser.parse_args()


##############################################################################
def export(evernote: Path, daily: Path) -> None:
    """Export the Evernote files to Markdown-based daily notes.

    Args:
        evernote: The source Evernote location.
        daily: The target daily location.
    """
    for source in evernote.glob("*.html"):
        if source.name != "Evernote_index.html":
            entry = EvernoteEntry.from_html(source.read_text())
            print(f"Importing {entry.title} -> {entry.markdown_file}")
            if entry.photos:
                print(f"\t{entry.photos}")


##############################################################################
def main() -> None:
    """Main entry point for the utility."""
    arguments = get_args()
    if not (evernote := Path(arguments.evernote_files)).is_dir():
        print("Evernote source needs to be a directory")
        exit(1)
    if not (daily := Path(arguments.target_directory)).is_dir():
        print("The target needs to be an existing directory")
        exit(1)
    export(evernote, daily)


##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
