#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2012 Nik Lutz <nik.lutz@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import signal
import sys
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject

from pulseaudio.PulseAudio import *
from VeromixDbus import *
from VeromixEvent import *
from Pa2dBus import *

if __name__ == '__main__':
    GObject.threads_init()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    mainloop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    conn = dbus.SessionBus()
    name = dbus.service.BusName("org.veromix.pulseaudio.glib", conn)

    dbus.set_default_main_loop(mainloop)

    pulse = PulseAudio()
    bus = VeromixDbus(pulse,conn)
    i = Pa2dBus(bus, pulse)
    event_processor = VeromixEvent(i)
    pulse.set_receiver(event_processor)

    pulse.start_pulsing()
    print ("starting main loop")
    GObject.MainLoop().run()

