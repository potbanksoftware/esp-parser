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
from io import BytesIO
from typing import Iterator, List, NamedTuple, Tuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import ACBS, AIDT, CTDA, EDID, OBND, Item, Model, PositionRotation, Script
from esp_parser.types import (
		BytesRecordType,
		CStringRecord,
		FaceGenRecord,
		Float32Record,
		FormIDRecord,
		Int16Record,
		Int32Record,
		IntEnumField,
		RawBytesRecord,
		Record,
		RecordType,
		Uint8Record,
		Uint16Record
		)
from esp_parser.utils import NULL, namedtuple_qualname_repr

__all__ = [
		"ACHR",
		"CELL",
		"DIAL",
		"DialType",
		"INFO",
		"InfoNextSpeaker",
		"NPC_",
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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

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


class ACHR(Record):
	"""
	Placed NPC.
	"""

	class NAME(FormIDRecord):
		"""
		The placed NPC.

		Form ID of an :class:`~.NPC_` record.
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

	class XPRD(Float32Record):
		"""
		Idle Time.

		Patrol data.
		"""

	class INAM(FormIDRecord):
		"""
		Idle.

		Patrol data. Form ID of an :class:`~.IDLE` record, or null.
		"""

	class TNAM(FormIDRecord):
		"""
		Topic.

		Patrol data. Form ID of a :class:`~.DIAL` record, or null.
		"""

	class XMRC(FormIDRecord):
		"""
		Merchant Container.

		Form ID of a :class:`~.REFR` record, or null.
		"""

	class XRDS(Float32Record):
		"""
		Radius.
		"""

	class XHLP(Float32Record):
		"""
		Health.
		"""

	class XLKR(FormIDRecord):
		"""
		Linked reference.

		Form ID of a :class:`~.REFR`, :class:`~.ACRE`, :class:`~.ACHR`, :class:`~.PGRE` or :class:`~.PMIS` record.
		"""

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
			elif record_type == b"DATA":
				yield PositionRotation.DATA.parse(raw_bytes)
			elif record_type in {
					b"NAME",
					b"XEZN",
					b"XPRD",
					b"INAM",
					b"TNAM",
					b"XMRC",
					b"XRDS",
					b"XHLP",
					b"XLKR",
					b"XEMI",
					b"XMBR",
					b"XRGD",
					b"XRGB",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in {b"SCHR", b"SCDA", b"SCTX", b"SCRO", b"SLSD", b"SCVR"}:
				yield getattr(Script, record_type.decode()).parse(raw_bytes)
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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

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

	class XCAS(FormIDRecord):
		"""
		Acoustic space.

		Form ID of an :class:`~.ASPC` record.
		"""

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
					b"FULL",
					b"DATA",
					b"XCLC",
					b"LTMP",
					b"LNAM",
					b"XCLW",
					b"XNAM",
					b"XCAS",
					b"XCLR",
					b"XCMO",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


class DialType(IntEnumField):
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


class InfoNextSpeaker(IntEnumField):
	"""
	Enum for ``INFO.DATA.next_speaker``.
	"""

	Target = 0
	Self = 1
	Either = 2


class TRDTEmotionType(IntEnumField):
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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(DATA)

	class INFC(FormIDRecord):
		"""
		Info connection (New Vegas Only).

		Form ID of an :class:`~.INFO` record.
		"""

	class INFX(Int32Record):
		"""
		Info index.
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
					b"QSTI",
					b"FULL",
					b"PNAM",
					b"DATA",
					b"INFC",
					b"INFX",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
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
			unpacked = struct.unpack("<Ii4sB3s4sB3s", raw_bytes.read(24))
			return cls(TRDTEmotionType(unpacked[0]), *unpacked[1:])

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			packed = struct.pack(
					"<Ii4sB3s4sB3s",
					self.emotion_type,
					self.emotion_value,
					self.unused,
					self.response_number,
					self.unused_,
					self.sound,
					self.flags,
					self.unused__,
					)

			return b"TRDT\x18\x00" + packed

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
			return "INFO.NEXT()"

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

	class TCFU(FormIDRecord):
		"""
		Unknown (New Vegas Only).

		Form ID of an :class:`~.INFO` record.
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
					b"TCFU",
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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(DATA)

	class INDX(Int16Record):
		"""
		Stage index.
		"""

	class QSDT(Uint8Record):
		"""
		Stage flags.

		See https://tes5edit.github.io/fopdoc/FalloutNV/Records/QUST.html
		"""

	class CNAM(CStringRecord):
		"""
		Log Entry.
		"""

	class QOBJ(Int32Record):
		"""
		Objective index.
		"""

	class NNAM(CStringRecord):
		"""
		Description.
		"""

	class QSTA(NamedTuple):
		"""
		Quest Target.
		"""

		target: bytes
		"""
		The quest target.

		Form ID of a :class:`~.REFR`, :class:`~.PGRE`,
		:class:`~.PMIS`, :class:`~.ACRE` or :class:`~.ACHR` record.
		"""

		flags: int
		unused: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<4sB3s", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"QSTA\x08\x00" + struct.pack("<4sB3s", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(QSTA)

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
					b"INDX",
					b"QSDT",
					b"CNAM",
					b"QOBJ",
					b"NNAM",
					b"QSTA",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in {b"SCHR", b"SCDA", b"SCTX", b"SCRO", b"SLSD", b"SCVR"}:
				yield getattr(Script, record_type.decode()).parse(raw_bytes)
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
			elif record_type == b"DATA":
				yield PositionRotation.DATA.parse(raw_bytes)
			elif record_type in {
					b"NAME",
					b"XRDO",
					b"XEZN",
					b"XRGD",
					b"XRGB",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)


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
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in {b"MODL", b"MODB"}:
				yield getattr(Model, record_type.decode()).parse(raw_bytes)
			elif record_type in {b"CNTO", b"COED"}:
				yield getattr(Item, record_type.decode()).parse(raw_bytes)
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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class ICON(CStringRecord):
		"""
		Large icon filename.
		"""

	class MICO(CStringRecord):
		"""
		Small icon filename.
		"""

	class MNAM(NamedTuple):
		"""
		Map Data.
		"""

		useable_x_size: int
		useable_y_size: int
		nw_x_coord: int
		nw_y_coord: int
		se_x_coord: int
		se_y_coord: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x10\x00"  # size field
			return cls(*struct.unpack(">iihhhh", raw_bytes.read(16)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"MNAM\x10\x00" + struct.pack(">iihhhh", *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

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

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	class NAM9(NAM0):
		"""
		Max Object Bounds.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""
			return b"NAM9\x08\x00" + struct.pack("<ff", *self)

	RecordType.register(PNAM)
	RecordType.register(MNAM)
	RecordType.register(DNAM)
	RecordType.register(ONAM)
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
					b"ICON",
					b"MICO",
					b"MNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
