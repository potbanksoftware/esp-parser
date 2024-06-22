#!/usr/bin/env python3
#
#  types.py
"""
Shared base types.
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
import enum
import struct
import zlib
from abc import abstractmethod
from io import BytesIO
from typing import Iterator, List, Protocol, Set, Tuple, Type, Union

# 3rd party
import attrs
from typing_extensions import Self

__all__ = [
		"AttrsStructRecord",
		"BytesRecordType",
		"CStringRecord",
		"Collection",
		"FaceGenRecord",
		"Float32Record",
		"FormIDRecord",
		"Int16Record",
		"Int32Record",
		"Int8Record",
		"IntEnum",
		"IntEnumField",
		"MarkerRecord",
		"RawBytesRecord",
		"Record",
		"RecordType",
		"StructRecord",
		"Uint16Record",
		"Uint32Record",
		"Uint8Record"
		]


class RecordType(Protocol):
	"""
	Base class for records in ESP files.
	"""

	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__}({super().__repr__()})"

	@abstractmethod
	def unparse(self) -> bytes:
		"""
		Turn this record back into raw bytes for an ESP file.
		"""

		raise NotImplementedError


class StructRecord(RecordType):
	"""
	Base class for records in ESP files.
	"""

	@staticmethod
	@abstractmethod
	def get_struct_and_size() -> Tuple[str, int]:
		"""
		Returns the pack/unpack struct string and the corresponding size.
		"""

		raise NotImplementedError

	@staticmethod
	@abstractmethod
	def get_field_names() -> Tuple[str, ...]:
		"""
		Returns a list of attributes on this class in the order they should be packed.
		"""

		raise NotImplementedError

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		unpack_struct, expected_size = cls.get_struct_and_size()
		size = struct.unpack("<H", raw_bytes.read(2))[0]
		if size != expected_size:
			raise ValueError(f"Size mismatch for {cls}: Expected {expected_size}, got {size}")
		return cls(*struct.unpack(unpack_struct, raw_bytes.read(size)))

	def unparse(self) -> bytes:
		"""
		Turn this record back into raw bytes for an ESP file.
		"""

		pack_struct, size = self.get_struct_and_size()
		size_field = struct.pack("<H", size)
		pack_items = [getattr(self, field_name) for field_name in self.get_field_names()]
		body = struct.pack(pack_struct, *pack_items)
		return self.__class__.__name__.encode() + size_field + body


@attrs.define
class AttrsStructRecord(StructRecord):
	"""
	Intermediate type for attrs-decorated record types, to give a better repr.
	"""

	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__}({super().__repr__()})"


@attrs.define
class Record(RecordType):
	"""
	Represents a record in an ESP file.
	"""

	#: Record type (4 bytes long)
	type: bytes

	# data_size: int

	#: Record flags
	flags: int
	# See https://tes5edit.github.io/fopdoc/Fallout3/Records.html

	#: 4-byte form ID
	id: bytes

	#: Used for revision control by the Creation Kit, if enabled.
	revision: int = 0

	#: Form version
	version: int = 15

	unknown: bytes = b"\x00\x00"

	#: Subrecords of this record.
	data: List[RecordType] = attrs.field(factory=list)

	@staticmethod
	def parse_subrecords(raw_bytes: BytesIO) -> Iterator[RecordType]:
		"""
		Parse this record's subrecords.

		Must be implemented in subclasses.

		:param raw_bytes: Raw bytes for this record's subrecords
		"""

		yield from ()

	@classmethod
	def parse(cls: Type[Self], record_type: bytes, raw_bytes: BytesIO) -> Self:
		"""
		Parse this record.

		:param record_type: 4-byte identifier for this record, e.g. ``b"INFO"``
		:param raw_bytes: Raw bytes for this record
		"""

		buf = raw_bytes.read(20)
		unpacked = struct.unpack("<II4sIH2s", buf)
		data_size, flags, form_id, revision, version, unknown = unpacked

		raw_data = BytesIO(raw_bytes.read(data_size))
		if flags & 0x00040000:
			# Compressed data
			decompressed_size = struct.unpack("<I", raw_data.read(4))[0]
			compressed_data = raw_data.read(data_size - 4)
			decompressed_data = zlib.decompress(compressed_data)
			assert len(decompressed_data) == decompressed_size
			raw_data = BytesIO(decompressed_data)

		data = list(cls.parse_subrecords(raw_data))

		return cls(
				type=record_type,
				flags=flags,
				id=form_id,
				revision=revision,
				version=version,
				unknown=unknown,
				data=data,
				)

	def unparse(self) -> bytes:
		"""
		Turn this record back into raw bytes for an ESP file.
		"""

		body = b"".join(subrecord.unparse() for subrecord in self.data)
		data_size = len(body)

		if self.flags & 0x00040000:
			# Compressed data
			compressed_data = zlib.compress(body)
			body = struct.pack("<I", data_size) + compressed_data
			data_size = len(body)

		packed = struct.pack(
				"<II4sIH2s",
				data_size,
				self.flags,
				self.id,
				self.revision,
				self.version,
				self.unknown,
				)
		return self.type + packed + body


class BytesRecordType(RecordType, bytes):
	"""
	Base class for bytes subrecord types.

	Subclasses are responsible for parsing and unparsing.
	"""

	def __new__(cls, cstring: Union[str, bytes] = b''):  # noqa: D102
		if isinstance(cstring, str):
			return super().__new__(cls, cstring, encoding="UTF-8")
		else:
			return super().__new__(cls, cstring)


class FormIDRecord(BytesRecordType):
	"""
	Base class for 4-byte long form ID subrecord types.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x04\x00"  # size field
		return cls(raw_bytes.read(4))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.split('.')[-1].encode()
		return name + b"\x04\x00" + self


