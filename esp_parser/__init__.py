#!/usr/bin/env python3
#
#  __init__.py
"""
Parser and unparser for Bethesda ESP files.
"""
#
#  Copyright © 2024 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2024 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

# stdlib
from io import BytesIO
from typing import TYPE_CHECKING, Iterator, Union

# this package
from esp_parser.types import RecordType

if TYPE_CHECKING:
	# this package
	from esp_parser.group import Group

__all__ = ["parse_esp"]


def parse_esp(raw_bytes: BytesIO) -> Iterator[Union[RecordType, "Group"]]:
	"""
	Recursively parse an ESP file.
	"""

	# this package
	from esp_parser import group, records
	while True:
		record_type = raw_bytes.read(4)
		if not record_type:
			break

		if record_type == b"GRUP":
			yield group.Group.parse(raw_bytes)
		elif record_type in {
				b"TES4",
				b"SOUN",
				b"DIAL",
				b"INFO",
				b"SCPT",
				b"TACT",
				b"WRLD",
				b"CELL",
				b"REFR",
				b"QUST",
				b"NPC_",
				b"ACHR",
				}:
			yield getattr(records, record_type.decode()).parse(record_type, raw_bytes)
		else:
			raise NotImplementedError(record_type)
