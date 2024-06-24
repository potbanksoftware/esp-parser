"""
Create ``__init__.py`` file for the records module.
"""

records = [
		"ACHR",  # Placed NPC
		"ACRE",  # Placed Creature
		"ACTI",  # Activator
		"ADDN",  # Addon Node
		"ALCH",  # Ingestible
		"ALOC",  # Media Relation Controller
		"AMEF",  # Ammo Effect
		"AMMO",  # Ammunition
		"ANIO",  # Animated Object
		"ARMA",  # Armor Addon
		"ARMO",  # Armor
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
		"IMAD",  # Image Space Modifier
		"IMGS",  # Image Space
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
		# "PMIS", # Placed Missile
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
		# "WTHR", # Weather
		]

print(
		'''\
#!/usr/bin/env python3
#
#  records.py
"""
Models for different record types.
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

# this package'''
		)

for record in records:
	if record == "PERK":
		print(f"from ._{record.lower()} import {record}, PerkEffect")
	else:
		print(f"from ._{record.lower()} import {record}")

print("\n__all__ = [")
for record in records:
	print(f'\t\t"{record}",')
	if record == "PERK":
		print('\t\t"PerkEffect",')
print("\t\t]\n")

for record in records:
	print(f'{record}.__module__ == "esp_parser.records"')
	if record == "PERK":
		print('PerkEffect.__module__ == "esp_parser.records"')
