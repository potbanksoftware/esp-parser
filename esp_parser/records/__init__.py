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
from ._addn import ADDN
from ._alch import ALCH
from ._aloc import ALOC
from ._amef import AMEF
from ._ammo import AMMO
from ._anio import ANIO
from ._arma import ARMA
from ._armo import ARMO
from ._aspc import ASPC
from ._avif import AVIF
from ._book import BOOK
from ._bptd import BPTD
from ._cams import CAMS
from ._ccrd import CCRD
from ._cdck import CDCK
from ._cell import CELL
from ._chal import CHAL
from ._chip import CHIP
from ._clas import CLAS
from ._clmt import CLMT
from ._cmny import CMNY
from ._cobj import COBJ
from ._cont import CONT
from ._cpth import CPTH
from ._crea import CREA
from ._csno import CSNO
from ._csty import CSTY
from ._debr import DEBR
from ._dehy import DEHY
from ._dial import DIAL
from ._dobj import DOBJ
from ._door import DOOR
from ._eczn import ECZN
from ._efsh import EFSH
from ._ench import ENCH
from ._expl import EXPL
from ._eyes import EYES
from ._fact import FACT
from ._flst import FLST
from ._furn import FURN
from ._glob import GLOB
from ._gmst import GMST
from ._gras import GRAS
from ._hair import HAIR
from ._hdpt import HDPT
from ._hung import HUNG
from ._idle import IDLE
from ._idlm import IDLM
from ._imad import IMAD
from ._imgs import IMGS
from ._imod import IMOD
from ._info import INFO
from ._ingr import INGR
from ._ipct import IPCT
from ._ipds import IPDS
from ._keym import KEYM
from ._land import LAND
from ._lgtm import LGTM
from ._ligh import LIGH
from ._lscr import LSCR
from ._lsct import LSCT
from ._ltex import LTEX
from ._lvlc import LVLC
from ._lvli import LVLI
from ._lvln import LVLN
from ._mesg import MESG
from ._mgef import MGEF
from ._micn import MICN
from ._misc import MISC
from ._mset import MSET
from ._mstt import MSTT
from ._musc import MUSC
from ._navi import NAVI
from ._navm import NAVM
from ._note import NOTE
from ._npc_ import NPC_
from ._pack import PACK
from ._perk import PERK, PerkEffect
from ._pgre import PGRE
from ._proj import PROJ
from ._pwat import PWAT
from ._qust import QUST
from ._race import RACE
from ._rads import RADS
from ._rcct import RCCT
from ._rcpe import RCPE
from ._refr import REFR
from ._regn import REGN
from ._repu import REPU
from ._rgdl import RGDL
from ._scol import SCOL
from ._scpt import SCPT
from ._slpd import SLPD
from ._soun import SOUN
from ._spel import SPEL
from ._stat import STAT
from ._tact import TACT
from ._term import TERM
from ._tes4 import TES4
from ._tree import TREE
from ._txst import TXST
from ._vtyp import VTYP
from ._watr import WATR
from ._weap import WEAP
from ._wrld import WRLD

__all__ = [
		"ACHR",
		"ACRE",
		"ACTI",
		"ADDN",
		"ALCH",
		"ALOC",
		"AMEF",
		"AMMO",
		"ANIO",
		"ARMA",
		"ARMO",
		"ASPC",
		"AVIF",
		"BOOK",
		"BPTD",
		"CAMS",
		"CCRD",
		"CDCK",
		"CELL",
		"CHAL",
		"CHIP",
		"CLAS",
		"CLMT",
		"CMNY",
		"COBJ",
		"CONT",
		"CPTH",
		"CREA",
		"CSNO",
		"CSTY",
		"DEBR",
		"DEHY",
		"DIAL",
		"DOBJ",
		"DOOR",
		"ECZN",
		"EFSH",
		"ENCH",
		"EXPL",
		"EYES",
		"FACT",
		"FLST",
		"FURN",
		"GLOB",
		"GMST",
		"GRAS",
		"HAIR",
		"HDPT",
		"HUNG",
		"IDLE",
		"IDLM",
		"IMAD",
		"IMGS",
		"IMOD",
		"INFO",
		"INGR",
		"IPCT",
		"IPDS",
		"KEYM",
		"LAND",
		"LGTM",
		"LIGH",
		"LSCR",
		"LSCT",
		"LTEX",
		"LVLC",
		"LVLI",
		"LVLN",
		"MESG",
		"MGEF",
		"MICN",
		"MISC",
		"MSET",
		"MSTT",
		"MUSC",
		"NAVI",
		"NAVM",
		"NOTE",
		"NPC_",
		"PACK",
		"PERK",
		"PerkEffect",
		"PGRE",
		"PROJ",
		"PWAT",
		"QUST",
		"RACE",
		"RADS",
		"RCCT",
		"RCPE",
		"REFR",
		"REGN",
		"REPU",
		"RGDL",
		"SCOL",
		"SCPT",
		"SLPD",
		"SOUN",
		"SPEL",
		"STAT",
		"TACT",
		"TERM",
		"TES4",
		"TREE",
		"TXST",
		"VTYP",
		"WATR",
		"WEAP",
		"WRLD",
		]

