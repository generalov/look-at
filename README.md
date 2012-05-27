Command line window focus switcher
==================================

Switch to the desktop containing the application, raise the window, and give it focus.


Installation
------------

Install [`wmctrl`][wmctrl] then run:

    $ easy_install look-at

Ubuntu users could try ppa:

    $ sudo apt-add-repository ppa:e15/ppa
    $ sudo apt-get update
    $ sudo apt-get install look-at


Usage
-----

    $ look-at <application>


Use cases
---------

Bind keyboard shortcuts with `~/.xbindkeysrc` to quick access to the desired
application:

    #Launch or switch to terminal
    "look-at gnome-terminal"
        Mod4 + 1

    #Launch or switch to browser
    "look-at firefox"
        Mod4 + 2

    #Lunch or switch to IM client
    "look-at empathy"
        Mod4 + 3

    #Lunch or switch to E-mail
    "look-at thunderbird"
        Mod4 + 4

and reload settings:

    $ killall -HUP xbindkeys


Details
-------

Development of `look-at` happens on Github: http://github.com/generalov/look-at

It uses [`wmctrl`][wmctrl] tool to interact with a EWMH/NetWM compatible X
Window Manager.


[wmctrl]: http://tomas.styblo.name/wmctrl/
