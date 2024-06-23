#!/usr/bin/env python3
#
#  _mset.py
"""
MSET record type.
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
		RawBytesRecord,
		Record,
		RecordType,
		Uint8Record,
		Uint32Record
		)

__all__ = ["MSET"]


class MSET(Record):
	"""
	Media Set.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class NAM1(Uint32Record):
		"""
		Type.

		Enum - see values below.
		"""

	class NAM2(CStringRecord):
		"""
		Loop (Battle) / Battle (Dungeon) / Day Outer (Location).
		"""

	class NAM3(CStringRecord):
		"""
		Explore (Dungeon) / Day Middle (Location).
		"""

	class NAM4(CStringRecord):
		"""
		Suspense (Dungeon) / Day Inner (Location).
		"""

	class NAM5(CStringRecord):
		"""
		Night Outer (Location).
		"""

	class NAM6(CStringRecord):
		"""
		Night Middle (Location).
		"""

	class NAM7(CStringRecord):
		"""
		Night Inner (Location).
		"""

	class NAM8(Float32Record):
		"""
		Loop dB (Battle) / Battle dB (Dungeon) / Day Outer dB (Location).
		"""

	class NAM9(Float32Record):
		"""
		Explore dB (Dungeon) / Day Middle dB (Location).
		"""

	class NAM0(Float32Record):
		"""
		Suspense dB (Dungeon) / Day Inner dB (Location).
		"""

	class ANAM(Float32Record):
		"""
		Night Outer dB (Location).
		"""

	class BNAM(Float32Record):
		"""
		Night Middle dB (Location).
		"""

	class CNAM(Float32Record):
		"""
		Night Inner dB (Location).
		"""

	class JNAM(Float32Record):
		"""
		Day/Night Outer/Middle/Inner Boundary % (Location).
		"""

	class PNAM(Uint8Record):
		"""
		Enable Flags.

		See values below.
		"""

	class DNAM(Float32Record):
		"""
		Wait Time (Battle) / Min Time On (Dungeon, Location) / Daytime Min (Incidental).
		"""

	class ENAM(Float32Record):
		"""
		Loop Fade Out (Battle) / Looping/Random Crossfade Overlap (Dungeon, Location) / Nighttime Min (Incidental).
		"""

	class FNAM(Float32Record):
		"""
		Recovery Time (Battle) / Layer Crossfade Time (Dungeon, Location) / Daytime Max (Incidental).
		"""

	class GNAM(Float32Record):
		"""
		Nighttime Max (Incidental).
		"""

	class HNAM(FormIDRecord):
		"""
		Intro (Battle, Dungeon) / Daytime (Incidental).

		Form ID of a :class:`~.SOUN` record.
		"""

	class INAM(FormIDRecord):
		"""
		Outro (Battle, Dungeon) / Nighttime (Incidental).

		Form ID of a :class:`~.SOUN` record.
		"""

	class KNAM(Float32Record):
		"""
		Unknown.
		"""

	class LNAM(Float32Record):
		"""
		Unknown.
		"""

	class MNAM(Float32Record):
		"""
		Unknown.
		"""

	class NNAM(Float32Record):
		"""
		Unknown.
		"""

	class ONAM(Float32Record):
		"""
		Unknown.
		"""

	class DATA(RawBytesRecord):
		"""
		Unknown.
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
					b"ANAM",
					b"BNAM",
					b"CNAM",
					b"DATA",
					b"DNAM",
					b"ENAM",
					b"FNAM",
					b"FULL",
					b"GNAM",
					b"HNAM",
					b"INAM",
					b"JNAM",
					b"KNAM",
					b"LNAM",
					b"MNAM",
					b"NAM0",
					b"NAM1",
					b"NAM2",
					b"NAM3",
					b"NAM4",
					b"NAM5",
					b"NAM6",
					b"NAM7",
					b"NAM8",
					b"NAM9",
					b"NNAM",
					b"ONAM",
					b"PNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
