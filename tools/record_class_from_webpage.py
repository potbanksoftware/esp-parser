"""
Create submodule for the given record(s).
"""

# stdlib
import sys
from typing import List

# 3rd party
import bs4
import httpx
import pandas
from domdf_python_tools.stringlist import StringList

sys.path.append('.')

# this package
from esp_parser.types import (
		CStringRecord,
		Float32Record,
		FormIDRecord,
		Int8Record,
		Int16Record,
		Int32Record,
		MarkerRecord,
		Uint8Record,
		Uint16Record,
		Uint32Record
		)

record = sys.argv[1]
try:
	flavour = sys.argv[2]
except IndexError:
	flavour = "Fallout3"

all_records = [
		"ACHR",  # Placed NPC
		"ACRE",  # Placed Creature
		"ACTI",  # Activator
		"ADDN",  # Addon Node
		"ALCH",  # Ingestible
		"ALOC",  # Media Relation Controller
		"AMEF",  # Ammo Effect
		"AMMO",  # Ammunition
		"ANIO",  # Animated Object
		"ARMO",  # Armor
		"ARMA",  # Armor Addon
		"ASPC",  # Acoustic Space
		"AVIF",  # Actor Value Information
		"BOOK",  # Book
		"BPTD",  # Body Part Data
		"CAMS",  # Camera Shot
		"CCRD",  # Caravan Card
		"CDCK",  # Caravan Deck
		"CELL",  # Cell
		"CHAL",  # Challenge
		"CHIP",  # Casino Chip
		"CLAS",  # Class
		"CLMT",  # Climate
		"CMNY",  # Caravan Money
		"COBJ",  # Constructable Object
		"CONT",  # Container
		"CPTH",  # Camera Path
		"CREA",  # Creature
		"CSNO",  # Casino
		"CSTY",  # Combat Style
		"DEBR",  # Debris
		"DEHY",  # Dehydration Stage
		"DIAL",  # Dialog Topic
		"DOBJ",  # Default Object Manager
		"DOOR",  # Door
		"ECZN",  # Encounter Zone
		"EFSH",  # Effect Shader
		"ENCH",  # Object Effect
		"EXPL",  # Explosion
		"EYES",  # Eyes
		"FACT",  # Faction
		"FLST",  # FormID List
		"FURN",  # Furniture
		"GLOB",  # Global
		"GMST",  # Game Setting
		"GRAS",  # Grass
		"HAIR",  # Hair
		"HDPT",  # Head Part
		"HUNG",  # Hunger Stage
		"IDLE",  # Idle Animation
		"IDLM",  # Idle Marker
		"IMGS",  # Image Space
		"IMAD",  # Image Space Modifier
		"IMOD",  # Item Mod
		"INFO",  # Dialog Response
		"INGR",  # Ingredient
		"IPCT",  # Impact
		"IPDS",  # Impact Data Set
		"KEYM",  # Key
		"LAND",  # Landscape
		"LGTM",  # Lighting Template
		"LIGH",  # Light
		"LSCR",  # Load Screen
		"LSCT",  # Load Screen Type
		"LTEX",  # Landscape Texture
		"LVLC",  # Leveled Creature
		"LVLI",  # Leveled Item
		"LVLN",  # Leveled NPC
		"MESG",  # Message
		"MGEF",  # Base Effect
		"MICN",  # Menu Icon
		"MISC",  # Misc. Item
		"MSET",  # Media Set
		"MSTT",  # Moveable Static
		"MUSC",  # Music Type
		"NAVI",  # Navigation Mesh Info Map
		"NAVM",  # Navigation Mesh
		"NOTE",  # Note
		"NPC_",  # Non-Player Character
		"PACK",  # Package
		"PERK",  # Perk
		"PGRE",  # Placed Grenade
		"PMIS",  # Placed Missile
		"PROJ",  # Projectile
		"PWAT",  # Placeable Water
		"QUST",  # Quest
		"RACE",  # Race
		"RADS",  # Radiation Stage
		"RCCT",  # Recipe Category
		"RCPE",  # Recipe
		"REFR",  # Placed Object
		"REGN",  # Region
		"REPU",  # Reputation
		"RGDL",  # Ragdoll
		"SCOL",  # Static Collection
		"SCPT",  # Script
		"SLPD",  # Sleep Deprivation Stage
		"SOUN",  # Sound
		"SPEL",  # Actor Effect
		"STAT",  # Static
		"TACT",  # Talking Activator
		"TERM",  # Terminal
		"TES4",  # Plugin info
		"TREE",  # Tree
		"TXST",  # Texture Set
		"VTYP",  # Voice Type
		"WATR",  # Water
		"WEAP",  # Weapon
		"WRLD",  # Worldspace
		"WTHR",  # Weather
		]