ACHR.__module__ == "esp_parser.records"
ACRE.__module__ == "esp_parser.records"
ACTI.__module__ == "esp_parser.records"
ADDN.__module__ == "esp_parser.records"
ALCH.__module__ == "esp_parser.records"
ALOC.__module__ == "esp_parser.records"
AMEF.__module__ == "esp_parser.records"
AMMO.__module__ == "esp_parser.records"
ANIO.__module__ == "esp_parser.records"
ARMA.__module__ == "esp_parser.records"
ARMO.__module__ == "esp_parser.records"
ASPC.__module__ == "esp_parser.records"
AVIF.__module__ == "esp_parser.records"
BOOK.__module__ == "esp_parser.records"
BPTD.__module__ == "esp_parser.records"
CAMS.__module__ == "esp_parser.records"
CCRD.__module__ == "esp_parser.records"
CDCK.__module__ == "esp_parser.records"
CELL.__module__ == "esp_parser.records"
CHAL.__module__ == "esp_parser.records"
CHIP.__module__ == "esp_parser.records"
CLAS.__module__ == "esp_parser.records"
CLMT.__module__ == "esp_parser.records"
CMNY.__module__ == "esp_parser.records"
COBJ.__module__ == "esp_parser.records"
CONT.__module__ == "esp_parser.records"
CPTH.__module__ == "esp_parser.records"
CREA.__module__ == "esp_parser.records"
CSNO.__module__ == "esp_parser.records"
CSTY.__module__ == "esp_parser.records"
DEBR.__module__ == "esp_parser.records"
DEHY.__module__ == "esp_parser.records"
DIAL.__module__ == "esp_parser.records"
DOBJ.__module__ == "esp_parser.records"
DOOR.__module__ == "esp_parser.records"
ECZN.__module__ == "esp_parser.records"
EFSH.__module__ == "esp_parser.records"
ENCH.__module__ == "esp_parser.records"
EXPL.__module__ == "esp_parser.records"
EYES.__module__ == "esp_parser.records"
FACT.__module__ == "esp_parser.records"
FLST.__module__ == "esp_parser.records"
FURN.__module__ == "esp_parser.records"
GLOB.__module__ == "esp_parser.records"
GMST.__module__ == "esp_parser.records"
GRAS.__module__ == "esp_parser.records"
HAIR.__module__ == "esp_parser.records"
HDPT.__module__ == "esp_parser.records"
HUNG.__module__ == "esp_parser.records"
IDLE.__module__ == "esp_parser.records"
IDLM.__module__ == "esp_parser.records"
IMAD.__module__ == "esp_parser.records"
IMGS.__module__ == "esp_parser.records"
IMOD.__module__ == "esp_parser.records"
INFO.__module__ == "esp_parser.records"
INGR.__module__ == "esp_parser.records"
IPCT.__module__ == "esp_parser.records"
IPDS.__module__ == "esp_parser.records"
KEYM.__module__ == "esp_parser.records"
LAND.__module__ == "esp_parser.records"
LGTM.__module__ == "esp_parser.records"
LIGH.__module__ == "esp_parser.records"
LSCR.__module__ == "esp_parser.records"
LSCT.__module__ == "esp_parser.records"
LTEX.__module__ == "esp_parser.records"
LVLC.__module__ == "esp_parser.records"
LVLI.__module__ == "esp_parser.records"
LVLN.__module__ == "esp_parser.records"
MESG.__module__ == "esp_parser.records"
MGEF.__module__ == "esp_parser.records"
MICN.__module__ == "esp_parser.records"
MISC.__module__ == "esp_parser.records"
MSET.__module__ == "esp_parser.records"
MSTT.__module__ == "esp_parser.records"
MUSC.__module__ == "esp_parser.records"
NAVI.__module__ == "esp_parser.records"
NAVM.__module__ == "esp_parser.records"
NOTE.__module__ == "esp_parser.records"
NPC_.__module__ == "esp_parser.records"
PACK.__module__ == "esp_parser.records"
PERK.__module__ == "esp_parser.records"
PerkEffect.__module__ == "esp_parser.records"
PGRE.__module__ == "esp_parser.records"
PROJ.__module__ == "esp_parser.records"
PWAT.__module__ == "esp_parser.records"
QUST.__module__ == "esp_parser.records"
RACE.__module__ == "esp_parser.records"
RADS.__module__ == "esp_parser.records"
RCCT.__module__ == "esp_parser.records"
RCPE.__module__ == "esp_parser.records"
REFR.__module__ == "esp_parser.records"
REGN.__module__ == "esp_parser.records"
REPU.__module__ == "esp_parser.records"
RGDL.__module__ == "esp_parser.records"
SCOL.__module__ == "esp_parser.records"
SCPT.__module__ == "esp_parser.records"
SLPD.__module__ == "esp_parser.records"
SOUN.__module__ == "esp_parser.records"
SPEL.__module__ == "esp_parser.records"
STAT.__module__ == "esp_parser.records"
TACT.__module__ == "esp_parser.records"
TERM.__module__ == "esp_parser.records"
TES4.__module__ == "esp_parser.records"
TREE.__module__ == "esp_parser.records"
TXST.__module__ == "esp_parser.records"
VTYP.__module__ == "esp_parser.records"
WATR.__module__ == "esp_parser.records"
WEAP.__module__ == "esp_parser.records"
WRLD.__module__ == "esp_parser.records"
