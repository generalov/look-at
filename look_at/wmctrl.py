# -*- coding: utf-8 -*-
# Copyright (c) 2012, Evgeny V. Generalov <e.generalov@gmail.com>
# Copyright (c) 2012, Antonio Cuni <anto.cuni@gmail.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of  nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Based on wmctrl library
# (https://bitbucket.org/antocuni/wmctrl/raw/7033d6bd56cf/wmctrl.py)
# writen by Antonio Cuni <anto.cuni@gmail.com>

import os
import subprocess


def getoutput(cmdline):
    process = subprocess.Popen(cmdline.split(), stdout=subprocess.PIPE)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        raise subprocess.CalledProcessError(retcode, cmdline, output=output)
    return output


class WmCtrl(object):

    def list_windows(self):
        out = getoutput('wmctrl -l -G -p -x')
        windows = []
        for line in out.splitlines():
            try:
                windows.append(Window.fromstring(line))
            except Exception:
                pass
        return windows

    def get_window_by_id(self, win_id):
        _win_id = int(win_id, 16)
        lst = [win for win in self.list_windows() if int(win.id, 16) == _win_id]
        assert len(lst) <= 1
        return lst[0] if lst else None

    def get_active_window(self):
        return self.get_window_by_id(self.get_active_window_id())

    def get_active_window_id(self):
        out = getoutput("xprop -root _NET_ACTIVE_WINDOW")
        try:
            win_id = out.split('#')[-1].split(',')[0].strip()
        except ValueError:
            return None
        return win_id


class CachedWmCtrl(WmCtrl):

    def list_windows(self):
        if not hasattr(self, '_list_windows_cache'):
            self._list_windows_cache = super(CachedWmCtrl, self).list_windows()
        return self._list_windows_cache


class Window(object):

    def __init__(self, win_id, desktop, pid, x, y, w, h, wm_class, host, wm_name, window_role=None):
        self.id = win_id
        self.desktop = desktop
        self.pid = pid
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.wm_class = wm_class
        self.host = host
        self.wm_name = wm_name
        self.window_role = window_role

    @classmethod
    def fromstring(self, line):
        parts = line.split(None, 9)
        parts = [x.strip() for x in parts]
        parts[1:7] = [int(x) for x in parts[1:7]]
        return Window(*parts)

    @property
    def wm_window_role(self):
        if not self.window_role:
            out = getoutput('xprop -id %s WM_WINDOW_ROLE' % self.id)
            try:
                _, value = out.split(' = ')
            except ValueError:
                # probably xprop returned an error
                return ''
            else:
                self.window_role = value.strip('"')
        return self.window_role

    def activate(self):
        os.system('wmctrl -i -a %s' % self.id)

    def resize_and_move(self, x, y, w, h):
        mvarg = '0,%d,%d,%d,%d' % (x, y, w, h)
        os.system('wmctrl -i -r %s -e %s' % (self.id, mvarg))

    def set_geometry(self, geometry):
        dim, pos = geometry.split('+', 1)
        w, h = map(int, dim.split('x'))
        x, y = map(int, pos.split('+'))
        self.resize_and_move(x, y, w, h)
