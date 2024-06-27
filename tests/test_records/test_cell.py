# stdlib
from io import BytesIO

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from esp_parser.records import CELL
from esp_parser.subrecords import EDID

# TODO: XCLR


def test_cell_record(advanced_data_regression: AdvancedDataRegressionFixture):
	cell = CELL(
			flags=0,
			id=b'(:\x00\x00',
			revision=0,
			version=15,
			unknown=b'\x03\x00',
			data=[
					EDID(b'MegatonWomensRestroom'),
					CELL.FULL(b"Women's Restroom"),
					CELL.DATA(1),
					CELL.XCLL(
							ambient_color=b'/FE\x00',
							directional_color=b'\x00\x00\x00\x00',
							fog_color=b'M> \x00',
							fog_near=100.0,
							fog_far=1500.0,
							directional_rotation_xy=0,
							directional_rotation_z=0,
							directional_fade=1.0,
							fog_clip_distance=1500.0,
							fog_power=1.0
							),
					CELL.LTMP(b'\x00\x00\x00\x00'),
					CELL.LNAM(159),
					CELL.XCLW(-2147483648.0),
					CELL.XNAM(b''),
					CELL.XCIM(b'zP\x01\x00'),
					CELL.XEZN(b'\xaaZ\x03\x00'),
					CELL.XCMO(b'\x06\t\t\x00')
					]
			)

	advanced_data_regression.check(cell.unparse())

	buffer = cell.unparse()
	advanced_data_regression.check(buffer)
	assert cell.parse(BytesIO(buffer)) == cell


def test_cell_record_xclc(advanced_data_regression: AdvancedDataRegressionFixture):
	cell = CELL(
			flags=0,
			id=b'\xaf\xad\r\x00',
			revision=0,
			version=15,
			unknown=b'\x02\x00',
			data=[
					EDID(b'GSCemetery'),
					CELL.DATA(2),
					CELL.XCLC(x=-16, y=3, force_hide_land=131072),
					CELL.LTMP(b'\x00\x00\x00\x00'),
					CELL.LNAM(159),
					CELL.XCLW(3.4028234663852886e+38),
					CELL.XNAM(b''),
					CELL.XCLR([b'\xe3<\x12\x00', b'&\xd2\x15\x00']),
					CELL.XCAS(b'b=\x11\x00'),
					CELL.XCMO(b'\xd4\xa6\x08\x00')
					]
			)

	advanced_data_regression.check(cell.unparse())

	buffer = cell.unparse()
	advanced_data_regression.check(buffer)
	assert cell.parse(BytesIO(buffer)) == cell
