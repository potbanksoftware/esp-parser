#!/usr/bin/env python3
#
#  _pgre.py
"""
PGRE record type.
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
from esp_parser.types import (
		CStringRecord,
		Float32Record,
		FormIDRecord,
		Int32Record,
		Record,
		RecordType,
		Uint8Record
		)

__all__ = ["PGRE"]


class PGRE(Record):
	"""
	Placed Grenade.
	"""

	class NAME(FormIDRecord):
		"""
		Base.

		Form ID of a :class:`~.PROJ` record.
		"""

	class XEZN(FormIDRecord):
		"""
		Encounter Zone.

		Form ID of an :class:`~.ECZN` record.
		"""

	# class XRGD(RecordType):
	# 	"""
	# 	Ragdoll Data.
	# 	"""

	# class XRGB(RecordType):
	# 	"""
	# 	Ragdoll Biped Data.
	# 	"""

	class XPRD(Float32Record):
		"""
		Idle Time.

		Patrol data
		"""

	# class XPPA(RecordType):
	# 	"""
	# 	Patrol Script Marker.
	#
	# 	Patrol data
	# 	"""

	class INAM(FormIDRecord):
		"""
		Idle.

		Patrol data. Form ID of an :class:`~.IDLE` record, or null.
		"""

	# Embedded Script. collection
	#
	# Patrol data.
	#
	# https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/Script.html

	class TNAM(FormIDRecord):
		"""
		Topic.

		Patrol data. Form ID of a :class:`~.DIAL` record, or null.
		"""

	class XOWN(FormIDRecord):
		"""
		Owner.

		Ownership data. Form ID of a :class:`~.FACT`, :class:`~.ACHR`, :class:`~.CREA` or :class:`~.NPC_` record.
		"""

	class XRNK(Int32Record):
		"""
		Faction rank.

		Ownership data
		"""

	class XCNT(Int32Record):
		"""
		Count.
		"""

	class XRDS(Float32Record):
		"""
		Radius.
		"""

	class XHLP(Float32Record):
		"""
		Health.
		"""

	# class XPWR(RecordType):
	# 	"""
	# 	Water Reflection / Refraction.
	#
	# 	https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/XPWR.html
	# 	"""

	# class XDCR(RecordType):
	# 	"""
	# 	Decal.
	#
	# 	Linked decals
	#
	# 	https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/XDCR.html
	# 	"""

	class XLKR(FormIDRecord):
		"""
		Linked Reference.

		Form ID of a :class:`~.REFR`, :class:`~.ACRE`, :class:`~.ACHR`, :class:`~.PGRE` or :class:`~.PMIS` record.
		"""

	# class XCLP(RecordType):
	# 	"""
	# 	Linked Reference Color.
	#
	# 	https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/XCLP.html
	# 	"""

	class XAPD(Uint8Record):
		"""
		Flags.

		Activate parents.

		https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/XAPD.html
		"""

	# class XAPR(RecordType):
	# 	"""
	# 	Activate Parent Ref.
	#
	# 	Activate parents
	#
	# 	https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/XAPR.html
	# 	"""

	class XATO(CStringRecord):
		"""
		Activation Prompt.
		"""

	# class XESP(RecordType):
	# 	"""
	# 	Enable Parent.
	#
	# 	https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/XESP.html
	# 	"""

	class XEMI(FormIDRecord):
		"""
		Emittance.

		Form ID of a :class:`~.LIGH` or :class:`~.REGN` record.
		"""

	class XMBR(FormIDRecord):
		"""
		MultiBound Reference.

		Form ID of a :class:`~.REFR` record.
		"""

	# class XIBS(RecordType):
	# 	"""
	# 	Ignored By Sandbox.
	#
	# 	Flag
	# 	"""

	class XSCL(Float32Record):
		"""
		Scale.
		"""

	# class DATA(RecordType):
	# 	"""
	# 	Position / Rotation.
	#
	# 	https://tes5edit.github.ioSubrecords/DATA (ACHR, ACRE).md
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
					b"DATA",
					b"INAM",
					b"NAME",
					b"TNAM",
					b"XAPD",
					b"XAPR",
					b"XATO",
					b"XCLP",
					b"XCNT",
					b"XDCR",
					b"XEMI",
					b"XESP",
					b"XEZN",
					b"XHLP",
					b"XIBS",
					b"XLKR",
					b"XMBR",
					b"XOWN",
					b"XPPA",
					b"XPRD",
					b"XPWR",
					b"XRDS",
					b"XRGB",
					b"XRGD",
					b"XRNK",
					b"XSCL"
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
