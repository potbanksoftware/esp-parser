#!/usr/bin/env python3
#
#  _npc_.py
r"""
NPC\_ record type.
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
from typing import Iterator, NamedTuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import ACBS, AIDT, EDID, OBND, Item, Model
from esp_parser.types import (
		BytesRecordType,
		CStringRecord,
		FaceGenRecord,
		Float32Record,
		FormIDRecord,
		IntEnumField,
		Record,
		RecordType,
		Uint16Record
		)
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["NPC_"]


class NPC_(Record):
	"""
	Non-Player Character.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class INAM(FormIDRecord):
		"""
		Death Item.

		Form ID of a :class:`~.LVLI` record.
		"""

	class VTCK(FormIDRecord):
		"""
		Voice.

		Form ID of a :class:`~.VTYP` record.
		"""

	class TPLT(FormIDRecord):
		"""
		Template.

		Form ID of an :class:`~.NPC_` or :class:`~.LVLN` record.
		"""

	class RNAM(FormIDRecord):
		"""
		Race.

		Form ID of a :class:`~.RACE`.
		"""

	class EITM(FormIDRecord):
		"""
		Unarmed Attack Effect.

		Form ID of an :class:`~.ENCH` or :class:`~.SPEL`.
		"""

	class EAMT(IntEnumField):
		"""
		Unarmed Attack Animation.
		"""

		AttackLeft = 26
		AttackLeftUp = 27
		AttackLeftDown = 28
		AttackLeftIS = 29
		AttackLeftISUp = 30
		AttackLeftISDown = 31
		AttackRight = 32
		AttackRightUp = 33
		AttackRightDown = 34
		AttackRightIS = 35
		AttackRightISUp = 36
		AttackRightISDown = 37
		Attack3 = 38
		Attack3Up = 39
		Attack3Down = 40
		Attack3IS = 41
		Attack3ISUp = 42
		Attack3ISDown = 43
		Attack4 = 44
		Attack4Up = 45
		Attack4Down = 46
		Attack4IS = 47
		Attack4ISUp = 48
		Attack4ISDown = 49
		Attack5 = 50
		Attack5Up = 51
		Attack5Down = 52
		Attack5IS = 53
		Attack5ISUp = 54
		Attack5ISDown = 55
		Attack6 = 56
		Attack6Up = 57
		Attack6Down = 58
		Attack6IS = 59
		Attack6ISUp = 60
		Attack6ISDown = 61
		Attack7 = 62
		Attack7Up = 63
		Attack7Down = 64
		Attack7IS = 65
		Attack7ISUp = 66
		Attack7ISDown = 67
		Attack8 = 68
		Attack8Up = 69
		Attack8Down = 70
		Attack8IS = 71
		Attack8ISUp = 72
		Attack8ISDown = 73
		AttackLoop = 74
		AttackLoopUp = 75
		AttackLoopDown = 76
		AttackLoopIS = 77
		AttackLoopISUp = 78
		AttackLoopISDown = 79
		AttackSpin = 80
		AttackSpinUp = 81
		AttackSpinDown = 82
		AttackSpinIS = 83
		AttackSpinISUp = 84
		AttackSpinISDown = 85
		AttackSpin2 = 86
		AttackSpin2Up = 87
		AttackSpin2Down = 88
		AttackSpin2IS = 89
		AttackSpin2ISUp = 90
		AttackSpin2ISDown = 91
		AttackPower = 92
		AttackForwardPower = 93
		AttackBackPower = 94
		AttackLeftPower = 95
		AttackRightPower = 96
		PlaceMine = 97
		PlaceMineUp = 98
		PlaceMineDown = 99
		PlaceMineIS = 100
		PlaceMineISUp = 101
		PlaceMineISDown = 102
		PlaceMine2 = 103
		PlaceMine2Up = 104
		PlaceMine2Down = 105
		PlaceMine2IS = 106
		PlaceMine2ISUp = 107
		PlaceMine2ISDown = 108
		AttackThrow = 109
		AttackThrowUp = 110
		AttackThrowDown = 111
		AttackThrowIS = 112
		AttackThrowISUp = 113
		AttackThrowISDown = 114
		AttackThrow2 = 115
		AttackThrow2Up = 116
		AttackThrow2Down = 117
		AttackThrow2IS = 118
		AttackThrow2ISUp = 119
		AttackThrow2ISDown = 120
		AttackThrow3 = 121
		AttackThrow3Up = 122
		AttackThrow3Down = 123
		AttackThrow3IS = 124
		AttackThrow3ISUp = 125
		AttackThrow3ISDown = 126
		AttackThrow4 = 127
		AttackThrow4Up = 128
		AttackThrow4Down = 129
		AttackThrow4IS = 130
		AttackThrow4ISUp = 131
		AttackThrow4ISDown = 132
		AttackThrow5 = 133
		AttackThrow5Up = 134
		AttackThrow5Down = 135
		AttackThrow5IS = 136
		AttackThrow5ISUp = 137
		AttackThrow5ISDown = 138
		PipBoy = 167
		PipBoyChild = 178
		ANY = 255

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x02\x00"
			return cls(*struct.unpack("<H", raw_bytes.read(2)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"EAMT" + struct.pack("<HH", 2, self)

	class SCRI(FormIDRecord):
		"""
		Script.

		Form ID of a :class:`~.SCPT` record.
		"""

	class CNAM(FormIDRecord):
		"""
		Class.

		Form ID of a :class:`~.CLAS` record.
		"""

	class DATA(NamedTuple):
		"""
		Health and SPECIAL attributes.
		"""

		base_health: int
		strength: int
		perception: int
		endurance: int
		charisma: int
		intelligence: int
		agility: int
		luck: int
		# unused: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x0b\x00"  # size field
			return cls(*struct.unpack("<iBBBBBBB", raw_bytes.read(11)))
			assert raw_bytes.read(2) == b"\x0c\x00"  # size field
			return cls(*struct.unpack("<iBBBBBBBB", raw_bytes.read(12)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA\x0b\x00" + struct.pack("<iBBBBBBB", *self)
			return b"DATA\x0c\x00" + struct.pack("<iBBBBBBBB", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	@attrs.define
	class DNAM(RecordType):
		"""
		Skills.
		"""

		barter: int
		big_guns: int
		energy_weapons: int
		explosives: int
		lockpick: int
		medicine: int
		melee_weapons: int
		repair: int
		science: int

		#: 'Guns' in Fallout New Vegas
		small_guns: int
		sneak: int
		speech: int

		#: Unused Throwing skill in Fallout 3
		survival: int
		unarmed: int
		barter_offset: int
		big_guns_offset: int
		energy_weapons_offset: int
		explosives_offset: int
		lockpick_offset: int
		medicine_offset: int
		melee_weapons_offset: int
		repair_offset: int
		science_offset: int
		small_guns_offset: int
		sneak_offset: int
		speech_offset: int

		#: Unused Throwing skill in Fallout 3
		survival_offset: int
		unarmed_offset: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x1c\x00"  # size field
			return cls(*struct.unpack("<BBBBBBBBBBBBBBBBBBBBBBBBBBBB", raw_bytes.read(28)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DNAM\x1c\x00" + struct.pack(
					"<BBBBBBBBBBBBBBBBBBBBBBBBBBBB",
					self.barter,
					self.big_guns,
					self.energy_weapons,
					self.explosives,
					self.lockpick,
					self.medicine,
					self.melee_weapons,
					self.repair,
					self.science,
					self.small_guns,
					self.sneak,
					self.speech,
					self.survival,
					self.unarmed,
					self.barter_offset,
					self.big_guns_offset,
					self.energy_weapons_offset,
					self.explosives_offset,
					self.lockpick_offset,
					self.medicine_offset,
					self.melee_weapons_offset,
					self.repair_offset,
					self.science_offset,
					self.small_guns_offset,
					self.sneak_offset,
					self.speech_offset,
					self.survival_offset,
					self.unarmed_offset,
					)

	class PNAM(FormIDRecord):
		"""
		Head Part.

		Form ID of a :class:`~.HDPT` record.
		"""

	class HNAM(FormIDRecord):
		"""
		Hair.

		Form ID of a :class:`~.HAIR` record.
		"""

	class LNAM(Float32Record):
		"""
		Hair Length.
		"""

	class ENAM(FormIDRecord):
		"""
		Eyes.

		Form ID of a :class:`~.EYES` record.
		"""

	class HCLR(BytesRecordType):
		"""
		Hair Color.

		RGBA as bytes.
		"""

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x04\x00"
			return cls(raw_bytes.read(4))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"HCLR" + b"\x04\x00" + bytes(self)

	class ZNAM(FormIDRecord):
		"""
		Combat Style.

		Form ID of a :class:`~.CSTY` record.
		"""

	class NAM4(IntEnumField):
		"""
		Impact Material Type.
		"""

		stone = 0
		dirt = 1
		grass = 2
		glass = 3
		metal = 4
		wood = 5
		organic = 6
		cloth = 7
		water = 8
		hollow_metal = 9
		organic_bug = 10
		organic_glow = 11

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

			return b"NAM4" + struct.pack("<HI", 4, self)

	RecordType.register(DATA)
	RecordType.register(EAMT)
	RecordType.register(NAM4)

	class FGGS(FaceGenRecord):
		"""
		FaceGen Geometry-Symmetric.
		"""

	class FGGA(FaceGenRecord):
		"""
		FaceGen Geometry-Asymmetric.
		"""

	class FGTS(FaceGenRecord):
		"""
		FaceGen Texture-Symmetric.
		"""

	class NAM5(Uint16Record):
		"""
		Unknown.
		"""

	class NAM6(Float32Record):
		"""
		Height.
		"""

	class NAM7(Float32Record):
		"""
		Weight.
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

			if record_type in b"EDID":
				yield EDID.parse(raw_bytes)
			elif record_type == b"OBND":
				yield OBND.parse(raw_bytes)
			elif record_type == b"ACBS":
				yield ACBS.parse(raw_bytes)
			elif record_type == b"AIDT":
				yield AIDT.parse(raw_bytes)
			elif record_type in {
					b"FULL",
					b"INAM",
					b"VTCK",
					b"TPLT",
					b"RNAM",
					b"EITM",
					b"EAMT",
					b"SCRI",
					b"CNAM",
					b"PNAM",
					b"HNAM",
					b"ENAM",
					b"ZNAM",
					b"DATA",
					b"DNAM",
					b"HCLR",
					b"NAM4",
					b"FGGS",
					b"FGGA",
					b"FGTS",
					b"NAM5",
					b"NAM6",
					b"NAM7",
					b"LNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			elif record_type in Item.members:
				yield Item.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
