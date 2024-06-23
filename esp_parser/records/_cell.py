#!/usr/bin/env python3
#
#  _cell.py
"""
CELL record type.
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
from typing import Iterator, List, Tuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID
from esp_parser.types import (
		CStringRecord,
		Float32Record,
		FormIDRecord,
		Int32Record,
		Record,
		RecordType,
		StructRecord,
		Uint8Record
		)

__all__ = ["CELL"]


class CELL(Record):
	"""
	Cell.
	"""

	class FULL(CStringRecord):
		"""
		The cell name.
		"""

	class DATA(Uint8Record):
		"""
		Flags.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/CELL.html
		"""

	@attrs.define
	class XCLC(StructRecord):
		"""
		Grid reference of the cell.
		"""

		x: int = 0
		y: int = 0
		force_hide_land: int = 0

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<iiI", 12

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return ('x', 'y', "force_hide_land")

	@attrs.define
	class XCLL(StructRecord):
		"""
		Lighting.
		"""

		# RGBA as 4 bytes
		ambient_color: bytes
		# RGBA as 4 bytes
		directional_color: bytes
		# RGBA as 4 bytes
		fog_color: bytes
		fog_near: float
		fog_far: float
		directional_rotation_xy: int
		directional_rotation_z: int
		directional_fade: float
		fog_clip_distance: float
		fog_power: float

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<4s4s4sffiifff", 40

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"ambient_color",
					"directional_color",
					"fog_color",
					"fog_near",
					"fog_far",
					"directional_rotation_xy",
					"directional_rotation_z",
					"directional_fade",
					"fog_clip_distance",
					"fog_power",
					)

	# class IMPF(RecordType):
	# 	"""
	# 	Footstep Material.
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/IMPF.html
	# 	"""

	class LTMP(FormIDRecord):
		"""
		Light template giving the Form ID of an :class:`~.LGTM` record. May be 0.
		"""

	class LNAM(RecordType, int):
		"""
		Lighting template flags.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/CELL.html
		"""

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x04\x00"  # size field
			return cls(*struct.unpack("<I", raw_bytes.read(4)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"LNAM\x04\x00" + struct.pack("<I", self)

	class XCLW(Float32Record):
		"""
		Water height.
		"""

	class XNAM(CStringRecord):
		"""
		Water noise texture name.
		"""

	class XCLR(List, RecordType):
		"""
		Regions.

		Sequence of form IDs (as bytes) for :class:`~.REGN` records.
		"""

		def __repr__(self) -> str:
			return f"{self.__class__.__qualname__}({super().__repr__()})"

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size = struct.unpack("<H", raw_bytes.read(2))[0]
			self = cls()
			num_form_ids: float = size / 4
			assert num_form_ids.is_integer()
			for _ in range(int(num_form_ids)):
				self.append(raw_bytes.read(4))
			return self

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			name = self.__class__.__name__.encode()
			size = len(self) * 4
			packed = struct.pack(f"<H", size)
			return name + packed + b''.join(self)

	class XCIM(FormIDRecord):
		"""
		Image Space.

		Form ID of an :class:`~.IMGS` record.
		"""

	# class XCET(RecordType):
	# 	"""
	# 	Unknown.
	# 	"""

	class XEZN(FormIDRecord):
		"""
		Encounter Zone.

		Form ID of an :class:`~.ECZN` record.
		"""

	class XCCM(FormIDRecord):
		"""
		Climate.

		Form ID of a :class:`~.CLMT` record.
		"""

	class XCWT(FormIDRecord):
		"""
		Water.

		Form ID of a :class:`~.WATR` record.
		"""

	class XOWN(FormIDRecord):
		"""
		Owner.

		Ownership data. Form ID of a :class:`~.FACT`, :class:`~.ACHR` or :class:`~.NPC_` record.
		"""

	class XRNK(Int32Record):
		"""
		Faction rank.

		Ownership data
		"""

	class XCAS(FormIDRecord):
		"""
		Acoustic space.

		Form ID of an :class:`~.ASPC` record.
		"""

	# class XCMT(RecordType):
	# 	"""
	# 	Unused.
	# 	"""

	class XCMO(FormIDRecord):
		"""
		Music type.

		Form ID of a :class:`~.MUSC` record.
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
					b"DATA",
					b"FULL",
					b"IMPF",
					b"LNAM",
					b"LTMP",
					b"XCAS",
					b"XCCM",
					b"XCET",
					b"XCIM",
					b"XCLC",
					b"XCLL",
					b"XCLR",
					b"XCLW",
					b"XCMO",
					b"XCMT",
					b"XCWT",
					b"XEZN",
					b"XNAM",
					b"XOWN",
					b"XRNK",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
