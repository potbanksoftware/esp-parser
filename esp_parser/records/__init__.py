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

# this package
from ._achr import ACHR
from ._acre import ACRE
from ._acti import ACTI
from ._alch import ALCH
from ._aloc import ALOC
from ._cell import CELL
from ._chal import CHAL
from ._cont import CONT
from ._crea import CREA
from ._dial import DIAL
from ._door import DOOR
from ._expl import EXPL
from ._fact import FACT
from ._flst import FLST
from ._imad import IMAD
from ._info import INFO
from ._keym import KEYM
from ._ligh import LIGH
from ._mesg import MESG
from ._mgef import MGEF
from ._misc import MISC
from ._mset import MSET
from ._musc import MUSC
from ._navi import NAVI
from ._navm import NAVM
from ._note import NOTE
from ._npc_ import NPC_
from ._pack import PACK
from ._perk import PERK, PerkEffect
from ._qust import QUST
from ._rcct import RCCT
from ._rcpe import RCPE
from ._refr import REFR
from ._repu import REPU
from ._scol import SCOL
from ._scpt import SCPT
from ._soun import SOUN
from ._spel import SPEL
from ._stat import STAT
from ._tact import TACT
from ._tes4 import TES4
from ._txst import TXST
from ._vtyp import VTYP
from ._weap import WEAP
from ._wrld import WRLD

__all__ = [
		"ACHR",
		"ACRE",
		"ACTI",
		"ALCH",
		"ALOC",
		"CELL",
		"CHAL",
		"CONT",
		"CREA",
		"DIAL",
		"DOOR",
		"EXPL",
		"FACT",
		"FLST",
		"IMAD",
		"INFO",
		"KEYM",
		"LIGH",
		"MESG",
		"MGEF",
		"MISC",
		"MSET",
		"MUSC",
		"NAVI",
		"NAVM",
		"NOTE",
		"NPC_",
		"PACK",
		"PERK",
		"PerkEffect",
		"QUST",
		"RCCT",
		"RCPE",
		"REFR",
		"REPU",
		"SCOL",
		"SCPT",
		"SOUN",
		"SPEL",
		"STAT",
		"TACT",
		"TES4",
		"TXST",
		"VTYP",
		"WEAP",
		"WRLD",
		]

ACHR.__module__ == "esp_parser.records"
ACTI.__module__ == "esp_parser.records"
CELL.__module__ == "esp_parser.records"
CONT.__module__ == "esp_parser.records"
CREA.__module__ == "esp_parser.records"
DIAL.__module__ == "esp_parser.records"
DOOR.__module__ == "esp_parser.records"
FACT.__module__ == "esp_parser.records"
INFO.__module__ == "esp_parser.records"
LIGH.__module__ == "esp_parser.records"
MGEF.__module__ == "esp_parser.records"
MISC.__module__ == "esp_parser.records"
NPC_.__module__ == "esp_parser.records"
QUST.__module__ == "esp_parser.records"
REFR.__module__ == "esp_parser.records"
SCOL.__module__ == "esp_parser.records"
SCPT.__module__ == "esp_parser.records"
SOUN.__module__ == "esp_parser.records"
SPEL.__module__ == "esp_parser.records"
STAT.__module__ == "esp_parser.records"
TACT.__module__ == "esp_parser.records"
TES4.__module__ == "esp_parser.records"
TXST.__module__ == "esp_parser.records"
WEAP.__module__ == "esp_parser.records"
WRLD.__module__ == "esp_parser.records"
KEYM.__module__ == "esp_parser.records"
ALCH.__module__ == "esp_parser.records"
NOTE.__module__ == "esp_parser.records"
NAVI.__module__ == "esp_parser.records"
ACRE.__module__ == "esp_parser.records"
NAVM.__module__ == "esp_parser.records"
PACK.__module__ == "esp_parser.records"
EXPL.__module__ == "esp_parser.records"
IMAD.__module__ == "esp_parser.records"
FLST.__module__ == "esp_parser.records"
PERK.__module__ == "esp_parser.records"
PerkEffect.__module__ == "esp_parser.records"
VTYP.__module__ == "esp_parser.records"
MESG.__module__ == "esp_parser.records"
MUSC.__module__ == "esp_parser.records"
REPU.__module__ == "esp_parser.records"
RCPE.__module__ == "esp_parser.records"
RCCT.__module__ == "esp_parser.records"
MSET.__module__ == "esp_parser.records"
ALOC.__module__ == "esp_parser.records"
CHAL.__module__ == "esp_parser.records"
