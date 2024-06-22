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
import struct
from io import BytesIO
from typing import Iterator, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID, OBND
from esp_parser.types import CStringRecord, Record, RecordType, Uint16Record

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
	class DODT(RecordType):
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

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x24\x00"  # size field
			return cls(*struct.unpack("<fffffffBB2s4s", raw_bytes.read(36)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			packed = struct.pack(
					"<fffffffBB2s4s",
					self.min_width,
					self.max_width,
					self.min_height,
					self.max_height,
					self.depth,
					self.shininess,
					self.parallax_scale,
					self.parallax_passes,
					self.flags,
					self.color,
					)

			return b"DODT\x24\x00" + packed

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
			elif record_type in {
					b"TX00",
					b"TX01",
					b"TX02",
					b"TX03",
					b"TX04",
					b"TX05",
					b"DODT",
					b"DNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
