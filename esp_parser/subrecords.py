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
from typing import NamedTuple, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.types import BytesRecordType, CStringRecord, FormIDRecord, RecordType
from esp_parser.utils import NULL

__all__ = ["CTDA", "EDID", "Model", "OBND", "Script"]


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


class OBND(NamedTuple):  # noqa: D106  # TODO
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
