#!/usr/bin/env python3
#
#  subrecords.py
"""
Subrecord types used by multiple records.
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
from enum import IntEnum
from io import BytesIO
from typing import NamedTuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.types import BytesRecordType, CStringRecord, FormIDRecord, RecordType
from esp_parser.utils import NULL

__all__ = [
		"ACBS",
		"AIDT",
		"AidtAggroEnum",
		"AidtAssistanceEnum",
		"AidtConfidenceEnum",
		"AidtMoodEnum",
		"CTDA",
		"EDID",
		"Item",
		"Model",
		"OBND",
		"PositionRotation",
		"Script",
		"SkillEnum"
		]


class EDID(CStringRecord):
	"""
	Editor ID.
	"""


@attrs.define
class CTDA(RecordType):
	"""
	Condition.
	"""

	type: int  # see https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/CTDA.html
	unused: bytes

	#: A form ID or a float32 value
	comparison_value: bytes

	#: Function index.
	function: int  # see https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/CTDA.html

	#: First parameter to pass to the function.
	param1: bytes

	#: Second parameter to pass to the function.
	param2: bytes

	# See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/CTDA.html
	run_on: int

	reference: bytes
	"""
	A form ID of a :class:`~.PLYR`, :class:`~.ACHR`, :class:`~.ACRE`, :class:`~.REFR`,
	:class:`~.PMIS` or :class:`~.PGRE` reference on which to apply the function, or null.
	"""

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x1c\x00"  # size field
		return cls(
				type=struct.unpack(">B", raw_bytes.read(1))[0],
				unused=raw_bytes.read(3),
				comparison_value=raw_bytes.read(4),
				function=struct.unpack("<I", raw_bytes.read(4))[0],
				param1=raw_bytes.read(4),
				param2=raw_bytes.read(4),
				run_on=struct.unpack(">I", raw_bytes.read(4))[0],
				reference=raw_bytes.read(4),
				)

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		return b"".join([
				b"CTDA\x1c\x00",
				struct.pack(">B", self.type),
				self.unused,
				self.comparison_value,
				struct.pack("<I", self.function),
				self.param1,
				self.param2,
				struct.pack(">I", self.run_on),
				self.reference,
				])


class Model:
	"""
	Subrecords for models.
	"""

	class MODL(CStringRecord):
		"""
		Model Filename.
		"""

	class MODB(FormIDRecord):  # noqa: D106  # TODO
		pass


class Script:
	"""
	Subrecords for scripts.
	"""

	@attrs.define
	class SCHR(RecordType):
		"""
		Basic Script Data.
		"""

		unused: bytes = NULL
		ref_count: int = 0
		compiled_size: int = 0
		variable_count: int = 0
		type: int = 0  # TODO: enum
		flags: int = 1

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x14\x00"  # size field
			return cls(
					raw_bytes.read(4),
					*struct.unpack("<IIIHH", raw_bytes.read(16)),
					)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			packed_body = struct.pack(
					"<IIIHH",
					self.ref_count,
					self.compiled_size,
					self.variable_count,
					self.type,
					self.flags,
					)
			return b"SCHR\x14\x00" + self.unused + packed_body

	class SCDA(BytesRecordType):
		"""
		Compiled Script Source.
		"""

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			return cls(raw_bytes.read(*struct.unpack("<H", raw_bytes.read(2))))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			buffer_size = len(self)
			size_field = struct.pack("<H", buffer_size)
			return b"SCDA" + size_field + self

	class SCTX(BytesRecordType):
		"""
		Script Source.
		"""

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			return cls(raw_bytes.read(*struct.unpack("<H", raw_bytes.read(2))))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			buffer_size = len(self)
			size_field = struct.pack("<H", buffer_size)
			return b"SCTX" + size_field + self

	@attrs.define
	class SLSD(RecordType):
		"""
		Local Variable Data.
		"""

		index: int
		unused: bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		flags: int = 1
		unused_: bytes = b'\x00\x00\x00\x00\x00\x00\x00'

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x18\x00"
			return cls(*struct.unpack("<I12sB7s", raw_bytes.read(24)))
			# return cls(
			# 		*struct.unpack("<I", raw_bytes.read(4)),
			# 		raw_bytes.read(12),
			# 		*struct.unpack("<B", raw_bytes.read(1)),
			# 		raw_bytes.read(7),
			# 		)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			index_pack = struct.pack("<I", self.index)
			flags_pack = struct.pack("<B", self.flags)
			return b"SLSD" + b"\x18\x00" + index_pack + self.unused + flags_pack + self.unused_

	class SCVR(CStringRecord):
		"""
		Local Variable Name.
		"""

	class SCRO(FormIDRecord):
		"""
		Reference.

		A local variable reference, or the form ID of an :class:`~.ACTI`, :class:`~.DOOR`,
		:class:`~.STAT`, :class:`~.FURN`, :class:`~.CREA`, :class:`~.SPEL`, :class:`~.NPC_`,
		:class:`~.CONT`, :class:`~.ARMO`, :class:`~.AMMO`, :class:`~.MISC`, :class:`~.WEAP`,
		:class:`~.IMAD`, :class:`~.BOOK`, :class:`~.KEYM`, :class:`~.ALCH`, :class:`~.LIGH`,
		:class:`~.QUST`, :class:`~.PLYR`, :class:`~.PACK`, :class:`~.LVLI`, :class:`~.ECZN`,
		:class:`~.EXPL`, :class:`~.FLST`, :class:`~.IDLM`, :class:`~.PMIS`, :class:`~.FACT`,
		:class:`~.ACHR`, :class:`~.REFR`, :class:`~.ACRE`, :class:`~.GLOB`, :class:`~.DIAL`,
		:class:`~.CELL`, :class:`~.SOUN`, :class:`~.MGEF`, :class:`~.WTHR`, :class:`~.CLAS`,
		:class:`~.EFSH`, :class:`~.RACE`, :class:`~.LVLC`, :class:`~.CSTY`, :class:`~.WRLD`,
		:class:`~.SCPT`, :class:`~.IMGS`, :class:`~.MESG`, :class:`~.MSTT`, :class:`~.MUSC`,
		:class:`~.NOTE`, :class:`~.PERK`, :class:`~.PGRE`, :class:`~.PROJ`, :class:`~.LVLN`,
		:class:`~.WATR`, :class:`~.ENCH`, :class:`~.TREE`, :class:`~.TERM`, :class:`~.HAIR`,
		:class:`~.EYES`, :class:`~.ADDN` or :class:`~.NULL` record.
		"""


class OBND(NamedTuple):
	"""
	Object Bounds.
	"""

	X1: int = 0
	Y1: int = 0
	Z1: int = 0
	X2: int = 0
	Y2: int = 0
	Z2: int = 0

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x0c\x00"  # size field
		X1, Y1, Z1, X2, Y2, Z2 = struct.unpack("<hhhhhh", raw_bytes.read(12))

		return cls(X1, Y1, Z1, X2, Y2, Z2)

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		return b"OBND\x0c\x00" + struct.pack("<hhhhhh", *self)


RecordType.register(OBND)


@attrs.define
class ACBS(RecordType):
	"""
	Configuration.

	Used by the :class:`~.CREA` and :class:`~.NPC_` record types.
	"""

	flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/ACBS.html
	fatigue: int
	barter_gold: int

	level_or_level_mult: int
	"""
	Level or level multiplier.

	If the 0x00000080 flag is set, the value is divided by 1000 to give a multiplier.
	"""

	calc_min: int
	calc_max: int
	speed_multiplier: int

	#: Karma (Alignment)
	karma: float
	disposition_base: int
	template_flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/ACBS.html

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x18\x00"  # size field
		return cls(*struct.unpack("<IHHhHHHfhH", raw_bytes.read(24)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		packed = struct.pack(
				"<IHHhHHHfhH",
				self.flags,
				self.fatigue,
				self.barter_gold,
				self.level_or_level_mult,
				self.calc_min,
				self.calc_max,
				self.speed_multiplier,
				self.karma,
				self.disposition_base,
				self.template_flags
				)
		return b"ACBS\x18\x00" + packed


class AidtAggroEnum(IntEnum):
	"""
	Enum for ``AIDT.aggression``.
	"""

	Unaggressive = 0
	Aggressive = 1
	VeryAggressive = 2
	Frenzied = 3

	def __repr__(self) -> str:
		return str(int(self))


class AidtConfidenceEnum(IntEnum):
	"""
	Enum for ``AIDT.confidence``.
	"""

	Cowardly = 0
	Cautious = 1
	Average = 2
	Brave = 3
	Foolhardy = 4

	def __repr__(self) -> str:
		return str(int(self))


class AidtMoodEnum(IntEnum):
	"""
	Enum for ``AIDT.mood``.
	"""

	Neutral = 0
	Afraid = 1
	Annoyed = 2
	Cocky = 3
	Drugged = 4
	Pleasant = 5
	Angry = 6
	Sad = 7

	def __repr__(self) -> str:
		return str(int(self))


class AidtAssistanceEnum(IntEnum):
	"""
	Enum for ``AIDT.assistance``.
	"""

	Nobody = 0
	Allies = 1
	FriendsAllies = 2

	def __repr__(self) -> str:
		return str(int(self))


class SkillEnum(IntEnum):
	"""
	Enum for Skills (e.g. AI teaching, skill book).

	As used in the :class:`~.AIDT`, :class:`~.BOOK` and :class:`~.CLAS` record types.
	"""

	NONE = -1
	Barter = 0
	BigGuns = 1
	EnergyWeapons = 2
	Explosives = 3
	Lockpick = 4
	Medicine = 5
	MeleeWeapons = 6
	Repair = 7
	Science = 8
	SmallGuns = 9
	Sneak = 10
	Speech = 11
	Throwing = 12  # unused
	Unarmed = 13

	def __repr__(self) -> str:
		return str(int(self))


@attrs.define
class AIDT(RecordType):
	"""
	AI Data.

	Used by the :class:`~.CREA` and :class:`~.NPC_` record types.
	"""

	aggression: AidtAggroEnum
	confidence: AidtConfidenceEnum
	energy_level: int
	responsibility: int
	mood: AidtMoodEnum
	unused: bytes
	buys_sells_services_flags: int  # see https://tes5edit.github.io/fopdoc/Fallout3/Records/Values/Services.html
	teaches: SkillEnum
	max_training_level: int
	assistance: AidtAssistanceEnum
	aggro_radius_behaviour_flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/AIDT.html
	aggro_radius: int

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x14\x00"  # size field

		unpacked = struct.unpack("<BBBBB3sIbBbBi", raw_bytes.read(20))

		aggression = AidtAggroEnum(unpacked[0])
		confidence = AidtConfidenceEnum(unpacked[1])
		mood = AidtMoodEnum(unpacked[4])
		teaches = SkillEnum(unpacked[7])
		assistance = AidtAssistanceEnum(unpacked[9])

		return cls(
				aggression=aggression,
				confidence=confidence,
				energy_level=unpacked[2],
				responsibility=unpacked[3],
				mood=mood,
				unused=unpacked[5],
				buys_sells_services_flags=unpacked[6],
				teaches=teaches,
				max_training_level=unpacked[8],
				assistance=assistance,
				aggro_radius_behaviour_flags=unpacked[10],
				aggro_radius=unpacked[11],
				)

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		packed = struct.pack(
				"<BBBBB3sIbBbBi",
				self.aggression,
				self.confidence,
				self.energy_level,
				self.responsibility,
				self.mood,
				self.unused,
				self.buys_sells_services_flags,
				self.teaches,
				self.max_training_level,
				self.assistance,
				self.aggro_radius_behaviour_flags,
				self.aggro_radius,
				)
		return b"AIDT\x14\x00" + packed


class Item:
	"""
	Subrecords for items.
	"""

	class CNTO(NamedTuple):
		"""
		Item.
		"""

		item: bytes
		"""
		Form ID of the item.

		Form ID of an :class:`~ARMO`, :class:`~AMMO`, :class:`~MISC`,
		:class:`~WEAP`, :class:`~BOOK`, :class:`~LVLI`, :class:`~KEYM`,
		:class:`~ALCH`, :class:`~NOTE`, :class:`~MSTT` or :class:`~STAT` record.
		"""

		item_count: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<4si", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"CNTO\x08\x00" + struct.pack("<4si", *self)

	class COED(NamedTuple):
		"""
		Extra item data.
		"""

		owner: bytes
		"""
		Form ID of the owner.

		Form ID of an :class:`~NPC_` or :class:`~FSCT` record, or null.
		"""

		glob_var_req_rank: bytes
		"""
		Form ID of a :class:`~.GLOB` record, an integer representing the required rank, or null.

		If an integer representing the required rank it will be stored as the 4 bytes of a uint32 (little endian).
		"""

		condition: float

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x0c\x00"  # size field
			return cls(*struct.unpack("<4s4sf", raw_bytes.read(12)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"COED\x0c\x00" + struct.pack("<4s4sf", *self)

	RecordType.register(CNTO)
	RecordType.register(COED)


class PositionRotation:
	"""
	Subrecord for position/rotation.

	Used in :class:`~.REFR`, :class:`~.ACHR` and :class:`~.ACRE`.
	"""

	class DATA(NamedTuple):
		"""
		Position / Rotation.
		"""

		xp: float = 0.0
		yp: float = 0.0
		zp: float = 0.0
		xr: float = 0.0
		yr: float = 0.0
		zr: float = 0.0

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""
			assert raw_bytes.read(2) == b"\x18\x00"  # size field
			xp, yp, zp, xr, yr, zr = struct.unpack("<ffffff", raw_bytes.read(24))

			return cls(xp, yp, zp, xr, yr, zr)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"DATA\x18\x00" + struct.pack("<ffffff", *self)

	RecordType.register(DATA)
