# stdlib
from io import BytesIO

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from esp_parser.records import CHAL
from esp_parser.subrecords import EDID


def test_chal_record(advanced_data_regression: AdvancedDataRegressionFixture):
	chal = CHAL(
			flags=0,
			id=b'\xd0\xce\x05\x01',
			revision=0,
			version=15,
			unknown=b'\x00\x00',
			data=[
					EDID(b'TestChallenge'),
					CHAL.FULL(b'A Challenge'),
					CHAL.DESC(b'Collect Something.'),
					CHAL.DATA(
							CHAL.DataTypeEnum.AcquireItemFromList,
							threshold=50,
							flags=CHAL.DATA.FLAG_SHOW_ZERO_PROGRESS,
							interval=1,
							value1=b'\x00\x00',
							value2=b'\x00\x00',
							value3=b'\x00\x00\x00\x00',
							),
					CHAL.SNAM(b'\xae\xd1\x05\x01'),
					],
			)
	advanced_data_regression.check(chal.unparse())

	buffer = chal.unparse()
	advanced_data_regression.check(buffer)
	assert chal.parse(BytesIO(buffer)) == chal
