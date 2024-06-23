#!/usr/bin/env python3
#
#  _navm.py
"""
NAVM record type.
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
from typing import Iterator, List, NamedTuple, Tuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID
from esp_parser.types import RawBytesRecord, Record, RecordType, StructRecord, Uint32Record
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["NAVM"]


class NAVM(Record):
	"""
	Navigation Mesh.
	"""

	class NVER(Uint32Record):
		"""
		Version.
		"""

	@attrs.define
	class DATA(StructRecord):
		"""
		Data.
		"""

		#: Form ID of a :class:`~.CELL`` record.
		cell: bytes
		vertex_count: int
		triangle_count: int
		external_connections_count: int
		nvca_count: int
		doors_count: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<4sIIIII", 24

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"cell",
					"vertex_count",
					"triangle_count",
					"external_connections_count",
					"nvca_count",
					"doors_count",
					)

	class NvvxVertex(NamedTuple):
		"""
		Individual element in :class:`~.NAVM.NVVX`.
		"""

		x: float
		y: float
		z: float

		@classmethod
		def unpack(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Unpack bytes for the :class:`~.NAVM.NvvxVertex`.
			"""

			return cls(*struct.unpack("<fff", raw_bytes.read(12)))

		def pack(self) -> bytes:
			"""
			Pack the :class:`~.NAVM.NvvxVertex` to bytes.
			"""

			return struct.pack("<fff", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class NVVX(List[NvvxVertex], RecordType):
		"""
		Vertices.
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
			count = size // 12
			assert not size % 12
			self = cls()
			for _ in range(count):
				buf = BytesIO(raw_bytes.read(12))
				self.append(NAVM.NvvxVertex.unpack(buf))

			return self

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			body = b"".join(di.pack() for di in self)
			size = struct.pack("<H", len(body))

			return b"NVVX" + size + body

	class NvtrTriangle(NamedTuple):
		"""
		Individual element in :class:`~.NAVM.NVTR`.
		"""

		vertex1: int
		vertex2: int
		vertex3: int
		edge_vertices_12: int
		edge_vertices_23: int
		edge_vertices_31: int
		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/NAVM.html

		@classmethod
		def unpack(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Unpack bytes for the :class:`~.NAVM.NvtrTriangle`.
			"""

			return cls(*struct.unpack("<hhhhhhI", raw_bytes.read(16)))

		def pack(self) -> bytes:
			"""
			Pack the :class:`~.NAVM.NvtrTriangle` to bytes.
			"""

			return struct.pack("<hhhhhhI", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class NVTR(List[NvtrTriangle], RecordType):
		"""
		Triangles.
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
			count = size // 16
			assert not size % 16
			self = cls()
			for _ in range(count):
				buf = BytesIO(raw_bytes.read(16))
				self.append(NAVM.NvtrTriangle.unpack(buf))

			return self

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			body = b"".join(di.pack() for di in self)
			size = struct.pack("<H", len(body))

			return b"NVTR" + size + body

	class NVCA(List[int], RecordType):
		"""
		Unknown.

		Unknown, may be triangle IDs.
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
			length = size // 2
			assert not size % 2
			return cls(struct.unpack(f"<{length}h", raw_bytes.read(size)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = len(self)
			size_field = struct.pack("<H", size * 2)
			body = struct.pack(f"<{size}h", *self)
			return b"NVCA" + size_field + body

	class NvdpDoor(NamedTuple):
		"""
		Individual element in :class:`~.NAVM.NVDP`.
		"""

		#: Form ID of a :class:`~.REFR`` record.
		reference: bytes
		unknown: int
		unused: bytes

		@classmethod
		def unpack(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Unpack bytes for the :class:`~.NAVM.NvtrTriangle`.
			"""

			return cls(*struct.unpack("<4sH2s", raw_bytes.read(8)))

		def pack(self) -> bytes:
			"""
			Pack the :class:`~.NAVM.NvdpDoor` to bytes.
			"""

			return struct.pack("<4sH2s", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class NVDP(List[NvdpDoor], RecordType):
		"""
		Doors.
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
			count = size // 8
			assert not size % 8
			self = cls()
			for _ in range(count):
				buf = BytesIO(raw_bytes.read(8))
				self.append(NAVM.NvdpDoor.unpack(buf))

			return self

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			body = b"".join(di.pack() for di in self)
			size = struct.pack("<H", len(body))

			return b"NVDP" + size + body

	class NVGD(RawBytesRecord):
		"""
		NavMesh Grid.
		"""

	# class NVEX(RecordType):
	# 	"""
	# 	External Connections.
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

			if record_type == b"EDID":
				yield EDID.parse(raw_bytes)
			elif record_type in {b"NVER", b"DATA", b"NVVX", b"NVTR", b"NVCA", b"NVDP", b"NVGD", b"NVEX"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
