===========
esp-parser
===========

.. start short_desc

**Parser and unparser for Bethesda ESP files.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/esp-parser/latest?logo=read-the-docs
	:target: https://esp-parser.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/potbanksoftware/esp-parser/workflows/Docs%20Check/badge.svg
	:target: https://github.com/potbanksoftware/esp-parser/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/potbanksoftware/esp-parser/workflows/Linux/badge.svg
	:target: https://github.com/potbanksoftware/esp-parser/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/potbanksoftware/esp-parser/workflows/Windows/badge.svg
	:target: https://github.com/potbanksoftware/esp-parser/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/potbanksoftware/esp-parser/workflows/macOS/badge.svg
	:target: https://github.com/potbanksoftware/esp-parser/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/potbanksoftware/esp-parser/workflows/Flake8/badge.svg
	:target: https://github.com/potbanksoftware/esp-parser/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/potbanksoftware/esp-parser/workflows/mypy/badge.svg
	:target: https://github.com/potbanksoftware/esp-parser/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/potbanksoftware/esp-parser/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/potbanksoftware/esp-parser/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/potbanksoftware/esp-parser/master?logo=coveralls
	:target: https://coveralls.io/github/potbanksoftware/esp-parser?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/potbanksoftware/esp-parser?logo=codefactor
	:target: https://www.codefactor.io/repository/github/potbanksoftware/esp-parser
	:alt: CodeFactor Grade

.. |license| image:: https://img.shields.io/github/license/potbanksoftware/esp-parser
	:target: https://github.com/potbanksoftware/esp-parser/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/potbanksoftware/esp-parser
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/potbanksoftware/esp-parser/v0.0.0
	:target: https://github.com/potbanksoftware/esp-parser/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/potbanksoftware/esp-parser
	:target: https://github.com/potbanksoftware/esp-parser/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2026
	:alt: Maintenance

.. end shields

Installation
--------------

.. start installation

``esp-parser`` can be installed from GitHub.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install git+https://github.com/potbanksoftware/esp-parser

.. end installation
