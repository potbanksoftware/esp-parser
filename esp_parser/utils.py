#!/usr/bin/env python3
#
#  utils.py
"""
General utilities.
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
from typing import TYPE_CHECKING, List, NamedTuple, Optional, Sequence

if TYPE_CHECKING:
	# this package
	from esp_parser.records import TES4
	from esp_parser.types import RecordType

__all__ = ["create_tes4", "NULL", "TES4_0_94", "namedtuple_qualname_repr"]

NULL: bytes = b'\x00\x00\x00\x00'

#: Helper for 0.94 (as a float) for TES4 headers' version attributes.
TES4_0_94 = 0.9399999976158142


def create_tes4(
		version: float,
		num_records: int,
		next_object_id: bytes,
		author: str = "DEFAULT",
		description: Optional[str] = None,
		masters: Sequence[str] = ("Fallout3.esm", ),
		) -> "TES4":
	"""
	Helper to create a :class:`~.TES4` record.

	:param version: 0.94 in most files; 1.7 in recent versions of ``Update.esm``.
	:param num_records: Number of records and groups (not including the TES4 record itself).
	:param next_object_id: Next available object ID, as a 4-byte sequence.
	:param author: Optional author's name.
	:param masters: List the plugin's master files, listed in the order they were present in when the plugin was created.
	"""

	# this package
	from esp_parser.records import TES4

	data: List["RecordType"] = [
			TES4.HEDR(version, num_records, next_object_id),
			TES4.CNAM(author),
			]

	if description is not None:
		data.append(TES4.SNAM(description))

	for master in masters:
		data.append(TES4.MAST(master))
		data.append(TES4.DATA(b'\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

	return TES4(
			type=b"TES4",
			flags=0,
			id=b'\x00\x00\x00\x00',
			revision=0,
			version=15,
			unknown=b'\x00\x00',
			data=data,
			)


def namedtuple_qualname_repr(namedtuple: NamedTuple) -> str:
	"""
	Produce a ``repr()`` of a :class:`~typing.NamedTuple` showing the ``__qualname__``.

	:param namedtuple:
	"""

	repr_fmt = '(' + ", ".join(f'{name}=%r' for name in namedtuple._fields) + ')'
	return namedtuple.__class__.__qualname__ + repr_fmt % namedtuple
