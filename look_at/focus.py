# -*- coding: utf-8 -*-
# Copyright (c) 2012, Evgeny V. Generalov <e.generalov@gmail.com>
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

import os
import re


class Focus(object):
    """Window focus switcher."""
    def __init__(self, wmctrl, session):
        self.wmctrl = wmctrl
        self.session = session

    def get_candidate_windows(self, program_name):
        return [w.id for w in self.wmctrl.list_windows()
                      if re.search(program_name, w.wm_class.lower())
                      or re.search(program_name, w.wm_name.lower())
                      ]

    def activate(self, program_name, window_id):
        self.wmctrl.get_window_by_id(window_id).activate()
        self.session[program_name] = window_id

    def execute(self, program_name):
        os.system("%s &" % (program_name,)) # open new window

    def switch(self, program_name):
        candidate_windows = self.get_candidate_windows(program_name)

        if not candidate_windows:
            self.execute(program_name)
        else:
            active_window = self.wmctrl.get_active_window()

            if active_window.id in candidate_windows:
                # we are already showing one of the candidate windows
                # show the *next* candidate in the list (cycling)
                self.activate(program_name,
                        candidate_windows[(candidate_windows.index(active_window.id)+1) % len(candidate_windows)])
            else:
                # if the active window is not along the candidate windows
                # try to display previous focused window with such program_name
                # or just show the first candidate window
                previos_active_window_id = self.session.get(program_name)
                self.activate(program_name,
                        previos_active_window_id if previos_active_window_id in candidate_windows else 
                        candidate_windows[0])
