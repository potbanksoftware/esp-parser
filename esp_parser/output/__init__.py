#!/usr/bin/env python3
#
#  output.py
"""
Output a representation of an ESP file as text or Python source code.
"""
#
#  Copyright © 2024 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import ast
from typing import TYPE_CHECKING, Iterator, List

# 3rd party
from domdf_python_tools.paths import TemporaryPathPlus, in_directory
from domdf_python_tools.stringlist import StringList
from formate import call_hooks
from formate.config import load_toml, parse_hooks

# this package
from esp_parser import records, subrecords
from esp_parser.output._formate_toml import formate_toml_content
from esp_parser.output._style_yapf import style_yapf_content

if TYPE_CHECKING:
	# this package
	from esp_parser.types import RecordType

__all__ = ["FunctionCallFinder", "records_as_python", "records_as_text", "reformat"]


class FunctionCallFinder(ast.NodeVisitor):
	"""
	AST node visitor to find function calls requiring import statements.
	"""

	def __init__(self):
		self.imports: List[str] = []

	def visit_Call(self, node: ast.Call) -> None:  # noqa: D102

		func = node.func
		if isinstance(func, ast.Attribute):
			func = func.value

		if isinstance(func, ast.Name):
			function_name = func.id
			if function_name in records.__dict__:
				self.imports.append(f"from esp_parser.records import {function_name}")
			elif function_name in subrecords.__dict__:
				self.imports.append(f"from esp_parser.subrecords import {function_name}")
			elif function_name == "Group":
				self.imports.append(f"from esp_parser.group import Group")

			self.generic_visit(node)


def reformat(source: str, output_filename: str) -> str:
	"""
	Reformat the text or Python representation of an ESP file's records.

	:param source:
	:param output_filename: Filename to show in error messages.
	"""

	with TemporaryPathPlus() as tmpdir:
		(tmpdir / "formate.toml").write_text(formate_toml_content)
		(tmpdir / ".style.yapf").write_text(style_yapf_content)

		formate_config = load_toml("formate.toml")

		with in_directory(tmpdir):
			formate_hooks = parse_hooks(formate_config)
			reformatted_source = StringList(call_hooks(formate_hooks, source, output_filename))

	reformatted_source.blankline(ensure_single=True)
	return str(reformatted_source)


def records_as_text(records: Iterator["RecordType"]) -> str:
	"""
	Get a text representation of the records, one top-level record or group per line.

	:param records:
	"""

	return '\n'.join(repr(record) for record in records)


def records_as_python(records: Iterator["RecordType"], plugin_name: str) -> str:
	"""
	Get a Python source code representation of the records, as an unformatted function which returns a list of :class:`~.RecordType` objects.

	:param records:
	:param plugin_name: Determines the function name.
	"""

	output = ',\n'.join(repr(record) for record in records)

	visitor = FunctionCallFinder()
	tree = ast.parse(output)
	visitor.visit(tree)
	imports = sorted(set(visitor.imports))

	output = '\n'.join([*imports, f"def {plugin_name}():", "\treturn [", output, ']'])

	return output
