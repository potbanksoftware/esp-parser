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
from io import BytesIO
from typing import List, NamedTuple, Tuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.types import (
		BytesRecordType,
		Collection,
		CStringRecord,
		FormIDRecord,
		Int32Record,
		IntEnum,
		MarkerRecord,
		RecordType,
		StructRecord
		)
from esp_parser.utils import NULL, namedtuple_qualname_repr

__all__ = [
		"ACBS",
		"AIDT",
		"AidtAggroEnum",
		"AidtAssistanceEnum",
		"AidtConfidenceEnum",
		"AidtMoodEnum",
		"CTDA",
		"Destruction",
		"DialType",
		"EDID",
		"Effect",
		"InfoNextSpeaker",
		"Item",
		"Model",
		"OBND",
		"PositionRotation",
		"Script",
		"SkillEnum",
		"XNAM",
		"XnamCombatReactionEnum"
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
	A form ID of a :class:`~.ACHR`, :class:`~.ACRE`, :class:`~.REFR`,
	:class:`~.PMIS` or :class:`~.PGRE` reference on which to apply the function, or null.
	"""

	# Also refers to :class:`~.PLYR` which doesn't exist.

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


class Model(Collection):
	"""
	Subrecords for models.
	"""

	members = {b"MODL", b"MODB", b"MODS"}

	class MODL(CStringRecord):
		"""
		Model Filename.
		"""

	class MODB(FormIDRecord):  # noqa: D106  # TODO
		pass

	@attrs.define
	class AlternateTexture:
		"""
		A texture in a :class:`~Model.MODS`.
		"""

		#: 3D Name
		name: bytes
		#: New Texture. Form ID of a :class:`~.TXST` record.
		texture: bytes
		index: int

		@classmethod
		def unpack(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Unpack bytes for the :class:`~.Model.AlternateTexture`.
			"""

			alt_texture_name_length = struct.unpack("<I", raw_bytes.read(4))[0]
			alt_texture_3d_name = raw_bytes.read(alt_texture_name_length)
			alt_texture_new_texture, alt_texture_3d_index = struct.unpack("<4si", raw_bytes.read(8))
			return cls(
					alt_texture_3d_name,
					alt_texture_new_texture,
					alt_texture_3d_index,
					)

		def pack(self) -> bytes:
			"""
			Pack the :class:`~.Model.AlternateTexture` to bytes.
			"""

			name_length = len(self.name)
			return struct.pack(f"<I{name_length}s4si", name_length, self.name, self.texture, self.index)

	class MODS(List[AlternateTexture], RecordType):
		"""
		List of alternate textures.
		"""

		def __repr__(self) -> str:
			return f"{self.__class__.__qualname__}({super().__repr__()})"

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size, count = struct.unpack("<HI", raw_bytes.read(6))

			buf = BytesIO(raw_bytes.read(size - 4))  # -4 for the count field already read

			alt_textures = cls()
			for _ in range(count):
				alt_textures.append(Model.AlternateTexture.unpack(buf))

			assert not buf.read()
			assert len(alt_textures) == count
			return alt_textures

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			alt_textures = b"".join(at.pack() for at in self)
			alt_textures_size = len(alt_textures)
			size = alt_textures_size + 4  # +4 for count field
			count = len(self)
			return b"MODS" + struct.pack("<HI", size, count) + alt_textures


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

	class SCRV(Int32Record):
		"""
		Referenced Variable.
		"""
		# Maybe?

	class SCRO(FormIDRecord):
		"""
		Reference.

		A local variable reference, or the form ID of an :class:`~.ACTI`, :class:`~.DOOR`,
		:class:`~.STAT`, :class:`~.FURN`, :class:`~.CREA`, :class:`~.SPEL`, :class:`~.NPC_`,
		:class:`~.CONT`, :class:`~.ARMO`, :class:`~.AMMO`, :class:`~.MISC`, :class:`~.WEAP`,
		:class:`~.IMAD`, :class:`~.BOOK`, :class:`~.KEYM`, :class:`~.ALCH`, :class:`~.LIGH`,
		:class:`~.QUST`, :class:`~.PACK`, :class:`~.LVLI`, :class:`~.ECZN`,
		:class:`~.EXPL`, :class:`~.FLST`, :class:`~.IDLM`, :class:`~.PMIS`, :class:`~.FACT`,
		:class:`~.ACHR`, :class:`~.REFR`, :class:`~.ACRE`, :class:`~.GLOB`, :class:`~.DIAL`,
		:class:`~.CELL`, :class:`~.SOUN`, :class:`~.MGEF`, :class:`~.WTHR`, :class:`~.CLAS`,
		:class:`~.EFSH`, :class:`~.RACE`, :class:`~.LVLC`, :class:`~.CSTY`, :class:`~.WRLD`,
		:class:`~.SCPT`, :class:`~.IMGS`, :class:`~.MESG`, :class:`~.MSTT`, :class:`~.MUSC`,
		:class:`~.NOTE`, :class:`~.PERK`, :class:`~.PGRE`, :class:`~.PROJ`, :class:`~.LVLN`,
		:class:`~.WATR`, :class:`~.ENCH`, :class:`~.TREE`, :class:`~.TERM`, :class:`~.HAIR`,
		:class:`~.EYES`, :class:`~.ADDN` record, or null.
		"""

		# Also refers to :class:`~.PLYR` which doesn't exist.


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


class AidtConfidenceEnum(IntEnum):
	"""
	Enum for ``AIDT.confidence``.
	"""

	Cowardly = 0
	Cautious = 1
	Average = 2
	Brave = 3
	Foolhardy = 4


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


class AidtAssistanceEnum(IntEnum):
	"""
	Enum for ``AIDT.assistance``.
	"""

	Nobody = 0
	Allies = 1
	FriendsAllies = 2


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


class Item(Collection):
	"""
	Subrecords for items.
	"""

	members = {b"CNTO", b"COED"}

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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class COED(NamedTuple):
		"""
		Extra item data.
		"""

		owner: bytes
		"""
		Form ID of the owner.

		Form ID of an :class:`~.NPC_` or :class:`~.FACT` record, or null.
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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(DATA)


class XnamCombatReactionEnum(IntEnum):
	"""
	Group Combat Reaction.
	"""

	Neutral = 0
	Enemy = 1
	Ally = 2
	Friend = 3


@attrs.define
class XNAM(RecordType):
	"""
	Relation used for :class:`~.FACT` and :class:`~.RACE` records.
	"""

	#: Form ID of a :class:`~.FACT` or :class:`~.RACE` record.
	faction: bytes

	modifier: int

	group_combat_reaction: XnamCombatReactionEnum

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this subrecord.

		:param raw_bytes: Raw bytes for this record
		"""

		assert raw_bytes.read(2) == b"\x0c\x00"  # size field
		return cls(*struct.unpack("<4siI", raw_bytes.read(12)))

	def unparse(self) -> bytes:
		"""
		Turn this subrecord back into raw bytes for an ESP file.
		"""

		return b"XNAM\x0c\x00" + struct.pack("<4siI", self.faction, self.modifier, self.group_combat_reaction)


class DialType(IntEnum):
	"""
	Enum for ``DIAL.DATA.type`` and ``INFO.DATA.type``.
	"""

	Topic = 0
	Conversation = 1
	Combat = 2
	Persuasion = 3
	Detection = 4
	Service = 5
	Miscellaneous = 6
	Radio = 7


class InfoNextSpeaker(IntEnum):
	"""
	Enum for ``INFO.DATA.next_speaker``.
	"""

	Target = 0
	Self = 1
	Either = 2


class Destruction(Collection):
	"""
	Destruction subrecord collection.
	"""

	members = {
			b"DEST",
			b"DSTD",
			b"DSTF",
			}

	@attrs.define
	class DEST(RecordType):
		"""
		Destruction data header.
		"""

		health: int
		count: int
		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Destruction.html
		unknown: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<iBB2s", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DEST" + struct.pack(
					"<HiBB2s",
					8,
					self.health,
					self.count,
					self.flags,
					self.unknown,
					)

	@attrs.define
	class DSTD(RecordType):
		"""
		Destruction Stage Data.
		"""

		health_percentage: int
		index: int
		damage_stage: int
		flags: int  # See https://tes5edit.github.io/fopdoc/FalloutNV/Records/Subrecords/Destruction.html
		self_dps: int

		#: Form ID of an :class:`~.EXPL` record or null.
		explosion: bytes

		#: Form ID of an :class:`~.DEBR` record or null.
		debris: bytes

		debris_count: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x14\x00"  # size field
			return cls(*struct.unpack("<BBBBi4s4si", raw_bytes.read(20)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DSTD" + struct.pack(
					"<HBBBBi4s4si",
					20,
					self.health_percentage,
					self.index,
					self.damage_stage,
					self.flags,
					self.self_dps,
					self.explosion,
					self.debris,
					self.debris_count,
					)

	class DSTF(MarkerRecord):
		"""
		Stage End Marker.
		"""


class Effect(Collection):
	"""
	Effect Subrecord Collection.
	"""

	members = {b"EFIT", b"EFID"}

	class EFID(FormIDRecord):
		"""
		Base effect.

		Form ID of a :class:`~.MGEF` record.
		"""

	class EfitTypeEnum(IntEnum):
		"""
		Enum for ``SPEL.EFIT``.
		"""

		Self = 0
		Touch = 1
		Target = 2

	@attrs.define
	class EFIT(StructRecord):
		"""
		Effect Data.
		"""

		magnitude: int
		area: int
		duration: int
		type: "Effect.EfitTypeEnum" = attrs.field(converter=lambda x: Effect.EfitTypeEnum(x))
		actor_value: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Effect.html

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<IIIIi", 20

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return (
					"magnitude",
					"area",
					"duration",
					"type",
					"actor_value",
					)