class CStringRecord(BytesRecordType):
	"""
	Base class for cstring subrecord types - sequences of bytes prefixed with the size.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		buf = []
		raw_bytes.read(2)
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

		return self.__class__.__name__.encode() + struct.pack("<H", len(self) + 1) + self + b"\x00"

	# @classmethod
	# def new(cls, value: Union[str, bytes]):
	# 	if isinstance(value, str):
	# 		value = value.encode()
	# 	size = struct.encode(">H", len(value))
	# 	return cls(size + value)


class Uint8Record(RecordType, int):
	"""
	Base class for uint8 subrecords.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x01\x00"  # size field
		return cls(*struct.unpack("<B", raw_bytes.read(1)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		body = struct.pack("<B", self)
		size = struct.pack("<H", len(body))
		return name + size + body


class Int8Record(RecordType, int):
	"""
	Base class for int8 subrecords.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x01\x00"  # size field
		return cls(*struct.unpack("<b", raw_bytes.read(1)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		body = struct.pack("<b", self)
		size = struct.pack("<H", len(body))
		return name + size + body


class Uint16Record(RecordType, int):
	"""
	Base class for uint16 subrecords.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x02\x00"  # size field
		return cls(*struct.unpack("<H", raw_bytes.read(2)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		body = struct.pack("<H", self)
		size = struct.pack("<H", len(body))
		return name + size + body


class Int16Record(RecordType, int):
	"""
	Base class for int16 subrecords.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x02\x00"  # size field
		return cls(*struct.unpack("<h", raw_bytes.read(2)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		body = struct.pack("<H", self)
		size = struct.pack("<h", len(body))
		return name + size + body


class Float32Record(RecordType, float):
	"""
	Base class for float32 subrecords.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x04\x00"  # size field
		return cls(*struct.unpack("<f", raw_bytes.read(4)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		body = struct.pack("<f", self)
		size = struct.pack("<H", len(body))
		return name + size + body


class Int32Record(RecordType, int):
	"""
	Base class for int32 subrecords.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x04\x00"  # size field
		return cls(*struct.unpack("<i", raw_bytes.read(4)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		body = struct.pack("<i", self)
		size = struct.pack("<H", len(body))
		return name + size + body


class Uint32Record(RecordType, int):
	"""
	Base class for uint32 subrecords.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x04\x00"  # size field
		return cls(*struct.unpack("<I", raw_bytes.read(4)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		body = struct.pack("<I", self)
		size = struct.pack("<H", len(body))
		return name + size + body


class FaceGenRecord(List):
	"""
	Sequence of uint8 for FaceGen.
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
		return cls(struct.unpack(f"<{size}B", raw_bytes.read(size)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		size = len(self)
		packed = struct.pack(f"<H{size}B", size, *self)
		return name + packed


RecordType.register(FaceGenRecord)


class RawBytesRecord(BytesRecordType):
	"""
	Used for unknown structures.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		size = struct.unpack("<H", raw_bytes.read(2))[0]
		return cls(raw_bytes.read(size))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		size = struct.pack("<H", len(self))
		return name + size + self


class IntEnumField(enum.IntEnum):
	"""
	Base class for int enum fields.
	"""

	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__}({int(self)})"


class IntEnum(enum.IntEnum):
	"""
	Base class for integer enums.
	"""

	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__}.{self._name_}"


RecordType.register(IntEnumField)


class Collection:
	"""
	Base class for collections of subrecords.
	"""

	#: Names of subrecords in this collection.
	members: Set[bytes]

	@classmethod
	def parse_member(cls, record_type: bytes, raw_bytes: BytesIO) -> RecordType:
		"""
		Parse subrecords in this collection.

		:param raw_bytes: Raw bytes for this record's subrecords
		"""

		assert record_type in cls.members
		return getattr(cls, record_type.decode()).parse(raw_bytes)


class MarkerRecord(RecordType):
	"""
	Zero byte long marker.
	"""

	def __repr__(self) -> str:
		return self.__class__.__qualname__ + "()"

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x00\x00"  # size field
		return cls()

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		return name + b"\x00\x00"
