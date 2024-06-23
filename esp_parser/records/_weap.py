#!/usr/bin/env python3
#
#  _weap.py
"""
WEAP record type.
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
from esp_parser.subrecords import EDID, OBND, Model
from esp_parser.types import (
		CStringRecord,
		FormIDRecord,
		Int16Record,
		Int32Record,
		Record,
		RecordType,
		Uint32Record
		)
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["WEAP"]


class WEAP(Record):
	"""
	Weapon.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class ICON(CStringRecord):
		"""
		Large icon filename.
		"""

	class MICO(CStringRecord):
		"""
		Small icon filename.
		"""

	class SCRI(FormIDRecord):
		"""
		Script.

		Form ID of a SCPT record.
		"""

	class EITM(FormIDRecord):
		"""
		Object Effect.

		Form ID of an ENCH or SPEL record.
		"""

	class EAMT(Int16Record):
		"""
		Enchantment Charge Amount.
		"""

	class NAM0(FormIDRecord):
		"""
		Ammo.

		Form ID of an AMMO or FLST record.
		"""

	class REPL(FormIDRecord):
		"""
		Repair List.

		Form ID of a FLST record.
		"""

	class ETYP(Int32Record):
		"""
		Equipment Type.
		"""

	class BIPL(FormIDRecord):
		"""
		Biped Model List.

		Form ID of a FLST record.
		"""

	class YNAM(FormIDRecord):
		"""
		Sound - Pick Up.

		Form ID of a :class:`~.SOUN` record.
		"""

	class ZNAM(FormIDRecord):
		"""
		Sound - Drop.

		Form ID of a :class:`~.SOUN` record.
		"""

	class EFSD(FormIDRecord):
		"""
		Scope Effect.

		Form ID of an EFSH record.
		"""

	class MWD1(CStringRecord):
		"""
		Model With Mod 1 (New Vegas only).
		"""

	class MWD2(CStringRecord):
		"""
		Model With Mod 2 (New Vegas only).
		"""

	class MWD3(CStringRecord):
		"""
		Model With Mods 1 and 2 (New Vegas only).
		"""

	class MWD4(CStringRecord):
		"""
		Model With Mod 3 (New Vegas only).
		"""

	class MWD5(CStringRecord):
		"""
		Model With Mods 1 and 3 (New Vegas only).
		"""

	class MWD6(CStringRecord):
		"""
		Model With Mods 2 and 3 (New Vegas only).
		"""

	class MWD7(CStringRecord):
		"""
		Model With Mods 1, 2 and 3 (New Vegas only).
		"""

	class VANM(CStringRecord):
		"""
		VATS Attack Name (New Vegas only).
		"""

	class NNAM(CStringRecord):
		"""
		Embedded Weapon Node.
		"""

	class INAM(FormIDRecord):
		"""
		Impact Dataset.

		Form ID of a :class:`~.IPDS` record.
		"""

	class WNAM(FormIDRecord):
		"""
		First Person Model.

		Form ID of a :class:`~.STAT` record.
		"""

	class WNM1(FormIDRecord):
		"""
		1st Person Model With Mod 1 (New Vegas only).

		Form ID of a :class:`~.STAT` record.
		"""

	class WNM2(FormIDRecord):
		"""
		1st Person Model With Mod 2 (New Vegas only).

		Form ID of a :class:`~.STAT` record.
		"""

	class WNM3(FormIDRecord):
		"""
		1st Person Model With Mods 1 and 2 (New Vegas only).

		Form ID of a :class:`~.STAT` record.
		"""

	class WNM4(FormIDRecord):
		"""
		1st Person Model With Mod 3 (New Vegas only).

		Form ID of a :class:`~.STAT` record.
		"""

	class WNM5(FormIDRecord):
		"""
		1st Person Model With Mods 1 and 3 (New Vegas only).

		Form ID of a :class:`~.STAT` record.
		"""

	class WNM6(FormIDRecord):
		"""
		1st Person Model With Mods 2 and 3 (New Vegas only).

		Form ID of a :class:`~.STAT` record.
		"""

	class WNM7(FormIDRecord):
		"""
		1st Person Model With Mods 1, 2 and 3 (New Vegas only).

		Form ID of a :class:`~.STAT` record.
		"""

	class WMI1(FormIDRecord):
		"""
		Weapon Mod 1 (New Vegas only).

		Form ID of an :class:`~.IMOD` record.
		"""

	class WMI2(FormIDRecord):
		"""
		Weapon Mod 2 (New Vegas only).

		Form ID of an :class:`~.IMOD` record.
		"""

	class WMI3(FormIDRecord):
		"""
		Weapon Mod 3 (New Vegas only).

		Form ID of an :class:`~.IMOD` record.
		"""

	class SNAM(FormIDRecord):
		"""
		Sound - Gun - Shoot 3D.

		Form ID of a :class:`~.SOUN` record.
		"""

	class XNAM(FormIDRecord):
		"""
		Sound - Gun - Shoot 2D.

		Form ID of a :class:`~.SOUN` record.
		"""

	class NAM7(FormIDRecord):
		"""
		Sound - Gun - Shoot 3D Looping.

		Form ID of a :class:`~.SOUN` record.
		"""

	class TNAM(FormIDRecord):
		"""
		Sound - Melee - Swing / Gun - No Ammo.

		Form ID of a :class:`~.SOUN` record.
		"""

	class NAM6(FormIDRecord):
		"""
		Sound - Block.

		Form ID of a :class:`~.SOUN` record.
		"""

	class UNAM(FormIDRecord):
		"""
		Sound - Idle.

		Form ID of a :class:`~.SOUN` record.
		"""

	class NAM9(FormIDRecord):
		"""
		Sound - Equip.

		Form ID of a :class:`~.SOUN` record.
		"""

	class NAM8(FormIDRecord):
		"""
		Sound - Unequip.

		Form ID of a :class:`~.SOUN` record.
		"""

	# class WMS1(FormIDRecord):
	# 	"""
	# 	Sound - Mod 1 - Shoot 3D (New Vegas only).
	# 	FormID of a SOUN record.
	# 	"""

	# class WMS1(FormIDRecord):
	# 	"""
	# 	Sound - Mod 1 - Shoot Dist (New Vegas only).
	# 	FormID of a SOUN record.
	# 	"""

	# class WMS2(FormIDRecord):
	# 	"""
	# 	Sound - Mod 1 - Shoot 2D (New Vegas only).
	# 	FormID of a SOUN record.
	# 	"""

	class DATA(NamedTuple):
		"""
		Weapon value, health (conditon), weight etc.
		"""

		value: int
		health: int
		weight: float
		base_damage: int
		clip_size: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x0f\x00"  # size field
			return cls(*struct.unpack("<iifhB", raw_bytes.read(15)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA\x0f\x00" + struct.pack("<iifhB", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(DATA)

	@attrs.define
	class DNAM(RecordType):
		"""
		Weapon animation, projectile, mod data etc.
		"""

		# # See https://tes5edit.github.io/fopdoc/Fallout3/Records/WEAP.html for enum and flag values
		animation_type: int  # enum
		animation_multiplier: float
		reach: float
		flags: int
		grip_animation: int  # enum
		ammo_use: int
		reload_animation: int  # enum
		min_spread: float
		spread: float
		unknown: bytes
		sight_fov: float
		unused: bytes

		#: 4-byte form id of a :class:`~.PROJ` record, or null.
		projectile: bytes
		base_vats_hit_chance: int
		attack_animation: int  # enum
		projectile_count: int
		embedded_weapon_actor_value: int  # enum
		min_range: float
		max_range: float
		on_hit: int  # enum
		flags_: int
		animation_attack_multiplier: float
		fire_rate: float
		override_action_points: float
		rumble_left_motor_strength: float
		rumble_right_motor_strength: float
		rumble_duration: float
		override_damage_to_weapon_mult: float
		attack_shots_per_sec: float
		reload_time: float
		jam_time: float
		aim_arc: float
		skill: int  # enum
		rumble_pattern: int  # enum
		rumble_wavelength: float
		limb_damage_multiplier: float
		resistance_type: int  # enum
		sight_usage: float
		semi_automatic_fire_delay_min: float
		semi_automatic_fire_delay_max: float

		# The following are New Vegas only
		unknown__: float = 0
		effect_mod_1: int = 0
		effect_mod_2: int = 0
		effect_mod_3: int = 0
		value_a_mod_1: float = 0
		value_a_mod_2: float = 0
		value_a_mod_3: float = 0
		power_attack_animation_override: int = 0
		strength_requirement: int = 0
		unknown___: bytes = b''
		reload_animation_mod: int = 0
		unknown____: bytes = b''
		regen_rate: float = 0
		kill_impulse: float = 0
		value_b_mod_1: float = 0
		value_b_mod_2: float = 0
		value_b_mod_3: float = 0
		impulse_dist: float = 0
		skill_requirement: int = 0

		#: Indicates that the New Vegas-specific fields should be included with ``unparse()``.
		new_vegas: bool = False

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size = struct.unpack("<H", raw_bytes.read(2))[0]
			unpack_string = "<IffBBBBff4sf4s4sBBBBffIIfffffffffffiIffifff"

			if size == 204:
				# New Vegas
				unpack_string += "fIIIfffIIsB2sffffffI"
				return cls(  # type: ignore[misc]  # false positive re: new_vegas=True being there twice (it isn't)
					*struct.unpack(unpack_string, raw_bytes.read(size)),
					new_vegas=True,
					)
			else:
				assert size == 136

				# Fallout 3
				return cls(*struct.unpack(unpack_string, raw_bytes.read(size)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			if self.new_vegas:
				packed = struct.pack(
						"<IffBBBBff4sf4s4sBBBBffIIfffffffffffiIffiffffIIIfffIIsB2sffffffI",
						self.animation_type,
						self.animation_multiplier,
						self.reach,
						self.flags,
						self.grip_animation,
						self.ammo_use,
						self.reload_animation,
						self.min_spread,
						self.spread,
						self.unknown,
						self.sight_fov,
						self.unused,
						self.projectile,
						self.base_vats_hit_chance,
						self.attack_animation,
						self.projectile_count,
						self.embedded_weapon_actor_value,
						self.min_range,
						self.max_range,
						self.on_hit,
						self.flags_,
						self.animation_attack_multiplier,
						self.fire_rate,
						self.override_action_points,
						self.rumble_left_motor_strength,
						self.rumble_right_motor_strength,
						self.rumble_duration,
						self.override_damage_to_weapon_mult,
						self.attack_shots_per_sec,
						self.reload_time,
						self.jam_time,
						self.aim_arc,
						self.skill,
						self.rumble_pattern,
						self.rumble_wavelength,
						self.limb_damage_multiplier,
						self.resistance_type,
						self.sight_usage,
						self.semi_automatic_fire_delay_min,
						self.semi_automatic_fire_delay_max,
						self.unknown__,
						self.effect_mod_1,
						self.effect_mod_2,
						self.effect_mod_3,
						self.value_a_mod_1,
						self.value_a_mod_2,
						self.value_a_mod_3,
						self.power_attack_animation_override,
						self.strength_requirement,
						self.unknown___,
						self.reload_animation_mod,
						self.unknown____,
						self.regen_rate,
						self.kill_impulse,
						self.value_b_mod_1,
						self.value_b_mod_2,
						self.value_b_mod_3,
						self.impulse_dist,
						self.skill_requirement,
						)
			else:
				# FO3 Only
				packed = struct.pack(
						"<IffBBBBff4sf4s4sBBBBffIIfffffffffffiIffifff",
						self.animation_type,
						self.animation_multiplier,
						self.reach,
						self.flags,
						self.grip_animation,
						self.ammo_use,
						self.reload_animation,
						self.min_spread,
						self.spread,
						self.unknown,
						self.sight_fov,
						self.unused,
						self.projectile,
						self.base_vats_hit_chance,
						self.attack_animation,
						self.projectile_count,
						self.embedded_weapon_actor_value,
						self.min_range,
						self.max_range,
						self.on_hit,
						self.flags_,
						self.animation_attack_multiplier,
						self.fire_rate,
						self.override_action_points,
						self.rumble_left_motor_strength,
						self.rumble_right_motor_strength,
						self.rumble_duration,
						self.override_damage_to_weapon_mult,
						self.attack_shots_per_sec,
						self.reload_time,
						self.jam_time,
						self.aim_arc,
						self.skill,
						self.rumble_pattern,
						self.rumble_wavelength,
						self.limb_damage_multiplier,
						self.resistance_type,
						self.sight_usage,
						self.semi_automatic_fire_delay_min,
						self.semi_automatic_fire_delay_max,
						)
			return b"DNAM\xcc\x00" + packed

	@attrs.define
	class CRDT(RecordType):
		"""
		Critical Data.
		"""

		critical_damage: int
		unused: bytes
		ctit_percent_mul: float
		flags: int  # see https://tes5edit.github.io/fopdoc/Fallout3/Records/WEAP.html
		unused_: bytes

		#: Form ID of a :class:`~.SPEL` record, or null.s
		effect: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x10\x00"  # size field
			return cls(*struct.unpack("<H2sfB3s4s", raw_bytes.read(16)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			packed = struct.pack(
					"<H2sfB3s4s",
					self.critical_damage,
					self.unused,
					self.ctit_percent_mul,
					self.flags,
					self.unused_,
					self.effect,
					)
			return b"CRDT\x10\x00" + packed

	@attrs.define
	class VATS(RecordType):
		"""
		VATS (New Vegas only).
		"""

		#: Form ID of a :class:`~.SPEL`, or null.
		effect: bytes
		skill: float
		damage_multiplier: float
		ap: float
		silent: int  # Enum - see https://tes5edit.github.io/fopdoc/FalloutNV/Records/WEAP.html
		mod_required: int  # Enum - see https://tes5edit.github.io/fopdoc/FalloutNV/Records/WEAP.html
		unused: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x14\x00"  # size field
			return cls(*struct.unpack("<4sfffBB2s", raw_bytes.read(20)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			packed = struct.pack(
					"<4sfffBB2s",
					self.effect,
					self.skill,
					self.damage_multiplier,
					self.ap,
					self.silent,
					self.mod_required,
					self.unused,
					)
			return b"VATS\x14\x00" + packed

	class VNAM(Uint32Record):
		"""
		Sound Level.
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
			elif record_type in {
					b"FULL",
					b"ICON",
					b"MICO",
					b"SCRI",
					b"EITM",
					b"EAMT",
					b"NAM0",
					b"REPL",
					b"ETYP",
					b"BIPL",
					b"YNAM",
					b"ZNAM",
					b"EFSD",
					b"NNAM",
					b"INAM",
					b"WNAM",
					b"SNAM",
					b"XNAM",
					b"NAM7",
					b"TNAM",
					b"NAM6",
					b"UNAM",
					b"NAM9",
					b"NAM8",
					b"VNAM",
					b"DATA",
					b"DNAM",
					b"CRDT",
					b"VATS",
					b"MWD1",
					b"MWD2",
					b"MWD3",
					b"MWD4",
					b"MWD5",
					b"MWD6",
					b"MWD7",
					b"VANM",
					b"WNM1",
					b"WNM2",
					b"WNM3",
					b"WNM4",
					b"WNM5",
					b"WNM6",
					b"WNM7",
					b"WMI1",
					b"WMI2",
					b"WMI3",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