def process_subrecord_docstring(docstring: List[str]):
	for row in docstring:
		row = row.replace(" FormID", " form ID")
		row = row.replace("FormID", "Form ID")
		for record_type in all_records:
			row = row.replace(record_type, f":class:`~.{record_type}`")
		row = row.replace("(FO3, FNV) ", '')
		yield row


if record == "all":
	records = [
			# "ACHR",  # Placed NPC
			# "ACRE",  # Placed Creature
			# "ACTI",  # Activator
			"ADDN",  # Addon Node
			# "ALCH",  # Ingestible
			# "ALOC",  # Media Relation Controller
			"AMEF",  # Ammo Effect
			"AMMO",  # Ammunition
			"ANIO",  # Animated Object
			"ARMO",  # Armor
			"ARMA",  # Armor Addon
			"ASPC",  # Acoustic Space
			"AVIF",  # Actor Value Information
			"BOOK",  # Book
			"BPTD",  # Body Part Data
			"CAMS",  # Camera Shot
			"CCRD",  # Caravan Card
			"CDCK",  # Caravan Deck
			# "CELL",  # Cell
			# "CHAL",  # Challenge
			"CHIP",  # Casino Chip
			"CLAS",  # Class
			"CLMT",  # Climate
			"CMNY",  # Caravan Money
			"COBJ",  # Constructable Object
			# "CONT",  # Container
			"CPTH",  # Camera Path
			# "CREA",  # Creature
			"CSNO",  # Casino
			"CSTY",  # Combat Style
			"DEBR",  # Debris
			"DEHY",  # Dehydration Stage
			# "DIAL",  # Dialog Topic
			"DOBJ",  # Default Object Manager
			# "DOOR",  # Door
			"ECZN",  # Encounter Zone
			"EFSH",  # Effect Shader
			"ENCH",  # Object Effect
			# "EXPL",  # Explosion
			"EYES",  # Eyes
			# "FACT",  # Faction
			# "FLST",  # FormID List
			"FURN",  # Furniture
			"GLOB",  # Global
			"GMST",  # Game Setting
			"GRAS",  # Grass
			"HAIR",  # Hair
			"HDPT",  # Head Part
			"HUNG",  # Hunger Stage
			"IDLE",  # Idle Animation
			"IDLM",  # Idle Marker
			"IMGS",  # Image Space
			# "IMAD",  # Image Space Modifier
			"IMOD",  # Item Mod
			# "INFO",  # Dialog Response
			"INGR",  # Ingredient
			"IPCT",  # Impact
			"IPDS",  # Impact Data Set
			# "KEYM",  # Key
			"LAND",  # Landscape
			"LGTM",  # Lighting Template
			# "LIGH",  # Light
			"LSCR",  # Load Screen
			"LSCT",  # Load Screen Type
			"LTEX",  # Landscape Texture
			"LVLC",  # Leveled Creature
			"LVLI",  # Leveled Item
			"LVLN",  # Leveled NPC
			# "MESG",  # Message
			# "MGEF",  # Base Effect
			"MICN",  # Menu Icon
			# "MISC",  # Misc. Item
			# "MSET",  # Media Set
			"MSTT",  # Moveable Static
			# "MUSC",  # Music Type
			# "NAVI",  # Navigation Mesh Info Map
			# "NAVM",  # Navigation Mesh
			# "NOTE",  # Note
			# "NPC_",  # Non-Player Character
			# "PACK",  # Package
			# "PERK",  # Perk
			"PGRE",  # Placed Grenade
			# # "PMIS", # Placed Missile
			"PROJ",  # Projectile
			"PWAT",  # Placeable Water
			# "QUST",  # Quest
			"RACE",  # Race
			"RADS",  # Radiation Stage
			# "RCCT",  # Recipe Category
			# "RCPE",  # Recipe
			# "REFR",  # Placed Object
			"REGN",  # Region
			# "REPU",  # Reputation
			"RGDL",  # Ragdoll
			# "SCOL",  # Static Collection
			# "SCPT",  # Script
			"SLPD",  # Sleep Deprivation Stage
			# "SOUN",  # Sound
			# "SPEL",  # Actor Effect
			# "STAT",  # Static
			# "TACT",  # Talking Activator
			"TERM",  # Terminal
			# "TES4",  # Plugin info
			"TREE",  # Tree
			# "TXST",  # Texture Set
			# "VTYP",  # Voice Type
			"WATR",  # Water
			# "WEAP",  # Weapon
			# "WRLD",  # Worldspace
			# # "WTHR",  # Weather
			]
