#!/usr/bin/env python3
#
#  _qust.py
"""
QUST record type.
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
from esp_parser.subrecords import EDID, Script
from esp_parser.types import CStringRecord, FormIDRecord, Int16Record, Int32Record, Record, RecordType, Uint8Record
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["QUST"]


class QUST(Record):
	"""
	Quest.
	"""

	class SCRI(FormIDRecord):
		"""
		Form ID of a :class:`~.SCPT` record.
		"""

	class FULL(CStringRecord):
		"""
		Quest name.
		"""

	class ICON(CStringRecord):
		"""
		Large Icon Filename.
		"""

	class MICO(CStringRecord):
		"""
		Small Icon FIlename.
		"""

	class DATA(NamedTuple):  # noqa: D106  # TODO
		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/QUST.html
		priority: int
		unused: bytes
		quest_delay: float = 0.0

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<BB2sf", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA\x08\x00" + struct.pack("<BB2sf", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(DATA)

	class INDX(Int16Record):
		"""
		Stage index.
		"""

	class QSDT(Uint8Record):
		"""
		Stage flags.

		See https://tes5edit.github.io/fopdoc/FalloutNV/Records/QUST.html
		"""

	class CNAM(CStringRecord):
		"""
		Log Entry.
		"""

	class QOBJ(Int32Record):
		"""
		Objective index.
		"""

	class NNAM(CStringRecord):
		"""
		Description.
		"""

	class QSTA(NamedTuple):
		"""
		Quest Target.
		"""

		target: bytes
		"""
		The quest target.

		Form ID of a :class:`~.REFR`, :class:`~.PGRE`,
		:class:`~.PMIS`, :class:`~.ACRE` or :class:`~.ACHR` record.
		"""

		flags: int
		unused: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<4sB3s", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"QSTA\x08\x00" + struct.pack("<4sB3s", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(QSTA)

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
					b"SCRI",
					b"FULL",
					b"ICON",
					b"MICO",
					b"DATA",
					b"INDX",
					b"QSDT",
					b"CNAM",
					b"QOBJ",
					b"NNAM",
					b"QSTA",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in {b"SCHR", b"SCDA", b"SCTX", b"SCRO", b"SLSD", b"SCVR"}:
				yield getattr(Script, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
