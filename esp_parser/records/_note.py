#!/usr/bin/env python3
#
#  _note.py
"""
NOTE record type.
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
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID, OBND, Model
from esp_parser.types import BytesRecordType, CStringRecord, FormIDRecord, Record, RecordType, Uint8Record

__all__ = ["NOTE"]


class NOTE(Record):
	"""
	Note.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class ICON(CStringRecord):
		"""
		Large Icon Filename.
		"""

	class MICO(CStringRecord):
		"""
		Small Icon FIlename.
		"""

	class YNAM(FormIDRecord):
		"""
		Sound - Pick Up.

		FormID of a SOUN record.
		"""

	class ZNAM(FormIDRecord):
		"""
		Sound - Drop.

		FormID of a SOUN record.
		"""

	class DATA(Uint8Record):
		"""
		Type.

		Enum - see values below.
		"""

	class ONAM(FormIDRecord):
		"""
		Quest.

		FormID of a QUST record.
		"""

	class XNAM(CStringRecord):
		"""
		Texture.
		"""

	class TNAM(BytesRecordType):
		"""
		Text / Topic.

		A text string, or the Form ID of a :class:`~.DIAL` record (in which case 4-bytes long).
		"""

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size = struct.unpack("<H", raw_bytes.read(2))[0]
			if size == 4:
				# Form ID
				return cls(raw_bytes.read(4))
			else:

				buf = []

				while True:
					char = raw_bytes.read(1)
					if char == b"\x00":
						break
					buf.append(char)

				return cls(b"".join(buf))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			class_qualname = self.__class__.__name__.encode()
			if len(self) == 4:
				return class_qualname + struct.pack("<H", len(self)) + self
			else:
				return class_qualname + struct.pack("<H", len(self) + 1) + self + b"\x00"

	class SNAM(FormIDRecord):
		"""
		Sound / NPC.

		Form ID of a :class:`~.SOUN` or :class:`~.NPC_` record.
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
					b"FULL",
					b"ICON",
					b"MICO",
					b"YNAM",
					b"ZNAM",
					b"DATA",
					b"ONAM",
					b"XNAM",
					b"TNAM",
					b"SNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			else:
				breakpoint()
				raise NotImplementedError(record_type)