else:
	records = [record]

for record in records:
	filename = f"_{record.lower()}.py"
	response = httpx.get(f"https://tes5edit.github.io/fopdoc/{flavour}/Records/{record}.html")
	response.raise_for_status()

	soup = bs4.BeautifulSoup(response.text, "html5lib")
	main_content = soup.select_one("section.main-content")
	children = list(main_content.children)
	docstring = main_content.select_one('p').text
	table = main_content.select_one("table")
	df = pandas.read_html(str(table), extract_links="body")[0]
	df = df[["Subrecord", "Name", "Type", "Info"]]

	output = StringList()

	header = f'''\
#!/usr/bin/env python3
#
#  {filename}
"""
{record} record type.
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
from io import BytesIO
from typing import Iterator

# this package
from esp_parser.types import Record, RecordType
from esp_parser.subrecords import EDID, OBND, CTDA
'''

	output.append(f"class {record}(Record):")
	output.append('\t"""')
	output.append(f'\t{docstring}.')
	output.append('\t"""')
	output.blankline()

	subrecords = []
	used_types = set()
	for row in df.itertuples():
		subrecord_class, subrecord_url = row.Subrecord

		subrecord_docstring = [row.Name[0] + '.']
		if row.Info[0]:
			subrecord_docstring.extend(('', row.Info[0]))

		if subrecord_url is None:
			subrecord_url = row.Name[1]
		if subrecord_url:
			subrecord_docstring.extend(('', "https://tes5edit.github.io" + subrecord_url))

		record_type = row.Type[0]
		if record_type == "cstring":
			# Null terminated string.
			baseclass = CStringRecord
		elif record_type == "formid":
			# Used to identify a data object. May refer to a data object from a mod or new object created in-game.
			baseclass = FormIDRecord
		elif record_type == "uint32":
			# Value stored as a 32-bit unsigned integer.
			baseclass = Uint32Record
		elif record_type == "int32":
			# Value stored as a 32-bit signed integer.
			baseclass = Int32Record
		elif record_type == "uint16":
			# Value stored as a 16-bit unsigned integer.
			baseclass = Uint16Record
		elif record_type == "int16":
			# Value stored as a 16-bit signed integer.
			baseclass = Int16Record
		elif record_type == "uint8":
			# Value stored as an 8-bit unsigned integer.
			baseclass = Uint8Record
		elif record_type == "int8":
			# Value stored as an 8-bit signed integer.
			baseclass = Int8Record
		elif record_type == "float32":
			# Value stored as a 32-bit floating point number.
			baseclass = Float32Record
		elif record_type == "null":
			# Subrecord with no data.
			baseclass = MarkerRecord
		else:
			baseclass = None

