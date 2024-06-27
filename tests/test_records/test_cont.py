# stdlib
from io import BytesIO

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from esp_parser.records import CONT
from esp_parser.subrecords import EDID, OBND, Item, Model


def test_cont_record(advanced_data_regression: AdvancedDataRegressionFixture):
	cont = CONT(
			flags=0,
			id=b'\xc8\xc5\x05\x01',
			revision=0,
			version=15,
			unknown=b'\x00\x00',
			data=[
					EDID(b'TestContainer'),
					OBND(X1=-25, Y1=-41, Z1=0, X2=23, Y2=41, Z2=32),
					CONT.FULL(b'A Container'),
					Model.MODL(b'Clutter\\Chest\\SteamerTrunk01.NIF'),
					Item.CNTO(item=b'\x1c;\x10\x00', item_count=1),  # Star Bottle Cap
					Item.CNTO(item=b'\\\xb0\x0c\x00', item_count=1),  # Doctor's Bag
					Item.CNTO(item=b'iQ\x01\x00', item_count=3),  # Stimpak
					Item.CNTO(item=b'\xa0x\x03\x00', item_count=10),  # Caps75Leveled
					CONT.DATA(flags=0, weight=0.0)
					]
			)
	advanced_data_regression.check(cont.unparse())

	buffer = cont.unparse()
	advanced_data_regression.check(buffer)
	assert cont.parse(BytesIO(buffer)) == cont
