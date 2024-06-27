# stdlib
from io import BytesIO

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from esp_parser.records import ALOC
from esp_parser.subrecords import EDID


def test_achr_record(advanced_data_regression: AdvancedDataRegressionFixture):
	aloc = ALOC(
			flags=0,
			id=b'\xb6\xfa\x06\x01',
			revision=0,
			version=15,
			unknown=b'\x00\x00',
			data=[
					EDID(b'TestMLC'),
					ALOC.FULL(b'TestMLC'),
					ALOC.NAM1(b'D\x00\x00\x00'),
					ALOC.NAM2(b'\x00\x00\x00\x00'),
					ALOC.NAM3(b'\x00\x00\x00\x00'),
					ALOC.NAM4(30.0),
					ALOC.NAM5(64),
					ALOC.NAM6(255),
					ALOC.NAM7(10.0),
					ALOC.LNAM(b'\xb1\xfa\x06\x01'),
					ALOC.FNAM(b'\x00\x00\x00\x00')
					]
			)
	advanced_data_regression.check(aloc.unparse())

	buffer = aloc.unparse()
	advanced_data_regression.check(buffer)
	assert aloc.parse(BytesIO(buffer)) == aloc
