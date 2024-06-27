# stdlib

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from esp_parser.records import TES4
from esp_parser.utils import TES4_0_94, create_tes4


def test_create_tes4(advanced_data_regression: AdvancedDataRegressionFixture):
	tes4 = create_tes4(
			TES4_0_94,
			num_records=45,
			next_object_id=b'l\x15\x00\x00',
			masters=("Fallout3.esm", ),
			description="This is the description.",
			author="domdfcoding",
			)

	assert isinstance(tes4.data[0], TES4.HEDR)
	hedr = tes4.data[0]
	assert hedr.version == TES4_0_94
	assert hedr.num_records == 45
	assert hedr.next_object_id == b'l\x15\x00\x00'

	assert isinstance(tes4.data[1], TES4.CNAM)
	assert tes4.data[1].decode() == "domdfcoding"

	assert isinstance(tes4.data[2], TES4.SNAM)
	assert tes4.data[2].decode() == "This is the description."

	assert isinstance(tes4.data[3], TES4.MAST)
	assert tes4.data[3].decode() == "Fallout3.esm"

	advanced_data_regression.check(tes4.unparse())


def test_create_tes4_no_desc(advanced_data_regression: AdvancedDataRegressionFixture):
	tes4 = create_tes4(TES4_0_94, num_records=45, next_object_id=b'l\x15\x00\x00', masters=("Fallout3.esm", ))

	assert isinstance(tes4.data[0], TES4.HEDR)
	hedr = tes4.data[0]
	assert hedr.version == TES4_0_94
	assert hedr.num_records == 45
	assert hedr.next_object_id == b'l\x15\x00\x00'

	assert isinstance(tes4.data[1], TES4.CNAM)
	assert tes4.data[1].decode() == "DEFAULT"

	assert isinstance(tes4.data[2], TES4.MAST)
	assert tes4.data[2].decode() == "Fallout3.esm"

	advanced_data_regression.check(tes4.unparse())
