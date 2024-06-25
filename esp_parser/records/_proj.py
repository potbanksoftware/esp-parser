#!/usr/bin/env python3
#
#  _proj.py
"""
PROJ record type.
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
from esp_parser.subrecords import EDID, OBND, Destruction, Model
from esp_parser.types import CStringRecord, Record, RecordType, StructRecord, Uint32Record

__all__ = ["PROJ"]


class PROJ(Record):
	"""
	Projectile.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	@attrs.define
	class DATA(StructRecord):
		"""
		Data.
		"""

		flags: int  # See https://tes5edit.github.io/fopdoc/FalloutNV/Records/PROJ.html
		type: int  # Enum - see https://tes5edit.github.io/fopdoc/FalloutNV/Records/PROJ.html
		gravity: float
		speed: float
		range: float

		#: Form ID of a :class:`~.LIGH` record, or null.
		light: bytes

		#: Form ID of a :class:`~.LIGH` record, or null.
		muzzle_flash_light: bytes

		tracer_chance: float
		explosion_alt_trigger_proximity: float
		explosion_alt_trigger_timer: float

		#: Form ID of an :class:`~.EXPL` record, or null.
		explosion: bytes

		#: Form ID of a :class:`~.SOUN` record, or null.
		sound: bytes
		muzzle_flash_duration: float
		fade_duration: float
		impact_force: float

		#: Form ID of a :class:`~.SOUN` record, or null.
		sound_countdown: bytes

		#: Form ID of a :class:`~.SOUN` record, or null.
		sound_disable: bytes

		#: Form ID of a :class:`~.WEAP` record, or null.
		default_weapon_source: bytes

		x_rotation: float
		y_rotation: float
		z_rotation: float
		bouncy_multiplier: float

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<HHfff4s4sfff4s4sfff4s4s4sffff", 84

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return (
					"flags",
					"type",
					"gravity",
					"speed",
					"range",
					"light",
					"muzzle_flash_light",
					"tracer_chance",
					"explosion_alt_trigger_proximity",
					"explosion_alt_trigger_timer",
					"explosion",
					"sound",
					"muzzle_flash_duration",
					"fade_duration",
					"impact_force",
					"sound_countdown",
					"sound_disable",
					"default_weapon_source",
					"x_rotation",
					"y_rotation",
					"z_rotation",
					"bouncy_multiplier",
					)

	class NAM1(CStringRecord):
		"""
		Muzzle Flash Model Filename.
		"""

	# class NAM2(RecordType):
	# 	"""
	# 	Muzzle Flash Model Texture File Hashes.
	# 	"""

	class VNAM(Uint32Record):
		"""
		Sound Level.

		Enum - see link for values.

		https://tes5edit.github.io/fopdoc/FalloutNV/Records/Values/Sound%20Levels.html
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
			elif record_type in {b"DATA", b"FULL", b"NAM1", b"NAM2", b"VNAM"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			elif record_type in Destruction.members:
				yield Destruction.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
