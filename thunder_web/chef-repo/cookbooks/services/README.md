Description
===========

lets you preform a variety of actions on many services easily

Requirements
============
None

Attributes
==========
node.services = { }

Usage
=====
```
node.services = { "service_name": [ "enable" ], "another_service": [ "disable", "stop" ], "service_name_2": ["restart"]  }
```

Note setting service_name_2 to "restart" could cause a service to flap each time chef runs

Expected usage might look like this:

```

"services": {
    "acpid":      ["stop", "disable"],
    "atd":        ["stop", "disable"],
    "autofs":     ["stop", "disable"],
    "bluetooth":  ["stop", "disable"],
    "cpuspeed":   ["stop", "disable"],
    "cups":       ["stop", "disable"],
    "firstboot":  ["stop", "disable"],
    "gpm":        ["stop", "disable"],
    "haldaemon":  ["stop", "disable"],
    "hidd":       ["stop", "disable"],
    "mdmonitor":  ["stop", "disable"],
    "pcscd":      ["stop", "disable"],
    "rawdevices": ["stop", "disable"],
    "rpcgssd":    ["stop", "disable"],
    "rpcidmapd" : ["stop", "disable"],
    "smartd":     ["stop", "disable"]
}
```
