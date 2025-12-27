# stdlib
from io import BytesIO

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from esp_parser.records import ALCH
from esp_parser.subrecords import EDID, OBND, Effect, Model


def test_achr_record(advanced_data_regression: AdvancedDataRegressionFixture):
	alch = ALCH(
			flags=0,
			id=b'\x97F\x03\x01',
			revision=0,
			version=15,
			unknown=b'\x00\x00',
			data=[
					EDID(b'TestSkillBook'),
					OBND(X1=0, Y1=0, Z1=0, X2=0, Y2=0, Z2=0),
					ALCH.FULL(b'A Consumable Book'),
					Model.MODL(b'meshes\\clutter\\books\\bookgeneric01.nif'),
					ALCH.ICON(b'items_skill_books.dds'),
					ALCH.MICO(b'items_skill_books.dds'),
					ALCH.ETYP(12),
					ALCH.DATA(0.0),
					ALCH.ENIT(
							value=20,
							flags=1,
							unused=b'\xcd\xcd\xcd',
							withdrawal_effect=b'\x00\x00\x00\x00',
							addiction_chance=0.0,
							sound_consume=b';\xb7\x07\x00',
							),
					Effect.EFID(b'vF\x03\x01'),
					Effect.EFIT(magnitude=0, area=0, duration=0, type=Effect.EfitTypeEnum.Self, actor_value=-1),
					]
			)

	advanced_data_regression.check(alch.unparse())

	buffer = alch.unparse()
	advanced_data_regression.check(buffer)
	assert alch.parse(BytesIO(buffer)) == alch
