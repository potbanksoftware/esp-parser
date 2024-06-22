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
import struct
from io import BytesIO
from typing import Iterator, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID, Model
from esp_parser.types import CStringRecord, Record, RecordType

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
	class DATA(RecordType):
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

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x48\x00"
			return cls(*struct.unpack("<If4siiH2s4sf4s4s4s4s4s4sffIi", raw_bytes.read(72)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			packed = struct.pack(
					"<If4siiH2s4sf4s4s4s4s4s4sffIi",
					self.flags,
					self.base_cost,
					self.associated_item,
					self.magic_school,
					self.resistance_type,
					self.unknown,
					self.unused,
					self.light,
					self.projectile_speed,
					self.effect_shader,
					self.object_display_shader,
					self.effect_sound,
					self.bold_sound,
					self.hit_sound,
					self.area_sound,
					self.constant_effect_enchantment_factor,
					self.constant_effect_barter_factor,
					self.archtype,
					self.actor_value,
					)
			return b"DATA" + b"\x48\x00" + packed

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

			if record_type in {
					b"FULL",
					b"DESC",
					b"ICON",
					b"MICO",
					b"DATA",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)

			elif record_type == b"EDID":
				yield EDID.parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
