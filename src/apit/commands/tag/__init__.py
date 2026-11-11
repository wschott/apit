import logging
from argparse import BooleanOptionalAction
from collections.abc import Iterable
from pathlib import Path
from typing import override

from .command import execute
from apit.core.options import Options
from apit.core.result import Result
from apit.commands.command import Command
from apit.commands.common_cli_parser_arguments import add_path_argument
from apit.commands.common_cli_parser_arguments import add_verbose_argument
from apit.core.metadata_loader import MetadataLoader
from apit.infra.metadata_source.itunes_metadata_parser import ItunesMetadataParser
from apit.infra.metadata_source.itunes_store_loader import ItunesStoreLoader
from apit.infra.metadata_source.local_file_loader import LocalFileLoader
from apit.utils.http import is_url

__all__ = ["TagCommand"]


class TagCommand(Command):
    @staticmethod
    @override
    def setup_cli_parser(subparsers):
        tag_command = subparsers.add_parser(
            "tag",
            help="tag files in PATH",
            description="tag files in PATH using Apple Music metadata",
        )
        tag_command.set_defaults(func=TagCommand.execute)

        add_verbose_argument(tag_command)
        tag_command.add_argument(
            "-b",
            "--backup",
            dest="has_backup_flag",
            action="store_true",
            default=False,
            help="create backup before updating tags (default: %(default)s)",
        )
        tag_command.add_argument(
            "--artwork",
            dest="has_embed_artwork_flag",
            action=BooleanOptionalAction,
            default=True,
            help="download and embed artwork in files",
        )
        tag_command.add_argument(
            "--artwork-size",
            dest="artwork_size",
            metavar="SIZE",
            type=int,
            default=600,
            help="set artwork size for download (default: %(default)s)",
        )
        add_path_argument(tag_command)
        tag_command.add_argument(
            "source",
            metavar="SOURCE",
            help="URL to Apple Music album for metadata download OR file with already downloaded metadata",
        )

    @staticmethod
    @override
    def execute(files: Iterable[Path], options: Options) -> Result:
        metadata_json = TagCommand._get_metadata(options.source)

        return execute(
            files=files,
            verbose_level=options.verbose_level,
            should_backup=options.has_backup_flag,
            should_embed_artwork=options.has_embed_artwork_flag,
            artwork_size=options.artwork_size,
            metadata_json=metadata_json,
            metadata_parser=ItunesMetadataParser(),
        )

    @staticmethod
    def _get_metadata(source: str) -> str:
        logging.info("Input source: %s", source)
        metadata_loader: MetadataLoader = (
            ItunesStoreLoader() if is_url(source) else LocalFileLoader()
        )
        return metadata_loader.load(source)
