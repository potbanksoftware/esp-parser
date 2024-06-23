#!/usr/bin/env python3
#
#  _perk.py
"""
PERK record type.
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
from esp_parser.subrecords import CTDA, EDID
from esp_parser.types import (
		Collection,
		CStringRecord,
		FormIDRecord,
		Int8Record,
		MarkerRecord,
		Record,
		RecordType,
		StructRecord,
		Uint8Record,
		Uint16Record
		)

__all__ = ["PERK", "PerkEffect"]


class PerkEffect(Collection):
	"""
	Effect subrecord collection for :class:`~.PERK`.
	"""

	members = {
			b"PRKE",
			b"DATA",  # Unreachable directly
			b"PRKC",
			b"EPFT",
			b"EPFD",
			b"EPF2",
			b"EPF3",
			b"PRKF",
			}

	@attrs.define
	class PRKE(StructRecord):
		"""
		Effect subrecord header.
		"""

		type: int  # Enum - see https://tes5edit.github.io/fopdoc/Fallout3/Records/PERK.html
		rank: int
		priority: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<BBB", 3

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return ("type", "rank", "priority")

	@attrs.define
	class DATAQuestStage(StructRecord):
		"""
		Data (Quest + Stage).
		"""

		#: Form ID of a :class:`~.QUST` record.
		quest: bytes
		quest_stage: int
		unused: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<4sb3s", 8

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return ("quest", "quest_stage", "unused")

		def unparse(self) -> bytes:
			"""
			Turn this record back into raw bytes for an ESP file.
			"""

			pack_struct, size = self.get_struct_and_size()
			size_field = struct.pack("<H", size)
			pack_items = [getattr(self, field_name) for field_name in self.get_field_names()]
			body = struct.pack(pack_struct, *pack_items)
			return b"DATA" + size_field + body

	class DATAAbility(FormIDRecord):
		"""
		Data (Ability).
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA" + b"\x04\x00" + self

	@attrs.define
	class DATAEntryPoint(StructRecord):
		"""
		Data (Quest + Stage).
		"""

		entry_point: int  # Enum - see https://tes5edit.github.io/fopdoc/Fallout3/Records/PERK.html
		function: int
		perk_condition_tab_count: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<BBB", 3

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return ("entry_point", "function", "perk_condition_tab_count")

		def unparse(self) -> bytes:
			"""
			Turn this record back into raw bytes for an ESP file.
			"""

			pack_struct, size = self.get_struct_and_size()
			size_field = struct.pack("<H", size)
			pack_items = [getattr(self, field_name) for field_name in self.get_field_names()]
			body = struct.pack(pack_struct, *pack_items)
			return b"DATA" + size_field + body

	class PRKC(Int8Record):
		"""
		Run On.
		"""

	class EPFT(Uint8Record):
		"""
		Entry Point Function Type.

		Determines the data type of the EPFD record - see https://tes5edit.github.io/fopdoc/Fallout3/Records/PERK.html
		"""

	class EPFD(FormIDRecord):
		"""
		Entry Point Function Data.

		May be a uint8[] or float32 or formid or null
		"""

	class EPF2(CStringRecord):
		"""
		Button Label.
		"""

	class EPF3(Uint16Record):
		"""
		Script Flags.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/PERK.html
		"""

	class PRKF(MarkerRecord):
		"""
		End Marker.
		"""


class PERK(Record):
	"""
	Perk.
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

		trait: int  # Enum - See https://tes5edit.github.io/fopdoc/Fallout3/Records/PERK.html
		min_level: int
		ranks: int
		playable: int  # Enum - See https://tes5edit.github.io/fopdoc/Fallout3/Records/PERK.html
		hidden: int  # Enum - See https://tes5edit.github.io/fopdoc/Fallout3/Records/PERK.html

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> RecordType:  # type: ignore[override]
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			unpack_struct, expected_size = cls.get_struct_and_size()
			size = struct.unpack("<H", raw_bytes.read(2))[0]
			if size == 8:
				# Effect subrecord collection version
				buf = BytesIO(struct.pack("<H", 8) + raw_bytes.read(8))
				return PerkEffect.DATAQuestStage.parse(buf)
			elif size == 4:
				# Effect subrecord collection version
				buf = BytesIO(struct.pack("<H", 4) + raw_bytes.read(4))
				return PerkEffect.DATAAbility.parse(buf)
			elif size == 3:
				# Effect subrecord collection version
				buf = BytesIO(struct.pack("<H", 3) + raw_bytes.read(3))
				return PerkEffect.DATAEntryPoint.parse(buf)

			if size != expected_size:
				raise ValueError(f"Size mismatch for {cls}: Expected {expected_size}, got {size}")
			return cls(*struct.unpack(unpack_struct, raw_bytes.read(size)))

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<BBBBB", 5

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return ("trait", "min_level", "ranks", "playable", "hidden")

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
			elif record_type in {b"FULL", b"DESC", b"ICON", b"MICO", b"DATA"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in PerkEffect.members:
				yield PerkEffect.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
