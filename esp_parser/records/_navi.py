#!/usr/bin/env python3
#
#  _navi.py
"""
NAVI record type.
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
from typing import Iterator, List, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID
from esp_parser.types import Record, RecordType, Uint32Record

__all__ = ["NAVI"]


class NAVI(Record):
	"""
	Navigation Mesh Info Map.
	"""

	class NVER(Uint32Record):
		"""
		Version.
		"""

	@attrs.define
	class NVMI(RecordType):
		"""
		Navigation Map Info.
		"""

		unknown: bytes
		#: Form ID of a :class:`~.NAVM` record.
		navmesh: bytes

		#: Form ID of a :class:`~.CELL` or :class:`~.WRLD` record.
		location: bytes
		grid_x: int
		grid_y: int
		unknown_: List[int]

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size = struct.unpack("<H", raw_bytes.read(2))[0]
			unknown = raw_bytes.read(4)
			navmesh = raw_bytes.read(4)
			location = raw_bytes.read(4)
			grid_x, grid_y = struct.unpack("<hh", raw_bytes.read(4))
			unknown2_size = size - 16
			unknown2 = list(struct.unpack(f"<{unknown2_size}B", raw_bytes.read(unknown2_size)))
			return cls(
					unknown,
					navmesh,
					location,
					grid_x,
					grid_y,
					unknown2,
					)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			unknown2_size = len(self.unknown_)
			size = unknown2_size + 16

			packed = struct.pack(
					f"<H4s4s4shh{unknown2_size}B",
					size,
					self.unknown,
					self.navmesh,
					self.location,
					self.grid_x,
					self.grid_y,
					*self.unknown_,
					)
			return b"NVMI" + packed

	class NVCI(List[bytes], RecordType):
		"""
		Unknown.
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
			length = size // 4
			assert not size % 4
			return cls(struct.unpack('<' + ("4s" * length), raw_bytes.read(size)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			body = b"".join(self)
			size = len(body)
			assert size == len(self) * 4
			size_field = struct.pack("<H", size)
			return b"NVCI" + size_field + body

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
					b"NVER",
					b"NVMI",
					b"NVCI",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
