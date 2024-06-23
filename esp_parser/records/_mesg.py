#!/usr/bin/env python3
#
#  _mesg.py
"""
MESG record type.
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
from io import BytesIO
from typing import Iterator

# this package
from esp_parser.subrecords import CTDA, EDID
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType, Uint32Record

__all__ = ["MESG"]


class MESG(Record):
	"""
	Message.
	"""

	class DESC(CStringRecord):
		"""
		Description.
		"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class INAM(FormIDRecord):
		"""
		Icon.

		Form ID of a :class:`~.MICN` record, or null.
		"""

	# class NAM1(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	# class NAM2(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	# class NAM3(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	# class NAM4(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	# class NAM5(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	# class NAM6(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	# class NAM7(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	# class NAM8(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	# class NAM9(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	class DNAM(Uint32Record):
		"""
		Flags.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/MESG.html
		"""

	class TNAM(Uint32Record):
		"""
		Display Time.
		"""

	class ITXT(CStringRecord):
		"""
		Button Text.
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
			elif record_type == b"CTDA":
				yield CTDA.parse(raw_bytes)
			elif record_type in {
					b"DESC",
					b"DNAM",
					b"FULL",
					b"INAM",
					b"ITXT",
					b"NAM1",
					b"NAM2",
					b"NAM3",
					b"NAM4",
					b"NAM5",
					b"NAM6",
					b"NAM7",
					b"NAM8",
					b"NAM9",
					b"TNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