# TODO
# char 	1 	A single 8-bit character
# int64 	8 	Value stored as a 64-bit signed integer.
# uint64 	8 	Value stored as a 64-bit unsigned integer.
# float64 	8 	Value stored as a 64-bit floating point number.
# struct 	variable 	Used for subrecords containing more than one data type. The subrecord structure should be documented on the same page.
# rgba 	4 	The first three bytes are red, green and blue color values respectively. The fourth byte is unused.
# collection 	variable 	Used for collections of subrecords that appear together.
# byte 	1 	Used when the data type of a subrecord or field is unknown, or can be of many different types depending on some factor (which is detailed elsewhere).

		if baseclass is not None:
			used_types.add(baseclass.__name__)

		if subrecord_class == "EDID":
			subrecords.append("EDID")
			continue
		elif subrecord_class == "OBND":
			subrecords.append("OBND")
			continue
		elif subrecord_class == "CTDA":
			subrecords.append("CTDA")
			continue

		subrecord_docstring = list(process_subrecord_docstring(subrecord_docstring))

		if not subrecord_class:
			output.append(f"\t# {subrecord_docstring[0]} {record_type}")
			for row in subrecord_docstring[1:]:
				output.append(f"\t# {row}")
			output.blankline()

		elif baseclass is None:
			output.append(f"\t# class {subrecord_class}(RecordType):")
			output.append('\t# \t"""')
			for row in subrecord_docstring:
				output.append(f'\t# \t{row}')
			output.append('\t# \t"""\n')

			subrecords.append(subrecord_class)
		else:
			output.append(f"\tclass {subrecord_class}({baseclass.__name__}):")
			output.append('\t\t"""')
			for row in subrecord_docstring:
				output.append(f'\t\t{row}')
			output.append('\t\t"""\n')

			subrecords.append(subrecord_class)

	output.append(
			'''\
	@classmethod
	def parse_subrecords(cls, raw_bytes: BytesIO) -> Iterator[RecordType]:
		"""
		Parse this record's subrecords.

		:param raw_bytes: Raw bytes for this record's subrecords
		"""

		while True:
			record_type = raw_bytes.read(4)
			if not record_type:
				break
	'''
			)

	if "EDID" in subrecords:
		output.append("""\
			if record_type == b"EDID":
				yield EDID.parse(raw_bytes)\
	""")
		subrecords.remove("EDID")
		if "OBND" in subrecords:
			output.append("""\
			elif record_type == b"OBND":
				yield OBND.parse(raw_bytes)\
	""")
			subrecords.remove("OBND")
		if "CTDA" in subrecords:
			output.append("""\
			elif record_type == b"CTDA":
				yield CTDA.parse(raw_bytes)\
	""")
			subrecords.remove("CTDA")
		output.append("\t\t\telif record_type in {")

	elif "OBND" in subrecords:
		output.append("""\
			if record_type == b"OBND":
				yield OBND.parse(raw_bytes)\
	""")
		subrecords.remove("OBND")
		if "CTDA" in subrecords:
			output.append("""\
			elif record_type == b"CTDA":
				yield CTDA.parse(raw_bytes)\
	""")
			subrecords.remove("CTDA")

		output.append("\t\t\telif record_type in {")
	else:
		output.append("\t\t\tif record_type in {")
	subrecords = sorted(set(subrecords))
	for subrecord_class in subrecords[:-1]:
		output.append(f'					b"{subrecord_class}",')
	if subrecords:
		output.append(f'					b"{subrecords[-1]}"')
	output.append("\t\t\t\t\t}:")
	output.append("\t\t\t\tyield getattr(cls, record_type.decode()).parse(raw_bytes)")
	output.append("""\
			else:
				raise NotImplementedError(record_type)
""")

	if used_types:
		types_import_line = "from esp_parser.types import " + ", ".join(sorted(used_types))
	else:
		types_import_line = ''

	with open(f"esp_parser/records/{filename}", 'w', encoding="UTF-8") as fp:
		fp.write(header)
		if types_import_line:
			fp.write(types_import_line)
		fp.write("\n\n")
		fp.write(str(output))

	# import subprocess, os
	# subprocess.Popen(["code", f"esp_parser/records/{filename}"], env=os.environ)
