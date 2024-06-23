#!/usr/bin/env python3
#
#  _spel.py
"""
SPEL record type.
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
from enum import IntEnum
from io import BytesIO
from typing import Iterator, NamedTuple, Tuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import CTDA, EDID
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType, StructRecord
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["SPEL"]


class SPEL(Record):
	"""
	Actor Effect.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	@attrs.define
	class SPIT(StructRecord):
		"""
		Effect type, cost etc.
		"""

		type: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/SPEL.html

		#: Unused
		cost: int

		#: Unused
		level: int

		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/SPEL.html

		unused: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<IIIB3s", 16

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return ("type", "cost", "level", "flags", "unused")

	class EFID(FormIDRecord):
		"""
		Base effect.

		Form ID of a :class:`~.MGEF` record.
		"""

	class EfitTypeEnum(IntEnum):
		"""
		Enum for ``SPEL.EFIT``.
		"""

		Self = 0
		Touch = 1
		Target = 2

	class EFIT(NamedTuple):
		"""
		Effect Data.
		"""

		magnitude: int
		area: int
		duration: int
		type: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Effect.html
		actor_value: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Effect.html

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x14\x00"  # size field
			return cls(*struct.unpack("<IIIIi", raw_bytes.read(20)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"EFIT" + struct.pack("<HIIIIi", 20, *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(EFIT)

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
			elif record_type == b"CTDA":
				yield CTDA.parse(raw_bytes)
			elif record_type in {b"FULL", b"SPIT", b"EFID", b"EFIT"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
