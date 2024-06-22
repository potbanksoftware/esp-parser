#!/usr/bin/env python3
#
#  _pack.py
"""
PACK record type.
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
from typing import Iterator, Tuple

# 3rd party
import attrs

# this package
from esp_parser.subrecords import CTDA, EDID, Script
from esp_parser.types import (
		Float32Record,
		FormIDRecord,
		MarkerRecord,
		RawBytesRecord,
		Record,
		RecordType,
		StructRecord,
		Uint8Record,
		Uint16Record,
		Uint32Record
		)

__all__ = ["PACK"]


class PACK(Record):
	"""
	Package.
	"""

	@attrs.define
	class PKDT(StructRecord):
		"""
		General.
		"""

		general_flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html 	uint32 	See below for values.
		type: int  # Enum - See https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html 	uint32 	See below for values.
		unused: bytes
		fallout_behaviour_flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html 	uint32 	See below for values.

		type_specific_flags: int

		unused_: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<IBsHH2s", 12

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"general_flags",
					"type",
					"unused",
					"fallout_behaviour_flags",
					"type_specific_flags",
					"unused_",
					)

	# Location. collection
	#
	# See below for details.

	@attrs.define
	class PLDT(StructRecord):
		"""
		Location Subrecord - Location 1
		"""

		type: int  # Enum - see https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html

		location: bytes
		"""
		Form ID or uint32 (as bytes) or uint8[] (as bytes)

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html
		"""

		radius: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<I4si", 12

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"type",
					"location",
					"radius",
					)

	class PLD2(PLDT):
		"""
		Location Subrecord - Location 2.
		"""

	@attrs.define
	class PSDT(StructRecord):
		"""
		Schedule.
		"""

		month: int
		day_of_week: int  # Enum - see https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html
		date: int
		time: int
		duration: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<bbBbi", 8

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"month",
					"day_of_week",
					"date",
					"time",
					"duration",
					)

	@attrs.define
	class PTDT(StructRecord):
		"""
		Target 1.
		"""

		type: int  # Enum - see https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html
		#: Form ID or uint32 (as bytes) or uint8[] (as bytes)
		target: bytes
		count_or_distance: int
		unknown: float

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<i4sif", 16

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"type",
					"target",
					"count_or_distance",
					"unknown",
					)

	class IDLF(Uint8Record):
		"""
		Idle Animation Flags.

		See below for values.
		"""

	# class IDLC(RecordType):
	# 	"""
	# 	Idle Animation Count.
	# 	"""

	class IDLT(Float32Record):
		"""
		Idle Timer Setting.
		"""

	# class IDLA(RecordType):
	# 	"""
	# 	Animations.
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/IDLA.html
	# 	"""

	# class IDLB(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	class CNAM(FormIDRecord):
		"""
		Combat Style.

		FormID of a CSTY record.
		"""

	# class PKED(RecordType):
	# 	"""
	# 	Eat Marker.
	# 	"""

	class PKE2(Uint32Record):
		"""
		Escort Distance.
		"""

	class PKFD(Float32Record):
		"""
		Follow - Start Location - Trigger Radius.
		"""

	class PKPT(Uint16Record):
		"""
		Patrol Flags.
		"""

	# class PKW3(RecordType):
	# 	"""
	# 	Use Weapon Data.
	# 	"""

	# class PTD2(RecordType):
	# 	"""
	# 	Target 2.
	# 	"""

	# class PUID(RecordType):
	# 	"""
	# 	Use Item Marker.
	# 	"""

	# class PKAM(RecordType):
	# 	"""
	# 	Ambush Marker.
	# 	"""

	@attrs.define
	class PKDD(StructRecord):
		"""
		Dialog Data.
		"""

		fov: float

		#: Form ID of a :class:`~.DIAL` record, or null.
		topic: bytes

		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html
		unused: bytes
		dialog_type: int  # Enum - see https://tes5edit.github.io/fopdoc/Fallout3/Records/PACK.html
		#: Four extra bytes at end not shown in fopdoc
		unknown: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<f4sI4sI4s", 24

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"fov",
					"topic",
					"flags",
					"unused",
					"dialog_type",
					"unknown",
					)

	class POBA(MarkerRecord):
		"""
		OnBegin Marker / OnEnd Marker / OnChange Marker.
		"""

	class INAM(FormIDRecord):
		"""
		OnBegin Idle / OnEnd Idle / OnChange Idle.

		FormID of an IDLE record, or null.
		"""

	# OnBegin Embedded Script. collection
	#
	# https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Script.html

	class TNAM(FormIDRecord):
		"""
		OnBegin Topic / OnEnd Topic / OnChange Topic.

		FormID of a DIAL record, or null.
		"""

	# OnEnd Embedded Script. collection
	#
	# https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Script.html

	# OnChange Embedded Script. collection
	#
	# https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Script.html

	class POEA(RawBytesRecord):
		"""
		Unknown.

		Not shown in fopdoc.
		"""

	class POCA(RawBytesRecord):
		"""
		Unknown.

		Not shown in fopdoc.
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
					b"PKDT",
					b"PSDT",
					b"PTDT",
					b"CTDA",
					b"IDLF",
					b"IDLC",
					b"IDLT",
					b"IDLA",
					b"IDLB",
					b"CNAM",
					b"PKED",
					b"PKE2",
					b"PKFD",
					b"PKPT",
					b"PKW3",
					b"PTD2",
					b"PUID",
					b"PKAM",
					b"PKDD",
					b"PLD2",
					b"POBA",
					b"INAM",
					b"TNAM",
					b"POBA",
					b"POBA",
					b"PLDT",
					b"POEA",
					b"POCA",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in {b"SCHR", b"SCDA", b"SCTX", b"SCRO", b"SLSD", b"SCVR", b"SCRV"}:
				yield getattr(Script, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
