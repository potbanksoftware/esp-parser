#!/usr/bin/env python3
#
#  _imad.py
"""
IMAD record type.
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
from typing import Iterator, Tuple

# 3rd party
import attrs

# this package
from esp_parser.subrecords import EDID
from esp_parser.types import FormIDRecord, RawBytesRecord, Record, RecordType, StructRecord

__all__ = ["IMAD"]


class IMAD(Record):
	"""
	Image Space Adapter.
	"""

	@attrs.define
	class DNAM(StructRecord):
		"""
		Data Count.
		"""

		flags: int
		duration: float
		hdr_eye_adapt_speed_mult: int
		hdr_eye_adapt_speed_add: int
		hdr_bloom_blur_radius_mult: int
		hdr_bloom_blur_radius_add: int
		hdr_bloom_threshold_mult: int
		hdr_bloom_threshold_add: int
		hdr_bloom_scale_mult: int
		hdr_bloom_scale_add: int
		hdr_target_lum_min_mult: int
		hdr_target_lum_min_add: int
		hdr_target_lum_max_mult: int
		hdr_target_lum_max_add: int
		hdr_sunlight_scale_mult: int
		hdr_sunlight_scale_add: int
		hdr_sky_scale_mult: int
		hdr_sky_scale_add: int
		unknown: bytes
		cinematic_saturation_mult: int
		cinematic_saturation_add: int
		cinematic_brightness_mult: int
		cinematic_brightness_add: int
		cinematic_contrast_mult: int
		cinematic_contrast_add: int
		unknown_: bytes
		tint_color: int
		blur_radius: int
		double_vision_strength: int
		radial_blur_strength: int
		radial_blur_ramp_up: int
		radial_blur_start: int
		radial_blur_flags: int
		radial_blur_center_x: int
		radial_blur_center_y: int
		depth_of_field_strength: int
		depth_of_field_distance: int
		depth_of_field_range: int
		depth_of_field_flags: int
		radial_blur_ramp_down: int
		radial_blur_down_start: int
		fade_color: int
		motion_blur_strength: int

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<If16I72s6I8s17I", 244

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"flags",
					"duration",
					"hdr_eye_adapt_speed_mult",
					"hdr_eye_adapt_speed_add",
					"hdr_bloom_blur_radius_mult",
					"hdr_bloom_blur_radius_add",
					"hdr_bloom_threshold_mult",
					"hdr_bloom_threshold_add",
					"hdr_bloom_scale_mult",
					"hdr_bloom_scale_add",
					"hdr_target_lum_min_mult",
					"hdr_target_lum_min_add",
					"hdr_target_lum_max_mult",
					"hdr_target_lum_max_add",
					"hdr_sunlight_scale_mult",
					"hdr_sunlight_scale_add",
					"hdr_sky_scale_mult",
					"hdr_sky_scale_add",
					"unknown",
					"cinematic_saturation_mult",
					"cinematic_saturation_add",
					"cinematic_brightness_mult",
					"cinematic_brightness_add",
					"cinematic_contrast_mult",
					"cinematic_contrast_add",
					"unknown_",
					"tint_color",
					"blur_radius",
					"double_vision_strength",
					"radial_blur_strength",
					"radial_blur_ramp_up",
					"radial_blur_start",
					"radial_blur_flags",
					"radial_blur_center_x",
					"radial_blur_center_y",
					"depth_of_field_strength",
					"depth_of_field_distance",
					"depth_of_field_range",
					"depth_of_field_flags",
					"radial_blur_ramp_down",
					"radial_blur_down_start",
					"fade_color",
					"motion_blur_strength",
					)

	class BNAM(RawBytesRecord):
		"""
		Blur Radius.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class VNAM(RawBytesRecord):
		"""
		Double Vision Strength.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class TNAM(RawBytesRecord):
		"""
		Tint Color.

		TODO: An array of Color structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class NAM3(RawBytesRecord):
		"""
		Fade Color.

		TODO: An array of Color structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class RNAM(RawBytesRecord):
		"""
		Radial Blur Strength.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class SNAM(RawBytesRecord):
		"""
		Radial Blur Ramp Up.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class UNAM(RawBytesRecord):
		"""
		Radial Blur Start.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class NAM1(RawBytesRecord):
		"""
		Radial Blur Ramp Down.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class NAM2(RawBytesRecord):
		"""
		Radial Blur Down Start.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class WNAM(RawBytesRecord):
		"""
		DoF Strength.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class XNAM(RawBytesRecord):
		"""
		DoF Distance.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class YNAM(RawBytesRecord):
		"""
		DoF Range.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class NAM4(RawBytesRecord):
		"""
		Motion Blur Strength.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x00IAD(RawBytesRecord):
		"""
		HDR Eye Adapt Speed Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x00IAD" + size + self

	class x40IAD(RawBytesRecord):
		"""
		HDR Eye Adapt Speed Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x40IAD" + size + self

	class x01IAD(RawBytesRecord):
		"""
		HDR Bloom Blur Radius Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x01IAD" + size + self

	class AIAD(RawBytesRecord):
		"""
		HDR Bloom Blur Radius Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x02IAD(RawBytesRecord):
		"""
		HDR Bloom Threshold Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x02IAD" + size + self

	class BIAD(RawBytesRecord):
		"""
		HDR Bloom Threshold Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x03IAD(RawBytesRecord):
		"""
		HDR Bloom Scale Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x03IAD" + size + self

	class CIAD(RawBytesRecord):
		"""
		HDR Bloom Scale Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x04IAD(RawBytesRecord):
		"""
		HDR Target Lum Min Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x04IAD" + size + self

	class DIAD(RawBytesRecord):
		"""
		HDR Target Lum Min Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x05IAD(RawBytesRecord):
		"""
		HDR Target Lum Max Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x05IAD" + size + self

	class EIAD(RawBytesRecord):
		"""
		HDR Target Lum Max Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x06IAD(RawBytesRecord):
		"""
		HDR Sunlight Scale Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x06IAD" + size + self

	class FIAD(RawBytesRecord):
		"""
		HDR Sunlight Scale Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x07IAD(RawBytesRecord):
		"""
		HDR Sky Scale Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x07IAD" + size + self

	class GIAD(RawBytesRecord):
		"""
		HDR Sky Scale Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x08IAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x08IAD" + size + self

	class HIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x09IAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x09IAD" + size + self

	class IIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x0aIAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x0aIAD" + size + self

	class JIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x0bIAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x0bIAD" + size + self

	class KIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x0cIAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x0cIAD" + size + self

	class LIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x0dIAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x0dIAD" + size + self

	class MIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x0eIAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x0eIAD" + size + self

	class NIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x0fIAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x0fIAD" + size + self

	class OIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x10IAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x10IAD" + size + self

	class PIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class x11IAD(RawBytesRecord):
		"""
		Cinematic Saturation Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x11IAD" + size + self

	class QIAD(RawBytesRecord):
		"""
		Cinematic Saturation Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x12IAD(RawBytesRecord):
		"""
		Cinematic Brightness Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x12IAD" + size + self

	class RIAD(RawBytesRecord):
		"""
		Cinematic Brightness Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x13IAD(RawBytesRecord):
		"""
		Cinematic Contrast Mult.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x13IAD" + size + self

	class SIAD(RawBytesRecord):
		"""
		Cinematic Contrast Add.

		TODO: An array of Time structures.
		https://tes5edit.github.io/fopdoc/Fallout3/Records/IMAD.html
		"""

	class x14IAD(RawBytesRecord):
		"""
		Unknown.
		"""

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			size = struct.pack("<H", len(self))
			return b"\x14IAD" + size + self

	class TIAD(RawBytesRecord):
		"""
		Unknown.
		"""

	class RDSD(FormIDRecord):
		"""
		Sound - Intro.

		Form ID of a :class:`~.SOUN` record.
		"""

	class RDSI(FormIDRecord):
		"""
		Sound - Outro.

		Form ID of a :class:`~.SOUN` record.
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
					b"@IAD",
					b"\x00IAD",
					b"\x01IAD",
					b"\x02IAD",
					b"\x03IAD",
					b"\x04IAD",
					b"\x05IAD",
					b"\x06IAD",
					b"\x07IAD",
					b"\x08IAD",
					b"\x09IAD",
					b"\x0AIAD",
					b"\x0BIAD",
					b"\x0CIAD",
					b"\x0DIAD",
					b"\x0EIAD",
					b"\x0FIAD",
					b"\x10IAD",
					b"\x11IAD",
					b"\x12IAD",
					b"\x13IAD",
					b"\x14IAD",
					b"AIAD",
					b"BIAD",
					b"BNAM",
					b"CIAD",
					b"DIAD",
					b"DNAM",
					b"EIAD",
					b"FIAD",
					b"GIAD",
					b"HIAD",
					b"IIAD",
					b"JIAD",
					b"KIAD",
					b"LIAD",
					b"MIAD",
					b"NAM1",
					b"NAM2",
					b"NAM3",
					b"NAM4",
					b"NIAD",
					b"OIAD",
					b"PIAD",
					b"QIAD",
					b"RDSD",
					b"RDSI",
					b"RIAD",
					b"RNAM",
					b"SIAD",
					b"SNAM",
					b"TIAD",
					b"TNAM",
					b"UNAM",
					b"VNAM",
					b"WNAM",
					b"XNAM",
					b"YNAM",
					}:
				if record_type[0] < 65:
					record_type = f"x{record_type[0]:02x}".encode() + record_type[1:]
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
