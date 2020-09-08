# PewPew Network Setup

This is a program for [PewPew](https://github.com/pewpew-game) devices using ESP microcontrollers (or possibly others with compatible WiFi support) that allows you to do common network configuration tasks, such as connecting to a known network or finding your IP address, using the device’s own display and buttons, without requiring a REPL connection to a computer.

It requires an extended version of the [menu module](https://github.com/pewpew-game/game-menu). Until the corresponding [pull request](https://github.com/pewpew-game/game-menu/pull/1) is accepted, you can download that from [https://github.com/cwalther/game-menu/tree/menumodule](https://github.com/cwalther/game-menu/tree/menumodule).

Because there is currently no way of entering passwords on the PewPew device, the names and passwords of known networks are instead stored in a file on the device (currently unencrypted). The file is named `networks`, located in the filesystem root next to `networksetup.py`, and is in a simple tab-separated plain text format: One network per line, with name and password separated by a single tab character. Example:

```
My Network	myPassword1
Other Network	otherPassword
```

You need to create this file using a text editor on your computer and transfer it to the device along with the program.

When started, the program presents a menu structure, detailed below. Navigate using the Up and Down buttons. Generally the O button means “select”, the X button means “back”. Selecting may enter a submenu. Some items are informational only and on them both O and X will act as “back”, these are marked with `(i)`. Some commands may result in error messages (not shown), these are `(i)` as well.

```
Sta                                 Commands for the Station interface.
    -active-                        Current state: - = inactive, + = active.
                                      Select to toggle.
    connect                         Connect to one of the networks listed in the
                                      'networks' file.
        My Network                  Select to connect.
        Other Network
    ifconfig                        Show interface configuration (unmodifiable).
        IP:123.45.67.89             IP address                          (i)
        NM:255.255.255.0            Netmask                             (i)
        GW:123.45.67.1              Gateway                             (i)
        NS:8.8.8.8                  Name Server                         (i)
    scan                            Scan for visible networks.
        Network X (-51, WPA2-PSK)   Select will rescan (can only connect to open
                                      networks due to inability to enter
                                      passwords).
        Network Y (-86, open)       Select to connect.
AP                                  Commands for the Access Point interface.
    -active-                        Current state: - = inactive, + = active.
                                      Select to toggle.
        pass:XXX                    Activating displays password        (i)
        name:YYY                      and name (unmodifiable).          (i)
    name:XXX                        When active: network name.          (i)
    ifconfig                        When active: show configuration, see above.
```
