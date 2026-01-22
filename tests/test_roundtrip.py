# stdlib
from io import BytesIO
from typing import cast

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

# this package
import esp_parser


@pytest.mark.parametrize(
		"plugin",
		[
				"BadassBadlandsArmour.esp",
				"EmptyPlugin.esp",
				"EmptyPlugin2.esp",
				],
		)
def test_roundtrip(plugin: str):
	filename = PathPlus("tests/examples") / plugin

	with filename.open("rb") as fp:
		records = esp_parser.parse_esp(cast(BytesIO, fp))
		output = b"".join(record.unparse() for record in records)

	with filename.open("rb") as fp:
		existing = fp.read()

	assert output == existing
