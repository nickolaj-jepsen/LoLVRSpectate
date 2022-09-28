# Author: Nicolas VERDIER
# This file is part of memorpy.
#
# memorpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# memorpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with memorpy.  If not, see <http://www.gnu.org/licenses/>.

import binascii
import logging
import re
import struct

from LoLVRSpectate.memorpy import utils
from LoLVRSpectate.memorpy.Address import Address
from LoLVRSpectate.memorpy.structures import *

from LoLVRSpectate.memorpy import Process

logger = logging.getLogger('memorpy')

class MemWorker(object):

    def __init__(self, process_name, end_offset = None, start_offset = None):
        logger.info(f'opening process {process_name} ...')
        self.process = Process()
        self.process.open_debug_from_name(process_name)
        si = self.process.GetSystemInfo()
        self.end_offset = end_offset or si.lpMaximumApplicationAddress
        self.start_offset = start_offset or si.lpMinimumApplicationAddress

    def Address(self, value, default_type = 'uint'):
        """ wrapper to instanciate an Address class for the memworker.process"""
        return Address(value, process=self.process, default_type=default_type)

    def search_address(self, address):
        address = int(address)
        for m in self.process.list_modules():
            for addr in self.mem_search(address, ftype='ulong', start_offset=m.modBaseAddr, end_offset=m.modBaseSize):
                logger.debug(f'found module {m.szModule} => addr {addr}')

    def umem_replace(self, regex, replace):
        """ like search_replace_mem but works with unicode strings """
        regex = utils.re_to_unicode(regex)
        replace = replace.encode('utf-16-le')
        return self.mem_replace(re.compile(regex, re.UNICODE), replace)

    def mem_replace(self, regex, replace):
        """ search memory for a pattern and replace all found occurrences """
        allWritesSucceed = True
        for start_offset in self.mem_search(regex, ftype='re'):
            if self.process.write_bytes(start_offset, replace) == 1:
                logger.debug(f'Write at offset {start_offset} succeeded !')
            else:
                allWritesSucceed = False
                logger.debug(f'Write at offset {start_offset} failed !')

        return allWritesSucceed

    def umem_search(self, regex):
        """ like mem_search but works with unicode strings """
        regex = utils.re_to_unicode(regex)
        yield from self.mem_search(str(regex), ftype='re')

    def group_search(self, group, start_offset = None, end_offset = None):
        regex = ''
        for value, type in group:
            if type not in ['f', 'float']:
                raise NotImplementedError(f'unknown type {type}')

            f = struct.pack('<f', float(value))
            regex += f'..{f[2:4]}'
        return self.mem_search(regex, ftype='re', start_offset=start_offset, end_offset=end_offset)

    def search_address(self, addr):
        a = '%08X' % addr
        logger.debug(f'searching address {a}')
        regex = ''.join(
            binascii.unhexlify(a[i : i + 2]) for i in range(len(a) - 2, -1, -2)
        )

        return self.mem_search(re.escape(regex), ftype='re')

    def mem_search(self, value, ftype = 'match', protec = PAGE_READWRITE | PAGE_READONLY, start_offset = None, end_offset = None):
        """ 
                iterator returning all indexes where the pattern has been found
        """
        ftype = ftype.lower().strip()
        if type(value) is list:
            ftype = 'group'
        if ftype == 're':
            regex = re.compile(value) if type(value) is str else value
        offset = self.start_offset if start_offset is None else start_offset
        if end_offset is None:
            end_offset = self.end_offset
        if ftype == 'float':
            structtype, structlen = utils.type_unpack(ftype)
        elif ftype not in ['match', 'group', 're']:
            structtype, structlen = utils.type_unpack(ftype)
            value = struct.pack(structtype, value)
        while not offset >= end_offset:
            totalread = 0
            mbi = self.process.VirtualQueryEx(offset)
            offset = mbi.BaseAddress
            chunk = mbi.RegionSize
            protect = mbi.Protect
            state = mbi.State
            if state & MEM_FREE or state & MEM_RESERVE:
                offset += chunk
                continue
            if protec and (
                not protect & protec
                or protect & PAGE_NOCACHE
                or protect & PAGE_WRITECOMBINE
                or protect & PAGE_GUARD
            ):
                offset += chunk
                continue
            b = ''
            try:
                b = self.process.read_bytes(offset, chunk)
                totalread = len(b)
            except Exception as e:
                logger.warning(e)
                offset += chunk
                continue

            if b:
                if ftype == 're':
                    duplicates_cache = set()
                    for res in regex.findall(b):
                        index = b.find(res)
                        while index != -1:
                            soffset = offset + index
                            if soffset not in duplicates_cache:
                                duplicates_cache.add(soffset)
                                yield self.Address(soffset, 'bytes')
                            index = b.find(res, index + len(res))

                elif ftype == 'float':
                    for index in range(len(b)):
                        try:
                            tmpval = struct.unpack(structtype, b[index:index + 4])[0]
                            if int(value) == int(tmpval):
                                soffset = offset + index
                                yield self.Address(soffset, 'float')
                        except Exception as e:
                            pass

                else:
                    index = b.find(value)
                    while index != -1:
                        soffset = offset + index
                        yield self.Address(soffset, 'bytes')
                        index = b.find(value, index + 1)

            offset += totalread

