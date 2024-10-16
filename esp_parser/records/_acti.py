#!/usr/bin/env python3
#
#  _acti.py
"""
ACTI record type.
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
from esp_parser.subrecords import EDID, OBND, Destruction, Model
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType

__all__ = ["ACTI"]


class ACTI(Record):
	"""
	Activator.
	"""

	class FULL(CStringRecord):
		"""
		Activator name.
		"""

	class SCRI(FormIDRecord):
		"""
		Script.

		Form ID of a :class:`~.SCPT` record.
		"""

	class SNAM(FormIDRecord):
		"""
		Sound - Looping.

		Form ID of a :class:`~.SOUN` record.
		"""

	class VNAM(FormIDRecord):
		"""
		Sound - Activation.

		Form ID of a :class:`~.SOUN` record.
		"""

	class INAM(FormIDRecord):
		"""
		Radio Template.

		Form ID of a :class:`~.SOUN` record.
		"""

	class RNAM(FormIDRecord):
		"""
		Radio Station.

		Form ID of a :class:`~.TACT` record.
		"""

	class WNAM(FormIDRecord):
		"""
		Water Type.

		Form ID of a :class:`~.WATR` record.
		"""

	class XATO(CStringRecord):
		"""
		Activation Prompt.
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
			elif record_type in {b"FULL", b"INAM", b"RNAM", b"SCRI", b"SNAM", b"VNAM", b"WNAM", b"XATO"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			elif record_type in Destruction.members:
				yield Destruction.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
