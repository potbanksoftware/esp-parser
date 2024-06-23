#!/usr/bin/env python3
#
#  _txst.py
"""
TXST record type.
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

# stdlib
from io import BytesIO
from typing import Iterator, Tuple

# 3rd party
import attrs

# this package
from esp_parser.subrecords import EDID, OBND
from esp_parser.types import CStringRecord, Record, RecordType, StructRecord, Uint16Record

__all__ = ["TXST"]


class TXST(Record):
	"""
	Texture set.
	"""

	class TX00(CStringRecord):
		"""
		Base Image / Transparency.

		The alpha channel holds the transparency data.
		"""

	class TX01(CStringRecord):
		"""
		Normal Map / Specular.

		The alpha channel holds the specular data.
		"""

	class TX02(CStringRecord):
		"""
		Environment Map Mask.
		"""

	class TX03(CStringRecord):
		"""
		Glow Map.
		"""

	class TX04(CStringRecord):
		"""
		Parallax Map.
		"""

	class TX05(CStringRecord):
		"""
		Enviroment Map.
		"""

	@attrs.define
	class DODT(StructRecord):
		"""
		Decal Data.
		"""

		min_width: float
		max_width: float
		min_height: float
		max_height: float
		depth: float
		shininess: float
		parallax_scale: float
		parallax_passes: int
		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/DODT.html
		color: bytes  # TODO: comment for rgba

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<fffffffBB2s4s", 36

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return (
					"min_width",
					"max_width",
					"min_height",
					"max_height",
					"depth",
					"shininess",
					"parallax_scale",
					"parallax_passes",
					"flags",
					"color",
					)

	class DNAM(Uint16Record):
		"""
		Flags.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/TXST.html
		"""

	@classmethod
	def parse_subrecords(cls, raw_bytes: BytesIO) -> Iterator[RecordType]:
		"""
		Parse this record's subrecords.

		:param raw_bytes: Raw bytes for this record's subrecords
		"""

		while True:
			record_type = raw_bytes.read(4)
			if not record_type:
				break

			if record_type == b"EDID":
				yield EDID.parse(raw_bytes)
			elif record_type == b"OBND":
				yield OBND.parse(raw_bytes)
			elif record_type in {b"TX00", b"TX01", b"TX02", b"TX03", b"TX04", b"TX05", b"DODT", b"DNAM"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
