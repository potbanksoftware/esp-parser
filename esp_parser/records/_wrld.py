#!/usr/bin/env python3
#
#  _wrld.py
"""
WRLD record type.
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
from typing import Iterator, NamedTuple, Type

# 3rd party
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID
from esp_parser.types import CStringRecord, Float32Record, FormIDRecord, Record, RecordType, Uint8Record
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["WRLD"]


class WRLD(Record):
	"""
	Worldspace.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class XEZN(FormIDRecord):
		"""
		Encounter Zone.

		Form ID of an :class:`~.ECZN` record.
		"""

	class WNAM(FormIDRecord):
		"""
		Parent worldspace.

		Form ID of a :class:`~.WRLD` record.
		"""

	class PNAM(NamedTuple):
		"""
		Parent worldspace flags.
		"""

		flags: int
		unknown: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x02\x00"  # size field
			return cls(*struct.unpack("<Bs", raw_bytes.read(2)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"PNAM\x02\x00" + struct.pack("<B", self.flags) + self.unknown

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class CNAM(FormIDRecord):
		"""
		Climate.

		Form ID of a :class:`~.CLMT` record.
		"""

	class NAM2(FormIDRecord):
		"""
		Water.

		Form ID of a :class:`~.WATR` record.
		"""

	class NAM3(FormIDRecord):
		"""
		LOD water type.

		Form ID of a :class:`~.WATR` record.
		"""

	class NAM4(Float32Record):
		"""
		LOD water height.
		"""

	class DNAM(NamedTuple):
		"""
		Land Data.
		"""

		default_land_height: float
		default_water_height: float

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""
			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack(">ff", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"DNAM\x08\x00" + struct.pack(">ff", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class ICON(CStringRecord):
		"""
		Large icon filename.
		"""

	class MICO(CStringRecord):
		"""
		Small icon filename.
		"""

	class MNAM(NamedTuple):
		"""
		Map Data.
		"""

		useable_x_size: int
		useable_y_size: int
		nw_x_coord: int
		nw_y_coord: int
		se_x_coord: int
		se_y_coord: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x10\x00"  # size field
			return cls(*struct.unpack(">iihhhh", raw_bytes.read(16)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"MNAM\x10\x00" + struct.pack(">iihhhh", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class ONAM(NamedTuple):
		"""
		World Map Offset Data.
		"""

		world_map_scale: float
		cell_x_offset: float
		cell_y_offset: float

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""
			assert raw_bytes.read(2) == b"\x0c\x00"  # size field
			return cls(*struct.unpack(">fff", raw_bytes.read(12)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"ONAM\x0c\x00" + struct.pack(">fff", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class INAM(FormIDRecord):
		"""
		Image space.

		Form ID of an :class:`~.IMGS` record.
		"""

	class DATA(Uint8Record):
		"""
		Flags.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/WRLD.html
		"""

	class NAM0(NamedTuple):
		"""
		Min Object Bounds.
		"""

		x: float
		y: float

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""
			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<ff", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"NAM0\x08\x00" + struct.pack("<ff", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class NAM9(NAM0):
		"""
		Max Object Bounds.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"NAM9\x08\x00" + struct.pack("<ff", *self)

	RecordType.register(PNAM)
	RecordType.register(MNAM)
	RecordType.register(DNAM)
	RecordType.register(ONAM)
	RecordType.register(NAM0)
	RecordType.register(NAM9)

	class ZNAM(FormIDRecord):
		"""
		Music.

		Form ID of a :class:`~.MUSC` record.
		"""

	class NNAM(CStringRecord):
		"""
		Canopy Shadow.
		"""

	class XNAM(CStringRecord):
		"""
		Water Noise Texture.
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
			elif record_type in {
					b"CNAM",
					b"DATA",
					b"DNAM",
					b"FULL",
					b"ICON",
					b"INAM",
					b"MICO",
					b"MNAM",
					b"NAM0",
					b"NAM2",
					b"NAM3",
					b"NAM4",
					b"NAM9",
					b"NNAM",
					b"ONAM",
					b"PNAM",
					b"WNAM",
					b"XEZN",
					b"XNAM",
					b"ZNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
