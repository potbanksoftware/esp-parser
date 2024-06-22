#!/usr/bin/env python3
#
#  _info.py
"""
INFO record type.
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
from typing import Iterator, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import CTDA, DialType, InfoNextSpeaker, Script
from esp_parser.types import CStringRecord, FormIDRecord, IntEnum, MarkerRecord, Record, RecordType, Uint32Record

__all__ = ["INFO"]


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

	class TPIC(FormIDRecord):
		"""
		Topic.

		FormID of a DIAL record.
		"""

	class PNAM(FormIDRecord):
		"""
		Form ID of the previous :class:`~.INFO` record, or null.
		"""

	class NAME(FormIDRecord):
		"""
		Topic.

		FormID of a DIAL record.
		"""

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

	@attrs.define
	class TRDT(RecordType):
		"""
		Response Data.
		"""

		emotion_type: "INFO.TRDTEmotionType"
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
			return cls(INFO.TRDTEmotionType(unpacked[0]), *unpacked[1:])

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

	# Embedded Script (Begin). collection
	#
	# https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Script.html

	class NEXT(MarkerRecord):
		"""
		Marker between scripts.
		"""

		# def __repr__(self) -> str:
		# 	return "INFO.NEXT()"

		# @classmethod
		# def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		# 	"""
		# 	Parse this subrecord.

		# 	:param raw_bytes: Raw bytes for this record
		# 	"""

		# 	assert raw_bytes.read(2) == b"\x00\x00"  # size field
		# 	return cls()

		# def unparse(self) -> bytes:
		# 	"""
		# 	Turn this subrecord back into raw bytes for an ESP file.
		# 	"""

		# 	return b"NEXT\x00\x00"

	# Embedded Script (End). collection
	#
	# https://tes5edit.github.io/fopdoc/Fallout3/Records/Subrecords/Script.html

	class SNDD(FormIDRecord):
		"""
		Unused.

		FormID of a SOUN record.
		"""

	class RNAM(CStringRecord):
		"""
		Prompt.
		"""

	class ANAM(FormIDRecord):
		"""
		Speaker.

		Form ID of a :class:`~.CERA` or :class:`~.NPC_` record.
		"""

	class KNAM(FormIDRecord):
		"""
		Actor Value / Perk.

		FormID of a AVIF or PERK record.
		"""

	class DNAM(Uint32Record):
		"""
		Speech Challenge.

		Enum - see below for values
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
					b"TPIC",
					b"PNAM",
					b"NAME",
					b"TCLT",
					b"TCLF",
					b"NEXT",
					b"SNDD",
					b"RNAM",
					b"ANAM",
					b"KNAM",
					b"DNAM",
					b"TRDT",
					b"NAM1",
					b"NAM2",
					b"NAM3",
					b"TCFU",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type == b"CTDA":
				yield CTDA.parse(raw_bytes)
			elif record_type in {b"SCHR", b"SCDA", b"SCTX", b"SCRO", b"SLSD", b"SCVR"}:
				yield getattr(Script, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
