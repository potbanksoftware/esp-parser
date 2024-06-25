#!/usr/bin/env python3
#
#  _tes4.py
"""
TES4 record type.
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
from typing import Iterator, List, NamedTuple, Type

# 3rd party
from typing_extensions import Self

# this package
from esp_parser.types import BytesRecordType, CStringRecord, Record, RecordType
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["TES4"]


class TES4(Record):
	"""
	Record for plugin info.
	"""

	class HEDR(NamedTuple):
		"""
		Header.

		Contains additional details about the plugin.
		"""

		version: float  # 0.94 in most files; 1.7 in recent versions of Update.esm.

		#: Number of records and groups (not including TES4 record itself).
		num_records: int

		#: Next available object ID.
		next_object_id: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x0c\x00"  # size field
			return cls(*struct.unpack("<fI4s", raw_bytes.read(12)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"HEDR\x0c\x00" + struct.pack("<fI4s", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(HEDR)

	# class OFST(RecordType):
	# 	"""
	# 	Unknown.
	# 	"""

	# class DELE(RecordType):
	# 	"""
	# 	Unknown.
	# 	"""

	class CNAM(CStringRecord):
		"""
		The plugin's author.

		Max 511 bytes.
		"""

	class SNAM(CStringRecord):
		"""
		The plugin's description.

		Max 511 bytes.
		"""

	class MAST(CStringRecord):
		"""
		Name of a master plugin.

		May be repeated.
		"""

	class DATA(BytesRecordType):  # noqa: D106  # TODO

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			return cls(raw_bytes.read(10))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA" + bytes(self)

	class ONAM(List[bytes], RecordType):
		"""
		Form Overrides.

		Overridden records. An array of :class:`~.REFR`, :class:`~.ACHR`, :class:`~.ACRE`,
		:class:`~.PMIS`, :class:`~.PBEA`, :class:`~.PGRE`, :class:`~.LAND` and :class:`~.NAVM` records.
		"""

		def __repr__(self) -> str:
			return f"{self.__class__.__qualname__}({super().__repr__()})"

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size = struct.unpack("<H", raw_bytes.read(2))[0]

			buf = raw_bytes.read(size)

			count = size // 4
			assert not size % 4

			return cls(struct.unpack('<' + ("4s" * count), buf))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			body = b"".join(self)

			size = len(body)
			assert len(self) * 4 == size
			return b"MODS" + struct.pack("<H", size) + body

	# class SCRN(RecordType):
	# 	"""
	# 	screenshot.
	# 	"""

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

			if record_type in {b"CNAM", b"DATA", b"DELE", b"HEDR", b"MAST", b"OFST", b"ONAM", b"SCRN", b"SNAM"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
