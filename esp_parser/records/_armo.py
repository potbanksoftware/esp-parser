#!/usr/bin/env python3
#
#  _armo.py
"""
ARMO record type.
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
from esp_parser.subrecords import EDID, OBND
from esp_parser.types import CStringRecord, FormIDRecord, Int32Record, Record, RecordType, Uint32Record

__all__ = ["ARMO"]


class ARMO(Record):
	"""
	Armor.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class SCRI(FormIDRecord):
		"""
		Script.

		Form ID of a :class:`~.SCPT` record.
		"""

	class EITM(FormIDRecord):
		"""
		Object Effect.

		Form ID of an :class:`~.ENCH` or :class:`~.SPEL` record.
		"""

	# class BMDT(RecordType):
	# 	"""
	# 	Biped Data.
	#
	# 	https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/BMDT.html
	# 	"""

	# Male Biped Model Data. collection
	#
	# The MODB subrecord is not present in this instance.
	#
	# https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/Model.html

	# Male World Model Data. collection
	#
	# #2
	#
	# https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/Model.html

	class ICON(CStringRecord):
		"""
		Male inventory icon filename.
		"""

	class MICO(CStringRecord):
		"""
		Male message icon filename.
		"""

	# Female Biped Model Data. collection
	#
	# #3
	#
	# https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/Model.html

	# Female World Model Data. collection
	#
	# #4
	#
	# https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/Model.html

	class ICO2(CStringRecord):
		"""
		Female inventory icon filename.
		"""

	class MIC2(CStringRecord):
		"""
		Female message icon filename.
		"""

	class BMCT(CStringRecord):
		"""
		Ragdoll Constraint Template.
		"""

	class REPL(FormIDRecord):
		"""
		Repair List.

		Form ID of a :class:`~.FLST` record.
		"""

	class BIPL(FormIDRecord):
		"""
		Biped Model List.

		Form ID of a :class:`~.FLST` record.
		"""

	class ETYP(Int32Record):
		"""
		Equipment Type.

		https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/ETYP.html
		"""

	class YNAM(FormIDRecord):
		"""
		Sound - Pick Up.

		Form ID of a :class:`~.SOUN` record.
		"""

	class ZNAM(FormIDRecord):
		"""
		Sound - Drop.

		Form ID of a :class:`~.SOUN` record.
		"""

	# class DATA(RecordType):
	# 	"""
	# 	Data.
	#
	# 	https://tes5edit.github.ioSubrecords/DATA (ARMO, ARMA).md
	# 	"""

	# class DNAM(RecordType):
	# 	"""
	# 	.
	# 	"""

	class BNAM(Uint32Record):
		"""
		Overrides Animation Sounds.

		Enum - see values below.
		"""

	# class SNAM(RecordType):
	# 	"""
	# 	Animation Sound.
	# 	"""

	class TNAM(FormIDRecord):
		"""
		Animation Sounds Template.

		Form ID of an :class:`~.ARMO` record.
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
					b"BIPL",
					b"BMCT",
					b"BMDT",
					b"BNAM",
					b"DATA",
					b"DNAM",
					b"EITM",
					b"ETYP",
					b"FULL",
					b"ICO2",
					b"ICON",
					b"MIC2",
					b"MICO",
					b"REPL",
					b"SCRI",
					b"SNAM",
					b"TNAM",
					b"YNAM",
					b"ZNAM"
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
