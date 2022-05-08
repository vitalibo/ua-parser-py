# UAParser.py

#### fork of [UAParser.js](https://github.com/faisalman/ua-parser-js)

![status](https://github.com/vitalibo/ua-parser-py/actions/workflows/ci.yaml/badge.svg)

Python library to detect Browser, Engine, OS, CPU, and Device type/model from User-Agent data.

# Documentation

## Constructor

* `UAParser([uastring])`
    * returns new instance

* `UAParser.parse([uastring])`
    * returns result object `{ 'ua': '', 'browser': {}, 'cpu': {}, 'device': {}, 'engine': {}, 'os': {} }`

## Properties

* `browser`
    * returns `{ 'name': '', 'version': '' }`

```sh
# Possible 'browser.name':
2345Explorer, 360 Browser, Amaya, Android Browser, Arora, Avant, Avast, AVG,
BIDUBrowser, Baidu, Basilisk, Blazer, Bolt, Brave, Bowser, Camino, Chimera,
Chrome Headless, Chrome WebView, Chrome, Chromium, Comodo Dragon, Dillo,
Dolphin, Doris, Edge, Electron, Epiphany, Facebook, Falkon, Fennec, Firebird,
Firefox [Reality], Flock, Flow, GSA, GoBrowser, ICE Browser, IE, IEMobile, IceApe, 
IceCat, IceDragon, Iceweasel, Instagram, Iridium, Iron, Jasmine, K-Meleon,
Kindle, Klar, Konqueror, LBBROWSER, Line, Links, Lunascape, Lynx, MIUI Browser,
Maemo Browser, Maemo, Maxthon, MetaSr Midori, Minimo, Mobile Safari, Mosaic,
Mozilla, NetFront, NetSurf, Netfront, Netscape, NokiaBrowser, Obigo, Oculus Browser,
OmniWeb, Opera Coast, Opera [Mini/Mobi/Tablet], PaleMoon, PhantomJS, Phoenix, 
Polaris, Puffin, QQ, QQBrowser, QQBrowserLite, Quark, QupZilla, RockMelt, Safari, 
Sailfish Browser, Samsung Browser, SeaMonkey, Silk, Skyfire, Sleipnir, Slim, 
SlimBrowser, Swiftfox, Tesla, Tizen Browser, UCBrowser, UP.Browser, Vivaldi, 
Waterfox, WeChat, Weibo, Yandex, baidu, iCab, w3m, Whale Browser...

# 'browser.version' determined dynamically
```

* `device`
    * returns `{ 'model': '', 'type': '', 'vendor': '' }`

```sh
# Possible 'device.type':
console, mobile, tablet, smarttv, wearable, embedded

# Possible 'device.vendor':
Acer, Alcatel, Amazon, Apple, Archos, ASUS, AT&T, BenQ, BlackBerry, Dell,
Essential, Fairphone, GeeksPhone, Google, HP, HTC, Huawei, Jolla, Lenovo, LG, 
Meizu, Microsoft, Motorola, Nexian, Nintendo, Nokia, Nvidia, OnePlus, OPPO, Ouya,
Palm, Panasonic, Pebble, Polytron, Realme, RIM, Roku, Samsung, Sharp, Siemens,
Sony[Ericsson], Sprint, Tesla, Vivo, Vodafone, Xbox, Xiaomi, Zebra, ZTE, ...

# 'device.model' determined dynamically
```

* `engine`
    * returns `{ 'name': '', 'version': '' }`

```sh
# Possible 'engine.name'
Amaya, Blink, EdgeHTML, Flow, Gecko, Goanna, iCab, KHTML, Links, Lynx, NetFront,
NetSurf, Presto, Tasman, Trident, w3m, WebKit

# 'engine.version' determined dynamically
```

* `os`
    * returns `{ 'name': '', 'version': '' }`

```sh
# Possible 'os.name'
AIX, Amiga OS, Android[-x86], Arch, Bada, BeOS, BlackBerry, CentOS, Chromium OS,
Contiki, Fedora, Firefox OS, FreeBSD, Debian, Deepin, DragonFly, elementary OS, 
Fuchsia, Gentoo, GhostBSD, GNU, Haiku, HP-UX, Hurd, iOS, Joli, KaiOS, Linpus, Linspire,
Linux, Mac OS, Maemo, Mageia, Mandriva, Manjaro, MeeGo, Minix, Mint, Morph OS, NetBSD,
Nintendo, OpenBSD, OpenVMS, OS/2, Palm, PC-BSD, PCLinuxOS, Plan9, PlayStation, QNX, 
Raspbian, RedHat, RIM Tablet OS, RISC OS, Sabayon, Sailfish, Series40, Slackware, Solaris, 
SUSE, Symbian, Tizen, Ubuntu, Unix, VectorLinux, WebOS, Windows [Phone/Mobile], Zenwalk, ...

# 'os.version' determined dynamically
```

* `cpu`
    * returns `{ 'architecture': '' }`

```sh
# Possible 'cpu.architecture'
68k, amd64, arm[64/hf], avr, ia[32/64], irix[64], mips[64], pa-risc, ppc, sparc[64]
```

* `ua`
    * returns UA string of current instance

# Usage

```python3
import json
from uaparser import UAParser

uastring1 = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.106 Chrome/15.0.874.106 Safari/535.2'
result = UAParser(uastring1)

print(result.browser)  # 'browser': {'name': 'Chromium', 'version': '15.0.874.106', 'major': '15'}
print(result.device)  # {'vendor': None, 'model': None, 'type': None}
print(result.os)  # {'name': 'Ubuntu', 'version': '11.10'}
print(result.os.version)  # '11.10'
print(result.engine.name)  # 'WebKit'
print(result.cpu.architecture)  # 'amd64'

uastring2 = 'Mozilla/5.0 (compatible; Konqueror/4.1; OpenBSD) KHTML/4.1.4 (like Gecko)'
result = UAParser.parse(uastring2)

print(result['browser']['name'])  # 'Konqueror
print(result['os'])  # {'name': 'OpenBSD', 'version': None}
print(result['engine'])  # {'name': 'KHTML', 'version': '4.1.4'}

uastring3 = 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 1.0.0; en-US) AppleWebKit/534.11 (KHTML, like Gecko) Version/7.1.0.7 Safari/534.11'
result = UAParser.parse(uastring3)

print(json.dumps(result, indent=4))
# {
#   "ua": "Mozilla/5.0 (PlayBook; U; RIM Tablet OS 1.0.0; en-US) AppleWebKit/534.11 (KHTML, like Gecko) Version/7.1.0.7 Safari/534.11",
#   "browser": {
#     "name": "Safari",
#     "version": "7.1.0.7",
#     "major": "7" // @deprecated
#   },
#   "cpu": {
#     "architecture": null
#   },
#   "device": {
#     "vendor": "RIM",
#     "model": "PlayBook",
#     "type": "tablet"
#   },
#   "engine": {
#     "name": "WebKit",
#     "version": "534.11"
#   },
#   "os": {
#     "name": "RIM Tablet OS",
#     "version": "1.0.0"
#   }
# }
```
