#!/usr/bin/env python3
"""
Copyright (c) 2015-2018 Nitrokey UG

This file is part of libnitrokey.

libnitrokey is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

libnitrokey is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with libnitrokey. If not, see <http://www.gnu.org/licenses/>.

SPDX-License-Identifier: LGPL-3.0

"""

import cffi
import tkinter as tk
import tkinter.simpledialog
from sys import argv
from time import time
from random import SystemRandom as random


ffi = cffi.FFI()


def get_library():
    fp = '/usr/include/libnitrokey/NK_C_API.h'  # path to C API header

    declarations = []
    with open(fp, 'r') as f:
        declarations = f.readlines()

    a = iter(declarations)
    for declaration in a:
        if declaration.strip().startswith('NK_C_API'):
            declaration = declaration.replace('NK_C_API', '').strip()
            while ';' not in declaration:
                declaration += (next(a)).strip()
            # print(declaration)
            ffi.cdef(declaration, override=True)

    p = "/usr/lib/x86_64-linux-gnu/libnitrokey.so"
    C = ffi.dlopen(p)

    return C


def gen_temp_passwd():
    return ''.join([random().choice('0123456789ABCDEF')
                    for x in range(20)])


def get_slot(libnitrokey, name=False):

    slots = []

    for i in range(0, 15):
        entry = (ffi.string(
                            libnitrokey.NK_get_totp_slot_name(i)
                            ).decode('utf-8'))
        if entry:
            slots.append(entry)

        else:
            break

    if name is False:
        print('\n'.join(slots))
        return True

    if name in slots:
        return slots.index(name)

    else:
        return False


def get_otp_libnitrokey(libnitrokey, index):

    if libnitrokey.NK_totp_set_time(int(time())) != 0:
        return False

    print(ffi.string(libnitrokey.NK_get_totp_code(index, 0, 0, 0)
                     ).decode('utf-8'))


def dialog_get_password():

    tk.Tk().withdraw()

    return tkinter.simpledialog.askstring("Pin", "Enter pin:",
                                          show='*').encode('utf-8')


def main():

    libnitrokey = get_library()
    log_level = int(0)
    libnitrokey.NK_set_debug_level(log_level)

    device_connected = libnitrokey.NK_login_auto()

    if not device_connected:
        return False

    if len(argv) < 2:
        get_slot(libnitrokey)
        return True

    name = argv[1]

    pin = dialog_get_password()
    pin_temp = gen_temp_passwd().encode('utf-8')

    pin_correct = libnitrokey.NK_user_authenticate(pin, pin_temp)

    if pin_correct != 0:
        return False

    index = get_slot(libnitrokey, name)
    get_otp_libnitrokey(libnitrokey, index)

    libnitrokey.NK_logout()


if __name__ == '__main__':
    main()
