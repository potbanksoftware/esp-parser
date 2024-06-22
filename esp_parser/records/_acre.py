#!/usr/bin/env python3
#
#  _acre.py
"""
ACRE record type.
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
from esp_parser.subrecords import EDID, PositionRotation
from esp_parser.types import (
		Float32Record,
		FormIDRecord,
		Int32Record,
		MarkerRecord,
		RawBytesRecord,
		Record,
		RecordType,
		Uint8Record
		)

__all__ = ["ACRE"]


class ACRE(Record):
	"""
	Placed Creature.
	"""

	class NAME(FormIDRecord):
		"""
		Base.

		FormID of a CREA record.
		"""

	class XEZN(FormIDRecord):
		"""
		Encounter Zone.

		FormID of a ECZN record.
		"""

	class XRGD(RawBytesRecord):
		"""
		Ragdoll Data.
		"""

	class XRGB(RawBytesRecord):
		"""
		Ragdoll Biped Data.
		"""

	class XPRD(Float32Record):
		"""
		Idle Time.

		Patrol data
		"""

	class XPPA(MarkerRecord):
		"""
		Patrol Script Marker.

		Patrol data
		"""

		# def __repr__(self) -> str:
		# 	return "ACRE.XPPA()"

		# @classmethod
		# def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		# 	"""
		# 	Parse this subrecord.

		# 	:param raw_bytes: Raw bytes for this record
		# 	"""

		# 	assert raw_bytes.read(2) == b"\x00\x00"  # size field
		# 	return cls()

		# def unparse(self) -> bytes:
		# 	"""
		# 	Turn this subrecord back into raw bytes for an ESP file.
		# 	"""

		# 	return b"XPPA\x00\x00"

	class INAM(FormIDRecord):
		"""
		Idle.

		Patrol data. FormID of an IDLE record, or null.
		"""

	# Embedded Script. collection
	#
	# Patrol data.
	#
	# https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Script.html

	class TNAM(FormIDRecord):
		"""
		Topic.

		Patrol data. FormID of a DIAL record, or null.
		"""

	class XLCM(Int32Record):
		"""
		Level Modifier.
		"""

	class XOWN(FormIDRecord):
		"""
		Owner.

		Ownership data. FormID of a :class:`~.FACT`, :class:`~.ACHR` or :class:`~.NPC_` record.
		"""

	class XRNK(Int32Record):
		"""
		Faction rank.

		Ownership data.
		"""

	class XMRC(FormIDRecord):
		"""
		Merchant Container.

		FormID of a REFR record.
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

	# class XDCR(RecordType):
	# 	"""
	# 	Decal.
	#
	# 	Linked decals
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XDCR.html
	# 	"""

	class XLKR(FormIDRecord):
		"""
		Linked Reference.
		"""

	# class XCLP(RecordType):
	# 	"""
	# 	Linked Reference Color.
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XCLP.html
	# 	"""

	class XAPD(Uint8Record):
		"""
		Flags.

		Activate parents

		https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XAPD.html
		"""

	# class XAPR(RecordType):
	# 	"""
	# 	Activate Parent Ref.
	#
	# 	Activate parents
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XAPR.html
	# 	"""

	# class XESP(RecordType):
	# 	"""
	# 	Enable Parent.
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XESP.html
	# 	"""

	class XEMI(FormIDRecord):
		"""
		Emittance.

		FormID of a LIGH or REGN record.
		"""

	class XMBR(FormIDRecord):
		"""
		MultiBound Reference.

		FormID of a REFR record.
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
					b"NAME",
					b"XEZN",
					b"XRGD",
					b"XRGB",
					b"XPRD",
					b"XPPA",
					b"INAM",
					b"TNAM",
					b"XLCM",
					b"XOWN",
					b"XRNK",
					b"XMRC",
					b"XCNT",
					b"XRDS",
					b"XHLP",
					b"XDCR",
					b"XLKR",
					b"XCLP",
					b"XAPD",
					b"XAPR",
					b"XESP",
					b"XEMI",
					b"XMBR",
					b"XIBS",
					b"XSCL",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type == b"DATA":
				yield PositionRotation.DATA.parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
