#!/usr/bin/env python3
#
#  _dial.py
"""
DIAL record type.
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
from esp_parser.subrecords import EDID, DialType
from esp_parser.types import CStringRecord, Float32Record, FormIDRecord, Int32Record, Record, RecordType
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["DIAL"]


class DIAL(Record):
	"""
	Dialog topic.
	"""

	class QSTI(FormIDRecord):
		"""
		Form ID of the associated quest (:class:`~.QUST`).
		"""

	# class QSTR(BytesRecordType):
	# 	"""
	# 	Form ID of the associated quest (:class:`~.QUST`).
	# 	"""

	# 	@classmethod
	# 	def parse(cls, raw_bytes: BytesIO):
	# 		raise NotImplementedError
	# 		return cls(raw_bytes.read(4))

	class FULL(CStringRecord):
		"""
		Name of the topic.
		"""

	class PNAM(Float32Record):
		"""
		Priority.
		"""

	class DATA(NamedTuple):  # noqa: D106  # TODO
		#: Dialog type
		type: DialType
		# see https://tes5edit.github.io/fopdoc/Fallout3/Records/DIAL.html
		flags: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size, type_, flags = struct.unpack("<HBB", raw_bytes.read(4))
			assert size == 2, size
			return cls(DialType(type_), flags)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA" + struct.pack("<HBB", 2, *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(DATA)

	class INFC(FormIDRecord):
		"""
		Info connection (New Vegas Only).

		Form ID of an :class:`~.INFO` record.
		"""

	class INFX(Int32Record):
		"""
		Info index.
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
					b"QSTI",
					b"FULL",
					b"PNAM",
					b"DATA",
					b"INFC",
					b"INFX",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
