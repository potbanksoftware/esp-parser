#!/usr/bin/env python3
#
#  _refr.py
"""
REFR record type.
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
from typing import Iterator, NamedTuple, Tuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID, PositionRotation
from esp_parser.types import (
		CStringRecord,
		Float32Record,
		FormIDRecord,
		Int32Record,
		MarkerRecord,
		RawBytesRecord,
		Record,
		RecordType,
		StructRecord,
		Uint8Record,
		Uint32Record
		)
from esp_parser.utils import NULL, namedtuple_qualname_repr

__all__ = ["REFR"]


class REFR(Record):
	"""
	Placed Object.
	"""

	# class RCLR(RecordType):
	# 	"""
	# 	Linked Reference Color.
	# 	"""

	# class RCLR(RecordType):
	# 	"""
	# 	??.
	# 	"""

	class NAME(FormIDRecord):
		"""
		The placed object.

		Form ID of a :class:`~.TREE`, :class:`~.SOUN`, :class:`~.ACTI`, :class:`~.DOOR`,
		:class:`~.STAT`, :class:`~.FURN`, :class:`~.CONT`, :class:`~.ARMO`, :class:`~.AMMO`,
		:class:`~.LVLN`, :class:`~.LVLC`, :class:`~.MISC`, :class:`~.WEAP`, :class:`~.BOOK`,
		:class:`~.KEYM`, :class:`~.ALCH`, :class:`~.LIGH`, :class:`~.GRAS`, :class:`~.ASPC`,
		:class:`~.IDLM`, :class:`~.ARMA`, :class:`~.MSTT`, :class:`~.NOTE`, :class:`~.PWAT`,
		:class:`~.SCOL`, :class:`~.TACT`, :class:`~.TERM`, :class:`~.TXST`,	:class:`~.CCRD`,
		:class:`~.IMOD` or :class:`~.CMNY` record.
		"""

	class XEZN(FormIDRecord):
		"""
		Encounter Zone.

		Form ID of an :class:`~.ECZN` record.
		"""

	class XRGD(RawBytesRecord):
		"""
		Ragdoll Data.

		Unknown structure.
		"""

	class XRGB(RawBytesRecord):
		"""
		Ragdoll Biped Data.

		Unknown structure.
		"""

	@attrs.define
	class XPRM(StructRecord):
		"""
		Primitive.
		"""

		x_bound: float
		y_bound: float
		z_bound: float
		red: float
		green: float
		blue: float
		unknown: bytes
		type: int  # Enum - see https://tes5edit.github.io/fopdoc/Fallout3/Records/REFR.html

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<ffffff4sI", 32

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"x_bound",
					"y_bound",
					"z_bound",
					"red",
					"green",
					"blue",
					"unknown",
					"type",
					)

	class XTRI(Uint32Record):
		"""
		Collision Layer.

		Enum - see below for values.
		"""

	# class XMBP(RecordType):
	# 	"""
	# 	MultiBound Primitive Marker.
	# 	"""

	@attrs.define
	class XMBO(StructRecord):
		"""
		Bound Half Extents.
		"""

		x: float
		y: float
		z: float

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<fff", 12

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return ('x', 'y', 'z')

	@attrs.define
	class XTEL(StructRecord):
		"""
		Teleport Destination.
		"""

		#: Form ID of a :class:`~.REFR`` record.
		door: bytes
		xp: float
		yp: float
		zp: float
		xr: float
		yr: float
		zr: float
		flags: int  # See https://tes5edit.github.io/fopdoc/FalloutNV/Records/REFR.html

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<4sffffffI", 32

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return ("door", "xp", "yp", "zp", "xr", "yr", "zr", "flags")

	class XMRK(MarkerRecord):
		"""
		Map Marker Marker.
		"""

	class FNAM(Uint8Record):
		"""
		Map Marker Flags.

		See https://tes5edit.github.io/fopdoc/FalloutNV/Records/REFR.html
		"""

	class FULL(CStringRecord):
		"""
		Map Marker Name.
		"""

	class CNAM(FormIDRecord):
		"""
		Audio location (New Vegas only).

		Form ID of a :class:`~.ALOC` record.
		"""

	class BNAM(RawBytesRecord):
		pass

	class MNAM(Float32Record):
		pass

	class NNAM(Float32Record):
		pass

	@attrs.define
	class TNAM(StructRecord):
		"""
		Map Marker Data.
		"""

		type: int
		unused: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<Bs", 2

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return ("type", "unused")

	class WMI1(FormIDRecord):
		"""
		Map Marker Reputation.

		Form ID of a :class:`~.REPU` record.
		"""

	class MMRK(MarkerRecord):
		"""
		Audio marker (New Vegas only).
		"""

	# class XSRF(RecordType):
	# 	"""
	# 	Unknown.
	# 	"""

	# class XSRD(RecordType):
	# 	"""
	# 	Unknown.
	# 	"""

	class XTRG(FormIDRecord):
		"""
		Target.

		Form ID of a :class:`~.REFR`, :class:`~.ACRE`, :class:`~.ACHR`, :class:`~.PGRE` or :class:`~.PMIS` record.
		"""

	class XLCM(Int32Record):
		"""
		Level Modifier.
		"""

	class XPRD(Float32Record):
		"""
		Patrol data - idle time.
		"""

	# class XPPA(RecordType):
	# 	"""
	# 	Patrol Script Marker.
	#
	# 	Patrol data
	# 	"""

	class INAM(FormIDRecord):
		"""
		Patrol data - Idle.

		Form ID of an :class:`~.IDLE` record, or null.
		"""

	# Embedded Script. collection
	#
	# Patrol data.
	#
	# https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Script.html

	class TNAM(FormIDRecord):
		"""
		Topic.

		Patrol data. Form ID of a :class:`~.DIAL` record, or null.
		"""

	class XRDO(NamedTuple):
		"""
		Radio Data.
		"""

		range_radius: float
		broadcast_range_type: int  # TODO: enum
		static_percentage: float = 0.0
		position_reference: bytes = NULL

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""
			assert raw_bytes.read(2) == b"\x10\x00"  # size field
			return cls(*struct.unpack("<fIf4s", raw_bytes.read(16)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"XRDO\x10\x00" + struct.pack("<fIf4s", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(XRDO)

	class XOWN(FormIDRecord):
		"""
		Owner.

		Ownership data. Form ID of a :class:`~.FACT`, :class:`~.ACHR`,
		:class:`~.CREA` or :class:`~.NPC_` record.
		"""

	class XRNK(Int32Record):
		"""
		Faction Rank.

		Ownership data
		"""

	@attrs.define
	class XLOC(StructRecord):
		"""
		Lock Data.
		"""

		level: int
		unused: bytes
		#: Form ID of a :class:`~.KEYM` record, or null.
		key: bytes
		flags: int  # See https://tes5edit.github.io/fopdoc/FalloutNV/Records/REFR.html
		unknown: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<B3s4sB11s", 20

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return ("level", "unused", "key", "flags", "unknown")

	class XCNT(Int32Record):
		"""
		Count.
		"""

	class XRDS(Float32Record):
		"""
		Radius.
		"""

	class XHLP(Float32Record):
		"""
		Health.
		"""

	class XRAD(Float32Record):
		"""
		Radiation.
		"""

	class XCHG(Float32Record):
		"""
		Charge.
		"""

	class XAMT(FormIDRecord):
		"""
		Ammo Type.

		Form ID of an :class:`~.AMMO` record, or null.
		"""

	class XAMC(Int32Record):
		"""
		Ammo Count.
		"""

	# class XPWR(RecordType):
	# 	"""
	# 	Water Reflection / Refraction.
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XPWR.html
	# 	"""

	class XLTW(FormIDRecord):
		"""
		Lit Water.

		Form ID of a :class:`~.REFR` record.
		"""

	# class XDCR(RecordType):
	# 	"""
	# 	Decal.
	#
	# 	Linked decals
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XDCR.html
	# 	"""

	class XLKR(FormIDRecord):
		"""
		Linked Reference.

		Form ID of a :class:`~.REFR`, :class:`~.ACRE`, :class:`~.ACHR`, :class:`~.PGRE` or :class:`~.PMIS` record.
		"""

	# class XCLP(RecordType):
	# 	"""
	# 	Linked Reference Color.
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XCLP.html
	# 	"""

	class XAPD(Uint8Record):
		"""
		Activate parents flags.

		https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XAPD.html
		"""

	# class XAPR(RecordType):
	# 	"""
	# 	Activate Parent Ref.
	#
	# 	Activate parents
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XAPR.html
	# 	"""

	class XATO(CStringRecord):
		"""
		Activation Prompt.
		"""

	# class XESP(RecordType):
	# 	"""
	# 	Enable Parent.
	#
	# 	https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/XESP.html
	# 	"""

	class XEMI(FormIDRecord):
		"""
		Emittance.

		Form ID of a :class:`~.LIGH` or :class:`~.REGN` record.
		"""

	class XMBR(FormIDRecord):
		"""
		MultiBound Reference.

		Form ID of a :class:`~.REFR` record.
		"""

	class XACT(Uint32Record):
		"""
		Action Flag.

		See below for values.
		"""

	# class ONAM(RecordType):
	# 	"""
	# 	Open By Default.
	# 	"""

	# class XIBS(RecordType):
	# 	"""
	# 	Ignored By Sandbox.
	# 	"""

	@attrs.define
	class XNDP(StructRecord):
		"""
		Navigation Door Link.
		"""

		#: Form ID of a :class:`~.NAVM`` record.
		navmesh: bytes
		unknown: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<4s4s", 8

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return ("navmesh", "unknown")

	# class XPOD(RecordType):
	# 	"""
	# 	Portal Rooms.
	#
	# 	Array of REFR record FormIDs, or null.
	# 	"""

	# class XPLT(RecordType):
	# 	"""
	# 	Portal Data.
	# 	"""

	class XSED(Uint8Record):
		"""
		SpeedTree Seed.
		"""

	# class XRMR(RecordType):
	# 	"""
	# 	Room Data Header.
	# 	"""

	class XLRM(FormIDRecord):
		"""
		Linked Room.

		Form ID of a :class:`~.REFR` record.
		"""

	# class XOCP(RecordType):
	# 	"""
	# 	Occlusion Plane Data.
	# 	"""

	# class XORD(RecordType):
	# 	"""
	# 	Linked Occlusion Planes.
	# 	"""

	# class XLOD(RecordType):
	# 	"""
	# 	Distant LOD Data.
	#
	# 	Unknown
	# 	"""

	class XSCL(Float32Record):
		"""
		Scale.
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
					b"BNAM",
					b"CNAM",
					b"FNAM",
					b"FULL",
					b"INAM",
					b"MMRK",
					b"MNAM",
					b"NAME",
					b"NNAM",
					b"ONAM",
					b"RCLR",
					b"RCLR",
					b"TNAM",
					b"WMI1",
					b"XACT",
					b"XAMC",
					b"XAMT",
					b"XAPD",
					b"XAPR",
					b"XATO",
					b"XCHG",
					b"XCLP",
					b"XCNT",
					b"XDCR",
					b"XEMI",
					b"XESP",
					b"XEZN",
					b"XHLP",
					b"XIBS",
					b"XLCM",
					b"XLKR",
					b"XLOC",
					b"XLOD",
					b"XLRM",
					b"XLTW",
					b"XMBO",
					b"XMBP",
					b"XMBR",
					b"XMRK",
					b"XNDP",
					b"XOCP",
					b"XORD",
					b"XOWN",
					b"XPLT",
					b"XPOD",
					b"XPPA",
					b"XPRD",
					b"XPRM",
					b"XPWR",
					b"XRAD",
					b"XRDO",
					b"XRDS",
					b"XRGB",
					b"XRGD",
					b"XRMR",
					b"XRNK",
					b"XSCL",
					b"XSED",
					b"XSRD",
					b"XSRF",
					b"XTEL",
					b"XTRG",
					b"XTRI",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type == b"DATA":
				yield PositionRotation.DATA.parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
