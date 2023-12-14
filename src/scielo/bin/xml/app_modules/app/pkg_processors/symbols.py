# coding=utf-8

import os

from ...generics import fs_utils
from ...__init__ import TABLES_PATH


SYMBOLS_CSV = TABLES_PATH + '/symbols.csv'
SYMBOLS_HTML = TABLES_PATH + '/symbols.html'
symbols = None


#<td><font face="Symbol" size="+2">&#167;</font></td><td nowrap>&lt;font face=&quot;Symbol&quot;&gt;&amp;#167;&lt;/font&gt;</td><td>club</td><td>&amp;clubs; &nbsp;is&nbsp; <span class="b">&clubs;</span></td><td>&amp;#9827; &nbsp;is&nbsp; <span class="b">&#9827;</span></td><td>Black club suit</td><td>WGL4</td></tr>
#caracter|source html|name|...|...|def|?
# 0 | 4 | 5 
def html2table():
    _items = []
    c = fs_utils.read_file(SYMBOLS_HTML)
    c = c.replace('<tr', '~BREAK~<tr').replace('</tr>', '</tr>~BREAK~')
    items = [item for item in c.split('~BREAK~') if item.startswith('<tr') and item.endswith('</tr>') and 'Symbol' in item]
    for item in items:
        item = item.replace('<td ', '<td>')
        cells = item.split('</td><td>')
        if len(cells) == 7:
            _char = cells[0]
            _ent = cells[4]
            _def = cells[5]
            _char = _char[0:_char.rfind('</font>')]
            _char = _char[_char.rfind('>')+1:]
            _ent = _ent[_ent.rfind('&'):]
            _ent = _ent[0:_ent.rfind(';')+1]
            _items.append(_char + '\t' + _ent + '\t' + _def)
    fs_utils.write_file(SYMBOLS_CSV, '\n'.join(_items))


def load_symbols():
    symbols_items = {}
    for row in fs_utils.read_file_lines(SYMBOLS_CSV):
        cells = row.split('\t')
        if len(cells) == 3:
            char, ent, descr = cells
            symbols_items[char] = ent
    return symbols_items


def get_symbol(c):
    global symbols
    if symbols is None:
        symbols = load_symbols()
    return symbols.get(c, '?')


if not os.path.isfile(SYMBOLS_CSV):
    html2table()
if os.path.isfile(SYMBOLS_CSV):
    if symbols is None:
        symbols = load_symbols()
