pytest_plugins = ("coincidence", )


def pytest_sessionfinish(session, exitstatus) -> None:  # noqa: MAN001

	# this package
	from esp_parser.types import _cov_instantiated_objects
	print()
	print(sorted(_cov_instantiated_objects))
