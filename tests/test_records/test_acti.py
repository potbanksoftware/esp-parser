# stdlib
from io import BytesIO

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from esp_parser.records import ACTI
from esp_parser.subrecords import EDID, OBND, Model


def test_achr_record(advanced_data_regression: AdvancedDataRegressionFixture):
	acti = ACTI(
			flags=0,
			id=b'\xa4\x98\x02\x01',
			revision=0,
			version=15,
			unknown=b'\x00\x00',
			data=[
					EDID(b'TestBook'),
					OBND(X1=-6, Y1=-9, Z1=-1, X2=6, Y2=9, Z2=1),
					ACTI.FULL(b'A Book'),
					Model.MODL(b'meshes\\clutter\\books\\bookgeneric01.nif'),
					ACTI.SCRI(b'\xa3\x98\x02\x01')
					]
			)

	buffer = acti.unparse()
	advanced_data_regression.check(buffer)
	assert ACTI.parse(BytesIO(buffer)) == acti
