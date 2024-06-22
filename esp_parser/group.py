#!/usr/bin/env python3
#
#  group.py
"""
Group (``GRUP``) of records.
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
from typing import List, Type, Union

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser import parse_esp
from esp_parser.types import IntEnum, RecordType

__all__ = ["Group"]


class GroupTypeEnum(IntEnum):
	"""
	Enum for ``Group.group_type``.
	"""

	TopLevel = 0  # Group contains records
	WorldChildren = 1  # Group label is a form ID of a WRLD record and group Contains ROAD and/or CELL records that are children of the given WRLD record.
	InteriorCellBlock = 2  # Group label is a cell block number (int32).
	InteriorCellSubBlock = 3  # Group label is a cell sub-block number (int32).
	ExteriorCellBlock = 4  # Group label is cell block grid (Y, X) coordinates, stored as int8 values.
	ExteriorCellSubBlock = 5  # Group label is cell sub-block grid (Y, X) coordinates, stored as int8 values.
	CellChildren = 6  # Group label is a CELL record form ID. Group contains REFR, ACRE, PGRE, PMIS and ACHR records that are children of the given CELL record.
	TopicChildren = 7  # Group label is a DIAL record form ID. Group contains INFO records that are children of the given DIAL record.
	CellPersistentChildren = 8  # Group label is a CELL record form ID. Group contains REFR, ACRE, PGRE, PMIS or ACHR records that are children of the given CELL record.
	CellTemporaryChildren = 9  # Group label is a CELL record form ID. Group contains REFR, ACRE, PGRE, PMIS or ACHR records that are children of the given CELL record.
	CellVisibleDistantChildren = 10  # Group label is a CELL record form ID. Group contains REFR records that are children of the given CELL record.


@attrs.define
class Group:
	"""
	A group of records.
	"""

	# group_size: int

	label: bytes
	"""
	The type of records within this group, e.g. ``INFO``.

	Depending on ``group_type`` may be an integer.
	"""

	group_type: GroupTypeEnum

	stamp: int  # TODO: datetime
	"""
	A date stamp.

	The first byte is the day of the month, and the second byte is the number of months
	since some unknown point in time
	(perhaps July 2004, when Bethesda began development of Fallout 3).
	"""

	unknown: bytes = b'\x00\x00\x00\x00\x00\x00'
	data: List[Union[RecordType, "Group"]] = attrs.field(factory=list)

	@classmethod
	def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
		"""
		Parse this group.

		:param raw_bytes: Raw bytes for this record
		"""

		unpacked = struct.unpack("<I4sIH6s", raw_bytes.read(20))
		group_size = unpacked[0] - 24
		label = unpacked[1]
		group_type = GroupTypeEnum(unpacked[2])
		stamp, unknown = unpacked[3:]

		data = BytesIO(raw_bytes.read(group_size))

		return cls(label, group_type, stamp, unknown, data=list(parse_esp(data)))

	def unparse(self) -> bytes:
		"""
		Turn this group back into raw bytes for an ESP file.
		"""

		body = b"".join(subrecord.unparse() for subrecord in self.data)
		group_size = len(body) + 24
		packed = struct.pack("<I4sIH6s", group_size, self.label, self.group_type, self.stamp, self.unknown)

		return b"GRUP" + packed + body
