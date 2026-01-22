# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from esp_parser.__main__ import dump_to_modules


def test_dump_to_modules(tmp_pathplus: PathPlus, advanced_data_regression: AdvancedDataRegressionFixture):
	dump_to_modules(PathPlus("tests/examples/BadassBadlandsArmour.esp"), output_file=tmp_pathplus / "dumped")
	advanced_data_regression.check(
			sorted(p.relative_to(tmp_pathplus).as_posix() for p in tmp_pathplus.iterchildren()),
			)
