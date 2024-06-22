#!/usr/bin/env python3
#
#  _soun.py
"""
SOUN record type.
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
from typing import Iterator, Tuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID, OBND
from esp_parser.types import CStringRecord, Record, RecordType, Uint8Record

__all__ = ["SOUN"]


class SOUN(Record):
	"""
	Sound.
	"""

	class FNAM(CStringRecord):
		"""
		Sound Filename.
		"""

	class RNAM(Uint8Record):
		"""
		Random Chance % (New Vegas only).
		"""

	@attrs.define
	class SNDD(RecordType):
		"""
		Sound Data.
		"""

		#: Minimum Attenuation Distance. Multiplied by 5.
		min_attenuation_distance: int = 0
		#: Maximum Attenuation Distance. Multiplied by 100.
		max_attenuation_distance: int = 0
		frequency_adjustment_percentage: int = 0
		unused: bytes = b"\x00"
		flags: int = 256
		#: Static Attenuation cdB
		static_attenuation: int = 0
		stop_time: int = 0
		start_time: int = 0
		#: Points on the attenuation curve.
		attenuation_points: Tuple[int, int, int, int, int] = (0, 0, 0, 0, 0)
		reverb_attenuation_control: int = 0
		priority: int = 0
		#: New Vegas only (bytes representation of int32). Unused on Fallout 3
		x: bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00'
		#: New Vegas only (bytes representation of int32). Not present on Fallout 3 (so should be empty)
		y: bytes = b''

		# TODO: helpers for X and Y on new vegas (allow setting and getting as ints)

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size = struct.unpack("<H", raw_bytes.read(2))[0]
			if size == 36:
				# Fallout 3
				unpacked = (*struct.unpack("<BBbcIhBBhhhhhhi8s", raw_bytes.read(size)), b'')
			elif size == 44:
				# Fallout New Vegas
				unpacked = struct.unpack("<BBbcIhBBhhhhhhi8s8s", raw_bytes.read(size))

			return cls(
					min_attenuation_distance=unpacked[0],
					max_attenuation_distance=unpacked[1],
					frequency_adjustment_percentage=unpacked[2],
					unused=unpacked[3],
					flags=unpacked[4],
					static_attenuation=unpacked[5],
					stop_time=unpacked[6],
					start_time=unpacked[7],
					attenuation_points=unpacked[8:13],
					reverb_attenuation_control=unpacked[13],
					priority=unpacked[14],
					x=unpacked[15],
					y=unpacked[16],
					)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			pack_values = [
					self.min_attenuation_distance,
					self.max_attenuation_distance,
					self.frequency_adjustment_percentage,
					self.unused,
					self.flags,
					self.static_attenuation,
					self.stop_time,
					self.start_time,
					*self.attenuation_points,
					self.reverb_attenuation_control,
					self.priority,
					self.x,
					]

			if self.y == b'':
				# Fallout 3
				pack_string = "<BBbcIhBBhhhhhhi8s"
				size = 36
			else:
				# Fallout New Vegas
				pack_values.append(self.y)
				pack_string = "<BBbcIhBBhhhhhhi8s8s"
				size = 44

			packed_body = struct.pack(pack_string, *pack_values)

			assert len(packed_body) == size
			return b"SNDD" + struct.pack("<H", size) + packed_body

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
			elif record_type == b"FNAM":
				yield cls.FNAM.parse(raw_bytes)
			elif record_type == b"SNDD":
				yield cls.SNDD.parse(raw_bytes)
			elif record_type == b"RNAM":
				yield cls.RNAM.parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
