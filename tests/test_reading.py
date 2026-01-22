# stdlib
from io import BytesIO
from typing import cast

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
import esp_parser
from esp_parser.output import records_as_text, reformat


@pytest.mark.parametrize(
		"plugin",
		[
				"BadassBadlandsArmour.esp",
				"EmptyPlugin.esp",
				"EmptyPlugin2.esp",
				],
		)
def test_read_plugins(plugin: str, advanced_file_regression: AdvancedFileRegressionFixture):
	filename = PathPlus("tests/examples") / plugin

	with filename.open("rb") as fp:
		records = esp_parser.parse_esp(cast(BytesIO, fp))

		output = records_as_text(records)
		output_file = f"{filename.stem}.txt"

	reformatted_output = reformat(output, output_file)
	advanced_file_regression.check(reformatted_output)
