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

import sys
import unittest
from flexmock import flexmock

from look_at import wmctrl
from look_at.wmctrl import WmCtrl
from look_at.focus import Focus


class WmCtrlListWindowsTest(unittest.TestCase):

    def test_normal_list(self):
        flexmock(wmctrl).should_receive('getoutput').with_args(str).and_return(
                '0x02600003  0 0      -1780 -1150 1680 1050 N/A                     N/A DNDCollectionWindow\n'
                '0x02600004  0 0      0    24   49   1026 N/A                     N/A launcher\n'
                )
        self.assertEquals(2, len(WmCtrl().list_windows()))

    def test_update_notifier_bug(self):
        flexmock(wmctrl).should_receive('getoutput').with_args(str).and_return(
                '0x02600003  0 0      -1780 -1150 1680 1050 N/A                     N/A DNDCollectionWindow\n'
                )
        self.assertEquals(1, len(WmCtrl().list_windows()))

    def test_get_active_window_compiz(self):
        flexmock(wmctrl).should_receive('getoutput').with_args("xprop -root _NET_ACTIVE_WINDOW").and_return(
                '_NET_ACTIVE_WINDOW(WINDOW): window id # 0x3200006\n'
                )
        self.assertEquals('0x3200006', WmCtrl().get_active_window_id())

    def test_get_active_window_xfce4(self):
        flexmock(wmctrl).should_receive('getoutput').with_args("xprop -root _NET_ACTIVE_WINDOW").and_return(
                '_NET_ACTIVE_WINDOW(WINDOW): window id # 0x3200039, 0x0\n'
                )
        self.assertEquals('0x3200039', WmCtrl().get_active_window_id())



class FocusSkipNautilusDesktopTest(unittest.TestCase):
    def test_normal_list(self):
        flexmock(wmctrl).should_receive('getoutput').with_args(str).and_return(
                '0x01a00004  0 2416   0    0    1680 1050 desktop_window.Nautilus  bunca Desktop\n'
                '0x01a04364  0 2416   1730 48   884  516  nautilus.Nautilus     bunca Documents\n'
                )
        self.assertEquals(1, len(Focus(WmCtrl(), dict()).get_candidate_windows('nautilus')))

def runtests():
    suite = unittest.TestLoader().loadTestsFromName(__name__)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    unittest.main()
