#!/usr/bin/env python3
#
#  _expl.py
"""
EXPL record type.
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
from io import BytesIO
from typing import Iterator, Tuple

# 3rd party
import attrs

# this package
from esp_parser.subrecords import EDID, OBND, Model
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType, StructRecord

__all__ = ["EXPL"]


class EXPL(Record):
	"""
	Explosion.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class EITM(FormIDRecord):
		"""
		Object Effect.

		Form ID of an :class:`~.ENCH` or :class:`~.SPEL` record.
		"""

	class MNAM(FormIDRecord):
		"""
		Image Space Modifier.

		Form ID of an :class:`~.IMAD` record.
		"""

	@attrs.define
	class DATA(StructRecord):
		"""
		Data.
		"""

		force: float
		damage: float
		radius: float

		#: Form ID of a :class:`~.LIGH` record, or null.
		light: bytes

		#: Form ID of a :class:`~.SOUN` record, or null.
		sound1: bytes
		flags: int  # See https://tes5edit.github.io/fopdoc/Fallout3/Records/EXPL.html
		is_radius: float

		#: Form ID of a :class:`~.IPDS` record, or null.
		impact_dataset: bytes

		#: Form ID of a :class:`~.SOUN` record, or null.
		sound2: bytes
		radiation_level: float
		radiation_dissipation_time: float
		radiation_radius: float
		sound_level: int  # Enum - See https://tes5edit.github.io/fopdoc/Fallout3/Records/EXPL.html

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<fff4s4sIf4s4sfffI", 52

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"force",
					"damage",
					"radius",
					"light",
					"sound1",
					"flags",
					"is_radius",
					"impact_dataset",
					"sound2",
					"radiation_level",
					"radiation_dissipation_time",
					"radiation_radius",
					"sound_level",
					)

	class INAM(FormIDRecord):
		"""
		Placed Impact Object.

		Form ID of a :class:`~.TREE`, :class:`~.SOUN`, :class:`~.ACTI`, :class:`~.DOOR`,
		:class:`~.STAT`, :class:`~.FURN`, :class:`~.CONT`, :class:`~.ARMO`, :class:`~.AMMO`,
		:class:`~.LVLN`, :class:`~.LVLC`, :class:`~.MISC`, :class:`~.WEAP`, :class:`~.BOOK`,
		:class:`~.KEYM`, :class:`~.ALCH`, :class:`~.LIGH`, :class:`~.GRAS`, :class:`~.ASPC`,
		:class:`~.IDLM`, :class:`~.ARMA`, :class:`~.MSTT`, :class:`~.NOTE`, :class:`~.PWAT`,
		:class:`~.SCOL`, :class:`~.TACT`, :class:`~.TERM`, :class:`~.TXST`, :class:`~.CHIP`,
		:class:`~.CMNY`, :class:`~.CCRD` or :class:`~.IMOD` record.
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
			elif record_type in {b"DATA", b"EITM", b"FULL", b"INAM", b"MNAM"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
