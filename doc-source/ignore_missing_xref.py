# 3rd party
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.errors import NoUri


def handle_missing_xref(app: Sphinx, env, node: nodes.Node, contnode: nodes.Node) -> None:

	if node.get("reftarget", '') in {
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
			"PMIS",  # Placed Missile, not yet implemented
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
			"WTHR",  # Weather, not yet implemented
			}:
		raise NoUri


def setup(app: Sphinx):
	app.connect("missing-reference", handle_missing_xref, priority=950)
