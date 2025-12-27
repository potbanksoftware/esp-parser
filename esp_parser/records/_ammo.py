#!/usr/bin/env python3
#
#  _ammo.py
"""
AMMO record type.
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
from esp_parser.subrecords import EDID, OBND, Model
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType, StructRecord

__all__ = ["AMMO"]


class AMMO(Record):
	"""
	Ammunition.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class ICON(CStringRecord):
		"""
		Large Icon Filename.
		"""

	class MICO(CStringRecord):
		"""
		Small Icon FIlename.
		"""

	class SCRI(FormIDRecord):
		"""
		Script.

		Form ID of a :class:`~.SCPT` record.
		"""

	# Destruction Data. collection
	#
	# https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/Destruction.html

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

	@attrs.define
	class DATA(StructRecord):
		"""
		Data.
		"""

		speed: float
		flags: int  # See https://tes5edit.github.io/fopdoc/FalloutNV/Records/AMMO.html
		unused: bytes
		value: int
		clip_rounds: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<fB3sIB", 13

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return (
					"speed",
					"flags",
					"unused",
					"value",
					"clip_rounds",
					)

	@attrs.define
	class DAT2(StructRecord):
		"""
		Data 2.
		"""

		projectiles_per_shot: int

		#: Form ID of a :class:`~.PROJ` record, or null.
		projectile: bytes

		weight: float

		#: Form ID of an :class:`~.AMMO` or :class:`~.MISC` record, or null.
		consumed_ammo: bytes
		consumed_percentage: float

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<I4sf4sf", 20

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return (
					"projectiles_per_shot",
					"projectile",
					"weight",
					"consumed_ammo",
					"consumed_percentage",
					)

	class ONAM(CStringRecord):
		"""
		Short Name.
		"""

	class QNAM(CStringRecord):
		"""
		Abbreviation.
		"""

	class RCIL(FormIDRecord):
		"""
		Ammo Effect.

		Form ID of an :class:`~.AMEF` record.
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
					b"DAT2",
					b"DATA",
					b"FULL",
					b"ICON",
					b"MICO",
					b"ONAM",
					b"QNAM",
					b"RCIL",
					b"SCRI",
					b"YNAM",
					b"ZNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
