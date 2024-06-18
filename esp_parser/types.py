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
import struct
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Iterator, List, Protocol, Type, Union

# 3rd party
import attrs
from typing_extensions import Self

__all__ = [
		"BytesRecordType", "CStringRecord", "Float32Record", "FormIDRecord", "Record", "RecordType", "Uint8Record"
		]


class RecordType(Protocol):
	"""
	Base class for records in ESP files.
	"""

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({super().__repr__()})"

	@abstractmethod
	def unparse(self) -> bytes:
		"""
		Turn this record back into raw bytes for an ESP file.
		"""

		raise NotImplementedError


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

		unpacked = struct.unpack("<II4sIH2s", raw_bytes.read(20))
		data_size, flags, form_id, revision, version, unknown = unpacked
		data = list(cls.parse_subrecords(BytesIO(raw_bytes.read(data_size))))

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
		return cls(*struct.unpack(">B", raw_bytes.read(1)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		name = self.__class__.__name__.encode()
		body = struct.pack(">B", self)
		size = struct.pack("<H", len(body))
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
