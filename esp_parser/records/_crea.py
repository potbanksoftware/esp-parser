#!/usr/bin/env python3
#
#  _crea.py
"""
CREA record type.
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
from esp_parser.subrecords import ACBS, AIDT, EDID, OBND, Destruction, Item, Model
from esp_parser.types import (
		CStringRecord,
		Float32Record,
		FormIDRecord,
		IntEnum,
		IntEnumField,
		Record,
		RecordType,
		StructRecord,
		Uint8Record,
		Uint16Record,
		Uint32Record
		)

__all__ = ["CREA"]


class CREA(Record):
	"""
	Creature.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class SPLO(FormIDRecord):
		"""
		Actor Effect.

		FormID of a SPEL record.
		"""

	class EITM(FormIDRecord):
		"""
		Unarmed Attack Effect.

		FormID of a ENCH or SPEL record.
		"""

	class EAMT(Uint16Record):
		"""
		Unarmed Attack Animation.

		https://tes5edit.github.io/fopdoc/Fallout3/Records/Values/Attack%20Animations.html
		"""

	class NIFZ(List[bytes], RecordType):
		"""
		Model List.

		An array of model filenames (``.nif``).
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
			body = raw_bytes.read(size)
			return cls(body.split(b"\x00"))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			body = b"\00".join(self)
			size = len(body)
			size_field = struct.pack("<H", size)
			return b"NIFZ" + size_field + body

	class NIFT(List[int], RecordType):
		"""
		Texture File Hashes.
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
			return cls(struct.unpack(f"<{size}B", raw_bytes.read(size)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = len(self)
			size_field = struct.pack("<H", size)
			body = struct.pack(f"<{size}B", *self)
			return b"NIFT" + size_field + body

	@attrs.define
	class SNAM(StructRecord):
		"""
		Faction.
		"""

		# https://tes5edit.github.ioSubrecords/SNAM (CREA, NPC_).md
		# TODO: share with NPC_

		#: Form ID of a :class:`~.FACT` record.
		faction: bytes
		rank: int
		unused: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<4sB3s", 8

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return ("faction", "rank", "unused")

		# @classmethod
		# def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		# 	"""
		# 	Parse this subrecord.

		# 	:param raw_bytes: Raw bytes for this record
		# 	"""

		# 	assert raw_bytes.read(2) == b"\x08\x00"  # size field
		# 	return cls(*struct.unpack("<4sB3s", raw_bytes.read(8)))

		# def unparse(self) -> bytes:
		# 	"""
		# 	Turn this subrecord back into raw bytes for an ESP file.
		# 	"""

		# 	return b"SNAM" + struct.pack("<H4sB3s", 8, self.faction, self.rank, self.unused)

	class INAM(FormIDRecord):
		"""
		Death Item.

		FormID of a LVLI record.
		"""

	class VTCK(FormIDRecord):
		"""
		Voice.

		FormID of a VTYP record.
		"""

	class TPLT(FormIDRecord):
		"""
		Template.

		FormID of a CREA or LVLC record.
		"""

	class SCRI(FormIDRecord):
		"""
		Script.

		FormID of a SCPT record.
		"""

	class PKID(FormIDRecord):
		"""
		Package.

		FormID of a PACK record.
		"""

	class KFFZ(List[bytes], RecordType):
		"""
		Animatons.

		An array of animation filenames (``.kf``).
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
			body = raw_bytes.read(size)
			return cls(body.split(b"\x00"))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			body = b"\00".join(self)
			size = len(body)
			size_field = struct.pack("<H", size)
			return b"KFFZ" + size_field + body

	class DataTypeEnum(IntEnum):
		Animal = 0
		MutatedAnimal = 1
		MutatedInsect = 2
		Abomination = 3
		SuperMutant = 4
		FeralGhoul = 5
		Robot = 6
		Giant = 7

	@attrs.define
	class DATA(StructRecord):
		"""
		Data.
		"""

		type: "CREA.DataTypeEnum" = attrs.field(converter=lambda x: CREA.DataTypeEnum(x))
		combat_skill: int
		magic_skill: int
		stealth_skill: int
		health: int
		unused: bytes
		damage: int
		strength: int
		perception: int
		endurance: int
		charisma: int
		intelligence: int
		agility: int
		luck: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<BBBBh2shBBBBBBB", 17

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return (
					"type",
					"combat_skill",
					"magic_skill",
					"stealth_skill",
					"health",
					"unused",
					"damage",
					"strength",
					"perception",
					"endurance",
					"charisma",
					"intelligence",
					"agility",
					"luck",
					)

		# @classmethod
		# def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		# 	"""
		# 	Parse this subrecord.

		# 	:param raw_bytes: Raw bytes for this record
		# 	"""

		# 	assert raw_bytes.read(2) == b"\x11\x00"  # size field
		# 	return cls(*struct.unpack("<BBBBh2shBBBBBBB", raw_bytes.read(17)))

		# def unparse(self) -> bytes:
		# 	"""
		# 	Turn this subrecord back into raw bytes for an ESP file.
		# 	"""

		# 	return b"DATA\x11\x00" + struct.pack(
		# 			"<BBBBh2shBBBBBBB",
		# 			self.type,
		# 			self.combat_skill,
		# 			self.magic_skill,
		# 			self.stealth_skill,
		# 			self.health,
		# 			self.unused,
		# 			self.damage,
		# 			self.strength,
		# 			self.perception,
		# 			self.endurance,
		# 			self.charisma,
		# 			self.intelligence,
		# 			self.agility,
		# 			self.luck,
		# 			)

	class RNAM(Uint8Record):
		"""
		Attack Reach.
		"""

	class ZNAM(FormIDRecord):
		"""
		Combat Style.

		FormID of a CSTY record.
		"""

	class PNAM(FormIDRecord):
		"""
		Body Part Data.

		FormID of a BPTD record.
		"""

	class TNAM(Float32Record):
		"""
		Turning Speed.
		"""

	class BNAM(Float32Record):
		"""
		Base Scale.
		"""

	class WNAM(Float32Record):
		"""
		Foot Weight.
		"""

	class NAM4(Uint32Record):
		"""
		Impact Material Type.

		See https://tes5edit.github.io/fopdoc/FalloutNV/Records/Values/Impact%20Material%20Types.html for enum values.
		"""

	class NAM5(Uint32Record):
		"""
		Sound Level.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/Values/Sound%20Levels.html for enum values.
		"""

	class CSCR(FormIDRecord):
		"""
		FormID of a CREA record to inherit sounds from.
		"""

	class CSDT(IntEnumField):
		"""
		Sound Type.
		"""

		LeftFoot = 0
		RightFoot = 1
		LeftBackFoot = 2
		RightBackFoot = 3
		Idle = 4
		Aware = 5
		Attack = 6
		Hit = 7
		Death = 8
		Weapon = 9
		MovementLoop = 10
		ConsciousLoop = 11
		Auxiliary1 = 12
		Auxiliary2 = 13
		Auxiliary3 = 14
		Auxiliary4 = 15
		Auxiliary5 = 16
		Auxiliary6 = 17
		Auxiliary7 = 18
		Auxiliary8 = 19
		Jump = 20
		PlayRandomOrLoop = 21

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x04\x00"
			return cls(*struct.unpack("<I", raw_bytes.read(4)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return self.__class__.__name__.encode() + struct.pack("<HI", 4, self)

	class CSDI(FormIDRecord):
		"""
		Sound.

		Form ID of a :class:`~.SOUN` record, or null.
		"""

	class CSDC(Uint8Record):
		"""
		Sound Chance.
		"""

	class CNAM(FormIDRecord):
		"""
		Impact Dataset.

		FormID of a IPDS record.
		"""

	class LNAM(FormIDRecord):
		"""
		Melee Weapon List.

		FormID of a FLST record.
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
			elif record_type == b"ACBS":
				yield ACBS.parse(raw_bytes)
			elif record_type == b"AIDT":
				yield AIDT.parse(raw_bytes)
			elif record_type in {
					b"FULL",
					b"SPLO",
					b"EITM",
					b"EAMT",
					b"NIFZ",
					b"NIFT",
					b"SNAM",
					b"INAM",
					b"VTCK",
					b"TPLT",
					b"SCRI",
					b"PKID",
					b"KFFZ",
					b"DATA",
					b"RNAM",
					b"ZNAM",
					b"PNAM",
					b"TNAM",
					b"BNAM",
					b"WNAM",
					b"NAM4",
					b"NAM5",
					b"CSCR",
					b"CNAM",
					b"LNAM",
					b"CSDT",
					b"CSDI",
					b"CSDC",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			elif record_type in Destruction.members:
				yield Destruction.parse_member(record_type, raw_bytes)
			elif record_type in Item.members:
				yield Item.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
