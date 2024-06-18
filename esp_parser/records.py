#!/usr/bin/env python3
#
#  records.py
"""
Models for different record types.
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
from typing import Iterator, NamedTuple, Tuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import CTDA, EDID, OBND, Model, Script
from esp_parser.types import (
		BytesRecordType,
		CStringRecord,
		Float32Record,
		FormIDRecord,
		Record,
		RecordType,
		Uint8Record
		)
from esp_parser.utils import NULL

__all__ = [
		"CELL",
		"DIAL",
		"DialType",
		"INFO",
		"InfoNextSpeaker",
		"QUST",
		"REFR",
		"SCPT",
		"SOUN",
		"TACT",
		"TES4",
		"TRDTEmotionType",
		"WRLD"
		]


@attrs.define
class TES4(Record):
	"""
	Record for Plugin info.
	"""

	class HEDR(NamedTuple):
		"""
		Header.

		Contains additional details about the plugin.
		"""

		version: float  # 0.94 in most files; 1.7 in recent versions of Update.esm.

		#: Number of records and groups (not including TES4 record itself).
		num_records: int

		#: Next available object ID.
		next_object_id: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x0c\x00"  # size field
			return cls(*struct.unpack("<fI4s", raw_bytes.read(12)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"HEDR\x0c\x00" + struct.pack("<fI4s", *self)

	RecordType.register(HEDR)

	class CNAM(CStringRecord):
		"""
		The plugin's author.

		Max 512 bytes.
		"""

	class SNAM(CStringRecord):
		"""
		The plugin's description.

		Max 512 bytes.
		"""

	class MAST(CStringRecord):
		"""
		Name of a master plugin.

		May be repeated.
		"""

	class DATA(BytesRecordType):  # noqa: D106  # TODO

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			return cls(raw_bytes.read(10))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA" + bytes(self)

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

			if record_type in {b"HEDR", b"CNAM", b"SNAM", b"MAST", b"DATA"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


class CELL(Record):
	"""
	Record for a cell.
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

	class XCLC(NamedTuple):
		"""
		Grid reference of the cell.
		"""

		x: int = 0
		y: int = 0
		force_hide_land: int = 0

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x0c\x00"  # size field
			return cls(*struct.unpack("<iiI", raw_bytes.read(12)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"XCLC\x0c\x00" + struct.pack("<iiI", *self)

	RecordType.register(XCLC)

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
			elif record_type in {b"FULL", b"DATA", b"XCLC", b"LTMP", b"LNAM", b"XCLW", b"XNAM"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


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

	def __repr__(self) -> str:
		return str(int(self))


class InfoNextSpeaker(IntEnum):
	"""
	Enum for ``INFO.DATA.next_speaker``.
	"""

	Target = 0
	Self = 1
	Either = 2

	def __repr__(self) -> str:
		return str(int(self))


class TRDTEmotionType(IntEnum):
	"""
	Enum for ``INFO.TRDT.emotion_type``.
	"""

	Neutral = 0
	Anger = 1
	Disgust = 2
	Fear = 3
	Sad = 4
	Happy = 5
	Surprise = 6
	Pained = 7

	def __repr__(self) -> str:
		return str(int(self))


@attrs.define
class DIAL(Record):
	"""
	Dialog topic.
	"""

	class QSTI(FormIDRecord):
		"""
		Form ID of the associated quest (:class:`~.QUST`).
		"""

	# class QSTR(BytesRecordType):
	# 	"""
	# 	Form ID of the associated quest (:class:`~.QUST`).
	# 	"""

	# 	@classmethod
	# 	def parse(cls, raw_bytes: BytesIO):
	# 		raise NotImplementedError
	# 		return cls(raw_bytes.read(4))

	class FULL(CStringRecord):
		"""
		Name of the topic.
		"""

	class PNAM(Float32Record):
		"""
		Priority.
		"""

	class DATA(NamedTuple):  # noqa: D106  # TODO
		#: Dialog type
		type: DialType
		# see https://tes5edit.github.io/fopdoc/Fallout3/Records/DIAL.html
		flags: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			size, type_, flags = struct.unpack("<HBB", raw_bytes.read(4))
			assert size == 2, size
			return cls(DialType(type_), flags)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA" + struct.pack("<HBB", 2, *self)

	RecordType.register(DATA)

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
			elif record_type == b"QSTI":
				yield cls.QSTI.parse(raw_bytes)
			# elif record_type == b"QSTR":
			# 	yield QSTR.parse(raw_bytes)
			elif record_type == b"FULL":
				yield cls.FULL.parse(raw_bytes)
			elif record_type == b"PNAM":
				yield cls.PNAM.parse(raw_bytes)
			elif record_type == b"DATA":
				yield cls.DATA.parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


@attrs.define
class INFO(Record):
	"""
	Dialog Response.
	"""

	@attrs.define
	class DATA(RecordType):  # noqa: D106  # TODO
		#: Dialog type
		type: DialType

		next_speaker: InfoNextSpeaker

		# See https://tes5edit.github.io/fopdoc/Fallout3/Records/INFO.html
		flags: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x04\x00"  # size field
			type_, next_speaker = struct.unpack("<BB", raw_bytes.read(2))
			return cls(DialType(type_), next_speaker, raw_bytes.read(2))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA\x04\x00" + struct.pack("<BB", self.type, self.next_speaker) + self.flags

	class QSTI(FormIDRecord):
		"""
		The associates quest.

		Form ID of a :class:`~.QUST` record.
		"""

	class PNAM(FormIDRecord):
		"""
		Form ID of the previous :class:`~.INFO` record, or null.
		"""

	@attrs.define
	class TRDT(RecordType):
		"""
		Response Data.
		"""

		emotion_type: TRDTEmotionType
		emotion_value: int
		unused: bytes
		response_number: int
		unused_: bytes

		#: Form ID of a :class:`~.SOUN` record, or null.
		sound: bytes

		# https://tes5edit.github.io/fopdoc/Fallout3/Records/INFO.html
		flags: int
		unused__: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x18\x00"  # size field
			emotion_type, emotion_value = struct.unpack(">Ii", raw_bytes.read(8))
			unused = raw_bytes.read(4)
			response_number, *_ = struct.unpack(">B", raw_bytes.read(1))
			unused_ = raw_bytes.read(3)
			sound = raw_bytes.read(4)
			flags, *_ = struct.unpack(">B", raw_bytes.read(1))
			unused__ = raw_bytes.read(3)
			return cls(
					emotion_type=TRDTEmotionType(emotion_type),
					emotion_value=emotion_value,
					unused=unused,
					response_number=response_number,
					unused_=unused_,
					sound=sound,
					flags=flags,
					unused__=unused__,
					)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"".join([
					b"TRDT\x18\x00",
					struct.pack(">Ii", self.emotion_type, self.emotion_value),
					self.unused,
					struct.pack(">B", self.response_number),
					self.unused_,
					self.sound,
					struct.pack(">B", self.flags),
					self.unused__,
					])

	class NAM1(CStringRecord):
		"""
		Response Text.
		"""

	class NAM2(CStringRecord):
		"""
		Script Notes.
		"""

	class NAM3(CStringRecord):
		"""
		Edits.
		"""

	class TCLT(FormIDRecord):
		"""
		Choice.

		Form ID of a :class:`~.DIAL` record.
		"""

	class TCLF(FormIDRecord):
		"""
		Link From Topic.

		Form ID of a :class:`~.DIAL` record.
		"""

	class NEXT(RecordType):
		"""
		Marker between scripts.
		"""

		def __repr__(self) -> str:
			return "NEXT()"

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x00\x00"  # size field
			return cls()

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"NEXT\x00\x00"

	class ANAM(FormIDRecord):
		"""
		Speaker.

		Form ID of a :class:`~.CERA` or :class:`~.NPC_` record.
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

			if record_type in {
					b"DATA",
					b"QSTI",
					b"PNAM",
					b"TRDT",
					b"NAM1",
					b"NAM2",
					b"NAM3",
					b"TCLF",
					b"TCLT",
					b"NEXT",
					b"ANAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)

			elif record_type == b"CTDA":
				yield CTDA.parse(raw_bytes)
			elif record_type in {b"SCHR", b"SCDA", b"SCTX", b"SCRO", b"SLSD", b"SCVR"}:
				yield getattr(Script, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


class QUST(Record):
	"""
	Quest.
	"""

	class SCRI(FormIDRecord):
		"""
		Form ID of a :class:`~.SCPT` record.
		"""

	class FULL(CStringRecord):
		"""
		Quest name.
		"""

	class ICON(CStringRecord):
		"""
		Large Icon Filename.
		"""

	class MICO(CStringRecord):
		"""
		Small Icon FIlename.
		"""

	class DATA(NamedTuple):  # noqa: D106  # TODO
		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/QUST.html
		priority: int
		unused: bytes
		quest_delay: float = 0.0

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<BB2sf", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA\x08\x00" + struct.pack("<BB2sf", *self)

	RecordType.register(DATA)

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
					b"SCRI",
					b"FULL",
					b"ICON",
					b"MICO",
					b"DATA",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


class REFR(Record):
	"""
	Placed Object.
	"""

	class NAME(FormIDRecord):
		"""
		The placed object.

		Form ID of a :class:`~.TREE`, :class:`~.SOUN`, :class:`~.ACTI`, :class:`~.DOOR`,
		:class:`~.STAT`, :class:`~.FURN`, :class:`~.CONT`, :class:`~.ARMO`, :class:`~.AMMO`,
		:class:`~.LVLN`, :class:`~.LVLC`, :class:`~.MISC`, :class:`~.WEAP`, :class:`~.BOOK`,
		:class:`~.KEYM`, :class:`~.ALCH`, :class:`~.LIGH`, :class:`~.GRAS`, :class:`~.ASPC`,
		:class:`~.IDLM`, :class:`~.ARMA`, :class:`~.MSTT`, :class:`~.NOTE`, :class:`~.PWAT`,
		:class:`~.SCOL`, :class:`~.TACT`, :class:`~.TERM` or :class:`~.TXST` record.
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

	RecordType.register(XRDO)
	RecordType.register(DATA)

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
					b"NAME",
					b"XRDO",
					b"DATA",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


class SCPT(Record):
	"""
	Script.
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
			elif record_type in {b"SCHR", b"SCDA", b"SCTX", b"SCRO", b"SLSD", b"SCVR"}:
				yield getattr(Script, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


@attrs.define
class SOUN(Record):
	"""
	Sound.
	"""

	class FNAM(CStringRecord):
		"""
		Sound Filename.
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
		unknown: bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00'

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x24\x00"  # size field (36 bytes)
			unpacked = struct.unpack("<BBbcIhBBhhhhhhi8s", raw_bytes.read(36))

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
					unknown=unpacked[15],
					)

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			packed_body = struct.pack(
					"<BBbcIhBBhhhhhhi8s",
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
					self.unknown,
					)

			assert len(packed_body) == 36
			return b"SNDD\x24\x00" + packed_body

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
			else:
				raise NotImplementedError(record_type)


class TACT(Record):
	"""
	Talking Activator.
	"""

	class FULL(CStringRecord):
		"""
		Name.
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
			elif record_type in {b"FULL"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in {b"MODL", b"MODB"}:
				yield getattr(Model, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


class WRLD(Record):
	"""
	Worldspace.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class XEZN(FormIDRecord):
		"""
		Encounter Zone.

		Form ID of an :class:`~.ECZN` record.
		"""

	class WNAM(FormIDRecord):
		"""
		Parent worldspace.

		Form ID of a :class:`~.WRLD` record.
		"""

	class PNAM(NamedTuple):
		"""
		Parent worldspace flags.
		"""

		flags: int
		unknown: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x02\x00"  # size field
			return cls(*struct.unpack("<Bs", raw_bytes.read(2)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"PNAM\x02\x00" + struct.pack("<B", self.flags) + self.unknown

	RecordType.register(PNAM)

	class CNAM(FormIDRecord):
		"""
		Climate.

		Form ID of a :class:`~.CLMT` record.
		"""

	class NAM2(FormIDRecord):
		"""
		Water.

		Form ID of a :class:`~.WATR` record.
		"""

	class NAM3(FormIDRecord):
		"""
		LOD water type.

		Form ID of a :class:`~.WATR` record.
		"""

	class NAM4(Float32Record):
		"""
		LOD water height.
		"""

	class DNAM(NamedTuple):
		"""
		Land Data.
		"""

		default_land_height: float
		default_water_height: float

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""
			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack(">ff", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"DNAM\x08\x00" + struct.pack(">ff", *self)

	class ONAM(NamedTuple):
		"""
		World Map Offset Data.
		"""

		world_map_scale: float
		cell_x_offset: float
		cell_y_offset: float

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""
			assert raw_bytes.read(2) == b"\x0c\x00"  # size field
			return cls(*struct.unpack(">fff", raw_bytes.read(12)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"ONAM\x0c\x00" + struct.pack(">fff", *self)

	RecordType.register(DNAM)
	RecordType.register(ONAM)

	class INAM(FormIDRecord):
		"""
		Image space.

		Form ID of an :class:`~.IMGS` record.
		"""

	class DATA(Uint8Record):
		"""
		Flags.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/WRLD.html
		"""

	class NAM0(NamedTuple):
		"""
		Min Object Bounds.
		"""

		x: float
		y: float

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""
			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<ff", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"NAM0\x08\x00" + struct.pack("<ff", *self)

	class NAM9(NAM0):
		"""
		Max Object Bounds.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"NAM9\x08\x00" + struct.pack("<ff", *self)

	RecordType.register(NAM0)
	RecordType.register(NAM9)

	class ZNAM(FormIDRecord):
		"""
		Music.

		Form ID of a :class:`~.MUSC` record.
		"""

	class NNAM(CStringRecord):
		"""
		Canopy Shadow.
		"""

	class XNAM(CStringRecord):
		"""
		Water Noise Texture.
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
					b"FULL",
					b"XEZN",
					b"WNAM",
					b"PNAM",
					b"CNAM",
					b"NAM2",
					b"NAM3",
					b"NAM4",
					b"DNAM",
					b"ONAM",
					b"INAM",
					b"ZNAM",
					b"DATA",
					b"NAM0",
					b"NAM9",
					b"NNAM",
					b"XNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
