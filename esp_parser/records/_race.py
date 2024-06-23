#!/usr/bin/env python3
#
#  _race.py
"""
RACE record type.
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
from esp_parser.subrecords import EDID
from esp_parser.types import CStringRecord, Float32Record, FormIDRecord, Record, RecordType

__all__ = ["RACE"]


class RACE(Record):
	"""
	Race.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class DESC(CStringRecord):
		"""
		Description.
		"""

	# class XNAM(RecordType):
	# 	"""
	# 	Relation.
	#
	# 	https://tes5edit.github.ioSubrecords/XNAM (FACT, RACE).md
	# 	"""

	# class DATA(RecordType):
	# 	"""
	# 	.
	# 	"""

	class ONAM(FormIDRecord):
		"""
		Older.

		Form ID of a :class:`~.RACE` record.
		"""

	class YNAM(FormIDRecord):
		"""
		Younger.

		Form ID of a :class:`~.RACE` record.
		"""

	# class NAM2(RecordType):
	# 	"""
	# 	Unkonwin Marker.
	# 	"""

	# class VTCK(RecordType):
	# 	"""
	# 	Voices.
	# 	"""

	# class DNAM(RecordType):
	# 	"""
	# 	Default Hair Styles.
	# 	"""

	# class CNAM(RecordType):
	# 	"""
	# 	Default Hair Colors.
	# 	"""

	class PNAM(Float32Record):
		"""
		FaceGen - Main Clamp.
		"""

	class UNAM(Float32Record):
		"""
		FaceGen - Face Clamp.
		"""

	# class ATTR(RecordType):
	# 	"""
	# 	Unknown.
	# 	"""

	# class NAM0(RecordType):
	# 	"""
	# 	Head Data Marker.
	# 	"""

	# class MNAM(RecordType):
	# 	"""
	# 	Male Head Data Marker.
	# 	"""

	# Male Head Part. collection
	#
	# See below for details.

	# class FNAM(RecordType):
	# 	"""
	# 	Female Head Data Marker.
	# 	"""

	# Female Head Part. collection
	#
	# See below for details.

	# class NAM1(RecordType):
	# 	"""
	# 	Body Data Marker.
	# 	"""

	# class MNAM(RecordType):
	# 	"""
	# 	Male Body Data Marker.
	# 	"""

	# Male Body Part. collection
	#
	# See below for details.

	# class FNAM(RecordType):
	# 	"""
	# 	Female Body Data Marker.
	# 	"""

	# Female Body Part. collection
	#
	# See below for details.

	# class HNAM(RecordType):
	# 	"""
	# 	Hairs.
	#
	# 	Array of HAIR record FormIDs.
	# 	"""

	# class ENAM(RecordType):
	# 	"""
	# 	Eyes.
	#
	# 	Array of EYES record FormIDs.
	# 	"""

	# class MNAM(RecordType):
	# 	"""
	# 	Male FaceGen Data Marker.
	# 	"""

	# class FGGS(RecordType):
	# 	"""
	# 	Male FaceGen Geometry-Symmetric.
	# 	"""

	# class FGGA(RecordType):
	# 	"""
	# 	Male FaceGen Geometry-Asymmetric.
	# 	"""

	# class FGTS(RecordType):
	# 	"""
	# 	Male FaceGen Texture-Symmetric.
	# 	"""

	# class SNAM(RecordType):
	# 	"""
	# 	??.
	# 	"""

	# class FNAM(RecordType):
	# 	"""
	# 	Female FaceGen Data Marker.
	# 	"""

	# class FGGS(RecordType):
	# 	"""
	# 	Female FaceGen Geometry-Symmetric.
	# 	"""

	# class FGGA(RecordType):
	# 	"""
	# 	Female FaceGen Geometry-Asymmetric.
	# 	"""

	# class FGTS(RecordType):
	# 	"""
	# 	Female FaceGen Texture-Symmetric.
	# 	"""

	# class SNAM(RecordType):
	# 	"""
	# 	??.
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
			elif record_type in {
					b"ATTR",
					b"CNAM",
					b"DATA",
					b"DESC",
					b"DNAM",
					b"ENAM",
					b"FGGA",
					b"FGGS",
					b"FGTS",
					b"FNAM",
					b"FULL",
					b"HNAM",
					b"MNAM",
					b"NAM0",
					b"NAM1",
					b"NAM2",
					b"ONAM",
					b"PNAM",
					b"SNAM",
					b"UNAM",
					b"VTCK",
					b"XNAM",
					b"YNAM"
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
