#!/usr/bin/env python3
#
#  _mgef.py
"""
MGEF record type.
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
from esp_parser.subrecords import EDID, Model
from esp_parser.types import CStringRecord, Record, RecordType, StructRecord

__all__ = ["MGEF"]


class MGEF(Record):
	"""
	Magic Effect.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class DESC(CStringRecord):
		"""
		Description.
		"""

	class ICON(CStringRecord):
		"""
		Large icon filename.
		"""

	class MICO(CStringRecord):
		"""
		Small icon filename.
		"""

	@attrs.define
	class DATA(StructRecord):
		"""
		Data.
		"""

		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/MGEF.html
		base_cost: float  # Unused

		#: A form ID
		associated_item: bytes

		#: Unused. A value of ``-1`` means ``none``.
		magic_school: int
		resistance_type: int
		unknown: int
		unused: bytes

		#: Form ID of a :class:`~.LIGH` record, or null.
		light: bytes
		projectile_speed: float  #

		#: Form ID of an :class:`~.EFSH` record, or null.
		effect_shader: bytes

		#: Form ID of an :class:`~.EFSH` record, or null.
		object_display_shader: bytes

		#: Form ID of an :class:`~.SOUN` record, or null.
		effect_sound: bytes

		#: Form ID of an :class:`~.SOUN` record, or null.
		bold_sound: bytes

		#: Form ID of an :class:`~.SOUN` record, or null.
		hit_sound: bytes

		#: Form ID of an :class:`~.SOUN` record, or null.
		area_sound: bytes

		#: Unused.
		constant_effect_enchantment_factor: float

		#: Unused.
		constant_effect_barter_factor: float
		archtype: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/MGEF.html
		actor_value: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<If4siiH2s4sf4s4s4s4s4s4sffIi", 72

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return (
					"flags",
					"base_cost",
					"associated_item",
					"magic_school",
					"resistance_type",
					"unknown",
					"unused",
					"light",
					"projectile_speed",
					"effect_shader",
					"object_display_shader",
					"effect_sound",
					"bold_sound",
					"hit_sound",
					"area_sound",
					"constant_effect_enchantment_factor",
					"constant_effect_barter_factor",
					"archtype",
					"actor_value",
					)

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

			if record_type in {b"FULL", b"DESC", b"ICON", b"MICO", b"DATA"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type == b"EDID":
				yield EDID.parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
