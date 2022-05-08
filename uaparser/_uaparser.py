import re

EMPTY = ''
UNKNOWN = '?'
MAJOR = 'major'
MODEL = 'model'
NAME = 'name'
TYPE = 'type'
VENDOR = 'vendor'
VERSION = 'version'
ARCHITECTURE = 'architecture'
CONSOLE = 'console'
MOBILE = 'mobile'
TABLET = 'tablet'
SMARTTV = 'smarttv'
WEARABLE = 'wearable'
EMBEDDED = 'embedded'
UA_MAX_LENGTH = 255

AMAZON = 'Amazon'
APPLE = 'Apple'
ASUS = 'ASUS'
BLACKBERRY = 'BlackBerry'
BROWSER = 'Browser'
CHROME = 'Chrome'
EDGE = 'Edge'
FIREFOX = 'Firefox'
GOOGLE = 'Google'
HUAWEI = 'Huawei'
LG = 'LG'
MICROSOFT = 'Microsoft'
MOTOROLA = 'Motorola'
OPERA = 'Opera'
SAMSUNG = 'Samsung'
SONY = 'Sony'
XIAOMI = 'Xiaomi'
ZEBRA = 'Zebra'
FACEBOOK = 'Facebook'

OLD_SAFARI_MAP = {
    '1.0': '/8',
    '1.2': '/1',
    '1.3': '/3',
    '2.0': '/412',
    '2.0.2': '/416',
    '2.0.3': '/417',
    '2.0.4': '/419',
    '?': '/'
}
WINDOWS_VERSION_MAP = {
    'ME': '4.90',
    'NT 3.11': 'NT3.51',
    'NT 4.0': 'NT4.0',
    '2000': 'NT 5.0',
    'XP': ['NT 5.1', 'NT 5.2'],
    'Vista': 'NT 6.0',
    '7': 'NT 6.1',
    '8': 'NT 6.2',
    '8.1': 'NT 6.3',
    '10': ['NT 6.4', 'NT 10.0'],
    'RT': 'ARM'
}


def has(str1, str2):
    if isinstance(str1, str):
        return lowerize(str1) in lowerize(str2)
    return False


def lowerize(string):
    return string.lower()


def majorize(version):
    if version is not None:
        return re.sub(r'[^\d\.]', EMPTY, version).split('.')[0]
    return None


def trim(string):
    return re.sub(r'\s\s*$', EMPTY, re.sub(r'^\s\s*', EMPTY, string))


def str_mapper(string, mapping):
    for key, value in mapping.items():
        # check if current value is array
        if isinstance(value, list):
            for item in value:
                if has(item, string):
                    return None if key == UNKNOWN else key
        elif has(value, string):
            return None if key == UNKNOWN else key
    return string


REGEXES = {
    'browser': [[
        r'\b(?:crmo|crios)\/([\w\.]+)'  # Chrome for Android/iOS
    ], [VERSION, [NAME, 'Chrome']], [
        r'edg(?:e|ios|a)?\/([\w\.]+)'  # Microsoft Edge
    ], [VERSION, [NAME, 'Edge']], [

        # Presto based
        r'(opera mini)\/([-\w\.]+)',  # Opera Mini
        r'(opera [mobiletab]{3,6})\b.+version\/([-\w\.]+)',  # Opera Mobi/Tablet
        r'(opera)(?:.+version\/|[\/ ]+)([\w\.]+)'  # Opera
    ], [NAME, VERSION], [
        r'opios[\/ ]+([\w\.]+)'  # Opera mini on iphone >= 8.0
    ], [VERSION, [NAME, OPERA + ' Mini']], [
        r'\bopr\/([\w\.]+)'  # Opera Webkit
    ], [VERSION, [NAME, OPERA]], [

        # Mixed
        r'(kindle)\/([\w\.]+)',  # Kindle
        r'(lunascape|maxthon|netfront|jasmine|blazer)[\/ ]?([\w\.]*)',  # Lunascape/Maxthon/Netfront/Jasmine/Blazer

        # Trident based
        r'(avant |iemobile|slim)(?:browser)?[\/ ]?([\w\.]*)',  # Avant/IEMobile/SlimBrowser
        r'(ba?idubrowser)[\/ ]?([\w\.]+)',  # Baidu Browser
        r'(?:ms|\()(ie) ([\w\.]+)',  # Internet Explorer

        # Webkit/KHTML based
        r'(flock|rockmelt|midori|epiphany|silk|skyfire|ovibrowser|bolt|iron|vivaldi|iridium|phantomjs|bowser|quark|qupzilla|falkon|rekonq|puffin|brave|whale|qqbrowserlite|qq)\/([-\w\.]+)',  # Rekonq/Puffin/Brave/Whale/QQBrowserLite/QQ, aka ShouQ
        r'(weibo)__([\d\.]+)'  # Weibo
    ], [NAME, VERSION], [
        r'(?:\buc? ?browser|(?:juc.+)ucweb)[\/ ]?([\w\.]+)'  # UCBrowser
    ], [VERSION, [NAME, 'UC' + BROWSER]], [
        r'\bqbcore\/([\w\.]+)'  # WeChat Desktop for Windows Built-in Browser
    ], [VERSION, [NAME, 'WeChat(Win) Desktop']], [
        r'micromessenger\/([\w\.]+)'  # WeChat
    ], [VERSION, [NAME, 'WeChat']], [
        r'konqueror\/([\w\.]+)'  # Konqueror
    ], [VERSION, [NAME, 'Konqueror']], [
        r'trident.+rv[: ]([\w\.]{1,9})\b.+like gecko'  # IE11
    ], [VERSION, [NAME, 'IE']], [
        r'yabrowser\/([\w\.]+)'  # Yandex
    ], [VERSION, [NAME, 'Yandex']], [
        r'(avast|avg)\/([\w\.]+)'  # Avast/AVG Secure Browser
    ], [[NAME, r'(.+)', '$1 Secure ' + BROWSER], VERSION], [
        r'\bfocus\/([\w\.]+)'  # Firefox Focus
    ], [VERSION, [NAME, FIREFOX + ' Focus']], [
        r'\bopt\/([\w\.]+)'  # Opera Touch
    ], [VERSION, [NAME, OPERA + ' Touch']], [
        r'coc_coc\w+\/([\w\.]+)'  # Coc Coc Browser
    ], [VERSION, [NAME, 'Coc Coc']], [
        r'dolfin\/([\w\.]+)'  # Dolphin
    ], [VERSION, [NAME, 'Dolphin']], [
        r'coast\/([\w\.]+)'  # Opera Coast
    ], [VERSION, [NAME, OPERA + ' Coast']], [
        r'miuibrowser\/([\w\.]+)'  # MIUI Browser
    ], [VERSION, [NAME, 'MIUI ' + BROWSER]], [
        r'fxios\/([-\w\.]+)'  # Firefox for iOS
    ], [VERSION, [NAME, FIREFOX]], [
        r'\bqihu|(qi?ho?o?|360)browser'  # 360
    ], [[NAME, '360 ' + BROWSER]], [
        r'(oculus|samsung|sailfish)browser\/([\w\.]+)'  # Oculus/Samsung/Sailfish Browser
    ], [[NAME, r'(.+)', '$1 ' + BROWSER], VERSION], [
        r'(comodo_dragon)\/([\w\.]+)'  # Comodo Dragon
    ], [[NAME, r'_', ' '], VERSION], [
        r'(electron)\/([\w\.]+) safari',  # Electron-based App
        r'(tesla)(?: qtcarbrowser|\/(20\d\d\.[-\w\.]+))',  # Tesla
        r'm?(qqbrowser|baiduboxapp|2345Explorer)[\/ ]?([\w\.]+)'  # QQBrowser/Baidu App/2345 Browser
    ], [NAME, VERSION], [
        r'(metasr)[\/ ]?([\w\.]+)',  # SouGouBrowser
        r'(lbbrowser)'  # LieBao Browser
    ], [NAME], [

        # WebView
        r'((?:fban\/fbios|fb_iab\/fb4a)(?!.+fbav)|;fbav\/([\w\.]+);)'  # Facebook App for iOS & Android
    ], [[NAME, FACEBOOK], VERSION], [
        r'safari (line)\/([\w\.]+)',  # Line App for iOS
        r'\b(line)\/([\w\.]+)\/iab',  # Line App for Android
        r'(chromium|instagram)[\/ ]([-\w\.]+)'  # Chromium/Instagram
    ], [NAME, VERSION], [
        r'\bgsa\/([\w\.]+) .*safari\/'  # Google Search Appliance on iOS
    ], [VERSION, [NAME, 'GSA']], [
        r'headlesschrome(?:\/([\w\.]+)| )'  # Chrome Headless
    ], [VERSION, [NAME, CHROME + ' Headless']], [
        r' wv\).+(chrome)\/([\w\.]+)'  # Chrome WebView
    ], [[NAME, CHROME + ' WebView'], VERSION], [
        r'droid.+ version\/([\w\.]+)\b.+(?:mobile safari|safari)'  # Android Browser
    ], [VERSION, [NAME, 'Android ' + BROWSER]], [
        r'(chrome|omniweb|arora|[tizenoka]{5} ?browser)\/v?([\w\.]+)'  # Chrome/OmniWeb/Arora/Tizen/Nokia
    ], [NAME, VERSION], [
        r'version\/([\w\.]+) .*mobile\/\w+ (safari)'  # Mobile Safari
    ], [VERSION, [NAME, 'Mobile Safari']], [
        r'version\/([\w\.]+) .*(mobile ?safari|safari)'  # Safari & Safari Mobile
    ], [VERSION, NAME], [
        r'webkit.+?(mobile ?safari|safari)(\/[\w\.]+)'  # Safari < 3.0
    ], [NAME, [VERSION, str_mapper, OLD_SAFARI_MAP]], [
        r'(webkit|khtml)\/([\w\.]+)'
    ], [NAME, VERSION], [

        # Gecko based
        r'(navigator|netscape\d?)\/([-\w\.]+)'  # Netscape
    ], [[NAME, 'Netscape'], VERSION], [
        r'mobile vr; rv:([\w\.]+)\).+firefox'  # Firefox Reality
    ], [VERSION, [NAME, FIREFOX + ' Reality']], [
        r'ekiohf.+(flow)\/([\w\.]+)',  # Flow
        r'(swiftfox)',  # Swiftfox
        r'(icedragon|iceweasel|camino|chimera|fennec|maemo browser|minimo|conkeror|klar)[\/ ]?([\w\.\+]+)',  # IceDragon/Iceweasel/Camino/Chimera/Fennec/Maemo/Minimo/Conkeror/Klar
        r'(seamonkey|k-meleon|icecat|iceape|firebird|phoenix|palemoon|basilisk|waterfox)\/([-\w\.]+)$',  # Firefox/SeaMonkey/K-Meleon/IceCat/IceApe/Firebird/Phoenix
        r'(firefox)\/([\w\.]+)',  # Other Firefox-based
        r'(mozilla)\/([\w\.]+) .+rv\:.+gecko\/\d+',  # Mozilla

        # Other
        r'(polaris|lynx|dillo|icab|doris|amaya|w3m|netsurf|sleipnir|obigo|mosaic|(?:go|ice|up)[\. ]?browser)[-\/ ]?v?([\w\.]+)',  # Polaris/Lynx/Dillo/iCab/Doris/Amaya/w3m/NetSurf/Sleipnir/Obigo/Mosaic/Go/ICE/UP.Browser
        r'(links) \(([\w\.]+)'  # Links
    ], [NAME, VERSION]],

    'cpu': [[
        r'(?:(amd|x(?:(?:86|64)[-_])?|wow|win)64)[;\)]'  # AMD64 (x64)
    ], [[ARCHITECTURE, 'amd64']], [
        r'(ia32(?=;))'  # IA32 (quicktime)
    ], [[ARCHITECTURE, lowerize]], [
        r'((?:i[346]|x)86)[;\)]'  # IA32 (x86)
    ], [[ARCHITECTURE, 'ia32']], [
        r'\b(aarch64|arm(v?8e?l?|_?64))\b'  # ARM64
    ], [[ARCHITECTURE, 'arm64']], [
        r'\b(arm(?:v[67])?ht?n?[fl]p?)\b'  # ARMHF
    ], [[ARCHITECTURE, 'armhf']], [
        r'windows (ce|mobile); ppc;'  # PocketPC mistakenly identified as PowerPC
    ], [[ARCHITECTURE, 'arm']], [
        r'((?:ppc|powerpc)(?:64)?)(?: mac|;|\))'  # PowerPC
    ], [[ARCHITECTURE, r'ower', EMPTY, lowerize]], [
        r'(sun4\w)[;\)]'  # SPARC
    ], [[ARCHITECTURE, 'sparc']], [
        r'((?:avr32|ia64(?=;))|68k(?=\))|\barm(?=v(?:[1-7]|[5-7]1)l?|;|eabi)|(?=atmel )avr|(?:irix|mips|sparc)(?:64)?\b|pa-risc)'  # IA64, 68K, ARM/64, AVR/32, IRIX/64, MIPS/64, SPARC/64, PA-RISC
    ], [[ARCHITECTURE, lowerize]]],

    'device': [[
        # Samsung
        r'\b(sch-i[89]0\d|shw-m380s|sm-[pt]\w{2,4}|gt-[pn]\d{2,4}|sgh-t8[56]9|nexus 10)'
    ], [MODEL, [VENDOR, SAMSUNG], [TYPE, TABLET]], [
        r'\b((?:s[cgp]h|gt|sm)-\w+|galaxy nexus)',
        r'samsung[- ]([-\w]+)',
        r'sec-(sgh\w+)'
    ], [MODEL, [VENDOR, SAMSUNG], [TYPE, MOBILE]], [

        # Apple
        r'\((ip(?:hone|od)[\w ]*);'  # iPod/iPhone
    ], [MODEL, [VENDOR, APPLE], [TYPE, MOBILE]], [
        r'\((ipad);[-\w\),; ]+apple',  # iPad
        r'applecoremedia\/[\w\.]+ \((ipad)',
        r'\b(ipad)\d\d?,\d\d?[;\]].+ios'
    ], [MODEL, [VENDOR, APPLE], [TYPE, TABLET]], [

        # Huawei
        r'\b((?:ag[rs][23]?|bah2?|sht?|btv)-a?[lw]\d{2})\b(?!.+d\/s)'
    ], [MODEL, [VENDOR, HUAWEI], [TYPE, TABLET]], [
        r'(?:huawei|honor)([-\w ]+)[;\)]',
        r'\b(nexus 6p|\w{2,4}-[atu]?[ln][01259x][012359][an]?)\b(?!.+d\/s)'
    ], [MODEL, [VENDOR, HUAWEI], [TYPE, MOBILE]], [

        # Xiaomi
        r'\b(poco[\w ]+)(?: bui|\))',  # Xiaomi POCO
        r'\b; (\w+) build\/hm\1',  # Xiaomi Hongmi 'numeric' models
        r'\b(hm[-_ ]?note?[_ ]?(?:\d\w)?) bui',  # Xiaomi Hongmi
        r'\b(redmi[\-_ ]?(?:note|k)?[\w_ ]+)(?: bui|\))',  # Xiaomi Redmi
        r'\b(mi[-_ ]?(?:a\d|one|one[_ ]plus|note lte|max)?[_ ]?(?:\d?\w?)[_ ]?(?:plus|se|lite)?)(?: bui|\))'  # Xiaomi Mi
    ], [[MODEL, '_', ' '], [VENDOR, XIAOMI], [TYPE, MOBILE]], [
        r'\b(mi[-_ ]?(?:pad)(?:[\w_ ]+))(?: bui|\))'  # Mi Pad tablets
    ], [[MODEL, '_', ' '], [VENDOR, XIAOMI], [TYPE, TABLET]], [

        # OPPO
        r'; (\w+) bui.+ oppo',
        r'\b(cph[12]\d{3}|p(?:af|c[al]|d\w|e[ar])[mt]\d0|x9007|a101op)\b'
    ], [MODEL, [VENDOR, 'OPPO'], [TYPE, MOBILE]], [

        # Vivo
        r'vivo (\w+)(?: bui|\))',
        r'\b(v[12]\d{3}\w?[at])(?: bui|;)'
    ], [MODEL, [VENDOR, 'Vivo'], [TYPE, MOBILE]], [

        # Realme
        r'\b(rmx[12]\d{3})(?: bui|;|\))'
    ], [MODEL, [VENDOR, 'Realme'], [TYPE, MOBILE]], [

        # Motorola
        r'\b(milestone|droid(?:[2-4x]| (?:bionic|x2|pro|razr))?:?( 4g)?)\b[\w ]+build\/',
        r'\bmot(?:orola)?[- ](\w*)',
        r'((?:moto[\w\(\) ]+|xt\d{3,4}|nexus 6)(?= bui|\)))'
    ], [MODEL, [VENDOR, MOTOROLA], [TYPE, MOBILE]], [
        r'\b(mz60\d|xoom[2 ]{0,2}) build\/'
    ], [MODEL, [VENDOR, MOTOROLA], [TYPE, TABLET]], [

        # LG
        r'((?=lg)?[vl]k\-?\d{3}) bui| 3\.[-\w; ]{10}lg?-([06cv9]{3,4})'
    ], [MODEL, [VENDOR, LG], [TYPE, TABLET]], [
        r'(lm(?:-?f100[nv]?|-[\w\.]+)(?= bui|\))|nexus [45])',
        r'\blg[-e;\/ ]+((?!browser|netcast|android tv)\w+)',
        r'\blg-?([\d\w]+) bui'
    ], [MODEL, [VENDOR, LG], [TYPE, MOBILE]], [

        # Lenovo
        r'(ideatab[-\w ]+)',
        r'lenovo ?(s[56]000[-\w]+|tab(?:[\w ]+)|yt[-\d\w]{6}|tb[-\d\w]{6})'
    ], [MODEL, [VENDOR, 'Lenovo'], [TYPE, TABLET]], [

        # Nokia
        r'(?:maemo|nokia).*(n900|lumia \d+)',
        r'nokia[-_ ]?([-\w\.]*)'
    ], [[MODEL, '_', ' '], [VENDOR, 'Nokia'], [TYPE, MOBILE]], [

        # Google
        r'(pixel c)\b'  # Google Pixel C
    ], [MODEL, [VENDOR, GOOGLE], [TYPE, TABLET]], [
        r'droid.+; (pixel[\daxl ]{0,6})(?: bui|\))'  # Google Pixel
    ], [MODEL, [VENDOR, GOOGLE], [TYPE, MOBILE]], [

        # Sony
        r'droid.+ ([c-g]\d{4}|so[-gl]\w+|xq-a\w[4-7][12])(?= bui|\).+chrome\/(?![1-6]{0,1}\d\.))'
    ], [MODEL, [VENDOR, SONY], [TYPE, MOBILE]], [
        r'sony tablet [ps]',
        r'\b(?:sony)?sgp\w+(?: bui|\))'
    ], [[MODEL, 'Xperia Tablet'], [VENDOR, SONY], [TYPE, TABLET]], [

        # OnePlus
        r' (kb2005|in20[12]5|be20[12][59])\b',
        r'(?:one)?(?:plus)? (a\d0\d\d)(?: b|\))'
    ], [MODEL, [VENDOR, 'OnePlus'], [TYPE, MOBILE]], [

        # Amazon
        r'(alexa)webm',
        r'(kf[a-z]{2}wi)( bui|\))',  # Kindle Fire without Silk
        r'(kf[a-z]+)( bui|\)).+silk\/'  # Kindle Fire HD
    ], [MODEL, [VENDOR, AMAZON], [TYPE, TABLET]], [
        r'((?:sd|kf)[0349hijorstuw]+)( bui|\)).+silk\/'  # Fire Phone
    ], [[MODEL, '(.+)', 'Fire Phone $1'], [VENDOR, AMAZON], [TYPE, MOBILE]], [

        # BlackBerry
        r'(playbook);[-\w\),; ]+(rim)'  # BlackBerry PlayBook
    ], [MODEL, VENDOR, [TYPE, TABLET]], [
        r'\b((?:bb[a-f]|st[hv])100-\d)',
        r'\(bb10; (\w+)'  # BlackBerry 10
    ], [MODEL, [VENDOR, BLACKBERRY], [TYPE, MOBILE]], [

        # Asus
        r'(?:\b|asus_)(transfo[prime ]{4,10} \w+|eeepc|slider \w+|nexus 7|padfone|p00[cj])'
    ], [MODEL, [VENDOR, ASUS], [TYPE, TABLET]], [
        r' (z[bes]6[027][012][km][ls]|zenfone \d\w?)\b'
    ], [MODEL, [VENDOR, ASUS], [TYPE, MOBILE]], [

        # HTC
        r'(nexus 9)'  # HTC Nexus 9
    ], [MODEL, [VENDOR, 'HTC'], [TYPE, TABLET]], [
        r'(htc)[-;_ ]{1,2}([\w ]+(?=\)| bui)|\w+)',  # HTC

        # ZTE
        r'(zte)[- ]([\w ]+?)(?: bui|\/|\))',
        r'(alcatel|geeksphone|nexian|panasonic|sony)[-_ ]?([-\w]*)'  # Alcatel/GeeksPhone/Nexian/Panasonic/Sony
    ], [VENDOR, [MODEL, '_', ' '], [TYPE, MOBILE]], [

        # Acer
        r'droid.+; ([ab][1-7]-?[0178a]\d\d?)'
    ], [MODEL, [VENDOR, 'Acer'], [TYPE, TABLET]], [

        # Meizu
        r'droid.+; (m[1-5] note) bui',
        r'\bmz-([-\w]{2,})'
    ], [MODEL, [VENDOR, 'Meizu'], [TYPE, MOBILE]], [

        # Sharp
        r'\b(sh-?[altvz]?\d\d[a-ekm]?)'
    ], [MODEL, [VENDOR, 'Sharp'], [TYPE, MOBILE]], [

        # Mixed
        r'(blackberry|benq|palm(?=\-)|sonyericsson|acer|asus|dell|meizu|motorola|polytron)[-_ ]?([-\w]*)',  # BlackBerry/BenQ/Palm/Sony-Ericsson/Acer/Asus/Dell/Meizu/Motorola/Polytron
        r'(hp) ([\w ]+\w)',  # HP iPAQ
        r'(asus)-?(\w+)',  # Asus
        r'(microsoft); (lumia[\w ]+)',  # Microsoft Lumia
        r'(lenovo)[-_ ]?([-\w]+)',  # Lenovo
        r'(jolla)',  # Jolla
        r'(oppo) ?([\w ]+) bui'  # OPPO
    ], [VENDOR, MODEL, [TYPE, MOBILE]], [
        r'(archos) (gamepad2?)',  # Archos
        r'(hp).+(touchpad(?!.+tablet)|tablet)',  # HP TouchPad
        r'(kindle)\/([\w\.]+)',  # Kindle
        r'(nook)[\w ]+build\/(\w+)',  # Nook
        r'(dell) (strea[kpr\d ]*[\dko])',  # Dell Streak
        r'(le[- ]+pan)[- ]+(\w{1,9}) bui',  # Le Pan Tablets
        r'(trinity)[- ]*(t\d{3}) bui',  # Trinity Tablets
        r'(gigaset)[- ]+(q\w{1,9}) bui',  # Gigaset Tablets
        r'(vodafone) ([\w ]+)(?:\)| bui)'  # Vodafone
    ], [VENDOR, MODEL, [TYPE, TABLET]], [

        r'(surface duo)'  # Surface Duo
    ], [MODEL, [VENDOR, MICROSOFT], [TYPE, TABLET]], [
        r'droid [\d\.]+; (fp\du?)(?: b|\))'  # Fairphone
    ], [MODEL, [VENDOR, 'Fairphone'], [TYPE, MOBILE]], [
        r'(u304aa)'  # AT&T
    ], [MODEL, [VENDOR, 'AT&T'], [TYPE, MOBILE]], [
        r'\bsie-(\w*)'  # Siemens
    ], [MODEL, [VENDOR, 'Siemens'], [TYPE, MOBILE]], [
        r'\b(rct\w+) b'  # RCA Tablets
    ], [MODEL, [VENDOR, 'RCA'], [TYPE, TABLET]], [
        r'\b(venue[\d ]{2,7}) b'  # Dell Venue Tablets
    ], [MODEL, [VENDOR, 'Dell'], [TYPE, TABLET]], [
        r'\b(q(?:mv|ta)\w+) b'  # Verizon Tablet
    ], [MODEL, [VENDOR, 'Verizon'], [TYPE, TABLET]], [
        r'\b(?:barnes[& ]+noble |bn[rt])([\w\+ ]*) b'  # Barnes & Noble Tablet
    ], [MODEL, [VENDOR, 'Barnes & Noble'], [TYPE, TABLET]], [
        r'\b(tm\d{3}\w+) b'
    ], [MODEL, [VENDOR, 'NuVision'], [TYPE, TABLET]], [
        r'\b(k88) b'  # ZTE K Series Tablet
    ], [MODEL, [VENDOR, 'ZTE'], [TYPE, TABLET]], [
        r'\b(nx\d{3}j) b'  # ZTE Nubia
    ], [MODEL, [VENDOR, 'ZTE'], [TYPE, MOBILE]], [
        r'\b(gen\d{3}) b.+49h'  # Swiss GEN Mobile
    ], [MODEL, [VENDOR, 'Swiss'], [TYPE, MOBILE]], [
        r'\b(zur\d{3}) b'  # Swiss ZUR Tablet
    ], [MODEL, [VENDOR, 'Swiss'], [TYPE, TABLET]], [
        r'\b((zeki)?tb.*\b) b'  # Zeki Tablets
    ], [MODEL, [VENDOR, 'Zeki'], [TYPE, TABLET]], [
        r'\b([yr]\d{2}) b',
        r'\b(dragon[- ]+touch |dt)(\w{5}) b'  # Dragon Touch Tablet
    ], [[VENDOR, 'Dragon Touch'], MODEL, [TYPE, TABLET]], [
        r'\b(ns-?\w{0,9}) b'  # Insignia Tablets
    ], [MODEL, [VENDOR, 'Insignia'], [TYPE, TABLET]], [
        r'\b((nxa|next)-?\w{0,9}) b'  # NextBook Tablets
    ], [MODEL, [VENDOR, 'NextBook'], [TYPE, TABLET]], [
        r'\b(xtreme\_)?(v(1[045]|2[015]|[3469]0|7[05])) b'  # Voice Xtreme Phones
    ], [[VENDOR, 'Voice'], MODEL, [TYPE, MOBILE]], [
        r'\b(lvtel\-)?(v1[12]) b'  # LvTel Phones
    ], [[VENDOR, 'LvTel'], MODEL, [TYPE, MOBILE]], [
        r'\b(ph-1) '  # Essential PH-1
    ], [MODEL, [VENDOR, 'Essential'], [TYPE, MOBILE]], [
        r'\b(v(100md|700na|7011|917g).*\b) b'  # Envizen Tablets
    ], [MODEL, [VENDOR, 'Envizen'], [TYPE, TABLET]], [
        r'\b(trio[-\w\. ]+) b'  # MachSpeed Tablets
    ], [MODEL, [VENDOR, 'MachSpeed'], [TYPE, TABLET]], [
        r'\btu_(1491) b'  # Rotor Tablets
    ], [MODEL, [VENDOR, 'Rotor'], [TYPE, TABLET]], [
        r'(shield[\w ]+) b'  # Nvidia Shield Tablets
    ], [MODEL, [VENDOR, 'Nvidia'], [TYPE, TABLET]], [
        r'(sprint) (\w+)'  # Sprint Phones
    ], [VENDOR, MODEL, [TYPE, MOBILE]], [
        r'(kin\.[onetw]{3})'  # Microsoft Kin
    ], [[MODEL, r'\.', ' '], [VENDOR, MICROSOFT], [TYPE, MOBILE]], [
        r'droid.+; (cc6666?|et5[16]|mc[239][23]x?|vc8[03]x?)\)'  # Zebra
    ], [MODEL, [VENDOR, ZEBRA], [TYPE, TABLET]], [
        r'droid.+; (ec30|ps20|tc[2-8]\d[kx])\)'
    ], [MODEL, [VENDOR, ZEBRA], [TYPE, MOBILE]], [

        # Consoles
        r'(ouya)',  # Ouya
        r'(nintendo) ([wids3utch]+)'  # Nintendo
    ], [VENDOR, MODEL, [TYPE, CONSOLE]], [
        r'droid.+; (shield) bui'  # Nvidia
    ], [MODEL, [VENDOR, 'Nvidia'], [TYPE, CONSOLE]], [
        r'(playstation [345portablevi]+)'  # Playstation
    ], [MODEL, [VENDOR, SONY], [TYPE, CONSOLE]], [
        r'\b(xbox(?: one)?(?!; xbox))[\); ]'  # Microsoft Xbox
    ], [MODEL, [VENDOR, MICROSOFT], [TYPE, CONSOLE]], [

        # SmartTVs
        r'smart-tv.+(samsung)'  # Samsung
    ], [VENDOR, [TYPE, SMARTTV]], [
        r'hbbtv.+maple;(\d+)'
    ], [[MODEL, '^', 'SmartTV'], [VENDOR, SAMSUNG], [TYPE, SMARTTV]], [
        r'(nux; netcast.+smarttv|lg (netcast\.tv-201\d|android tv))'  # LG SmartTV
    ], [[VENDOR, LG], [TYPE, SMARTTV]], [
        r'(apple) ?tv'  # Apple TV
    ], [VENDOR, [MODEL, APPLE + ' TV'], [TYPE, SMARTTV]], [
        r'crkey'  # Google Chromecast
    ], [[MODEL, CHROME + 'cast'], [VENDOR, GOOGLE], [TYPE, SMARTTV]], [
        r'droid.+aft(\w)( bui|\))'  # Fire TV
    ], [MODEL, [VENDOR, AMAZON], [TYPE, SMARTTV]], [
        r'\(dtv[\);].+(aquos)'  # Sharp
    ], [MODEL, [VENDOR, 'Sharp'], [TYPE, SMARTTV]], [
        r'\b(roku)[\dx]*[\)\/]((?:dvp-)?[\d\.]*)',  # Roku
        r'hbbtv\/\d+\.\d+\.\d+ +\([\w ]*; *(\w[^;]*);([^;]*)'  # HbbTV devices
    ], [[VENDOR, trim], [MODEL, trim], [TYPE, SMARTTV]], [
        r'\b(android tv|smart[- ]?tv|opera tv|tv; rv:)\b'  # SmartTV from Unidentified Vendors
    ], [[TYPE, SMARTTV]], [

        # Wearables
        r'((pebble))app'  # Pebble
    ], [VENDOR, MODEL, [TYPE, WEARABLE]], [
        r'droid.+; (glass) \d'  # Google Glass
    ], [MODEL, [VENDOR, GOOGLE], [TYPE, WEARABLE]], [
        r'droid.+; (wt63?0{2,3})\)'
    ], [MODEL, [VENDOR, ZEBRA], [TYPE, WEARABLE]], [
        r'(quest( 2)?)'  # Oculus Quest
    ], [MODEL, [VENDOR, FACEBOOK], [TYPE, WEARABLE]], [

        # Embedded
        r'(tesla)(?: qtcarbrowser|\/[-\w\.]+)'  # Tesla
    ], [VENDOR, [TYPE, EMBEDDED]], [

        # Mixed (Generic)
        r'droid .+?; ([^;]+?)(?: bui|\) applew).+? mobile safari'  # Android Phones from Unidentified Vendors
    ], [MODEL, [TYPE, MOBILE]], [
        r'droid .+?; ([^;]+?)(?: bui|\) applew).+?(?! mobile) safari'  # Android Tablets from Unidentified Vendors
    ], [MODEL, [TYPE, TABLET]], [
        r'\b((tablet|tab)[;\/]|focus\/\d(?!.+mobile))'  # Unidentifiable Tablet
    ], [[TYPE, TABLET]], [
        r'(phone|mobile(?:[;\/]| safari)|pda(?=.+windows ce))'  # Unidentifiable Mobile
    ], [[TYPE, MOBILE]], [
        r'(android[-\w\. ]{0,9});.+buil'  # Generic Android Device
    ], [MODEL, [VENDOR, 'Generic']]],

    'engine': [[
        r'windows.+ edge\/([\w\.]+)'  # EdgeHTML
    ], [VERSION, [NAME, EDGE + 'HTML']], [
        r'webkit\/537\.36.+chrome\/(?!27)([\w\.]+)'  # Blink
    ], [VERSION, [NAME, 'Blink']], [
        r'(presto)\/([\w\.]+)',  # Presto
        r'(webkit|trident|netfront|netsurf|amaya|lynx|w3m|goanna)\/([\w\.]+)',  # WebKit/Trident/NetFront/NetSurf/Amaya/Lynx/w3m/Goanna
        r'ekioh(flow)\/([\w\.]+)',  # Flow
        r'(khtml|tasman|links)[\/ ]\(?([\w\.]+)',  # KHTML/Tasman/Links
        r'(icab)[\/ ]([23]\.[\d\.]+)'  # iCab
    ], [NAME, VERSION], [
        r'rv\:([\w\.]{1,9})\b.+(gecko)'  # Gecko
    ], [VERSION, NAME]],

    'os': [[
        # Windows
        r'microsoft (windows) (vista|xp)'  # Windows (iTunes)
    ], [NAME, VERSION], [
        r'(windows) nt 6\.2; (arm)',  # Windows RT
        r'(windows (?:phone(?: os)?|mobile))[\/ ]?([\d\.\w ]*)',  # Windows Phone
        r'(windows)[\/ ]?([ntce\d\. ]+\w)(?!.+xbox)'
    ], [NAME, [VERSION, str_mapper, WINDOWS_VERSION_MAP]], [
        r'(win(?=3|9|n)|win 9x )([nt\d\.]+)'
    ], [[NAME, 'Windows'], [VERSION, str_mapper, WINDOWS_VERSION_MAP]], [

        # iOS/macOS
        r'ip[honead]{2,4}\b(?:.*os ([\w]+) like mac|; opera)',  # iOS
        r'cfnetwork\/.+darwin'
    ], [[VERSION, '_', '.'], [NAME, 'iOS']], [
        r'(mac os x) ?([\w\. ]*)',
        r'(macintosh|mac_powerpc\b)(?!.+haiku)'  # Mac OS
    ], [[NAME, 'Mac OS'], [VERSION, '_', '.']], [

        # Mobile OSes
        r'droid ([\w\.]+)\b.+(android[- ]x86)'  # Android-x86
    ], [VERSION, NAME], [
        r'(android|webos|qnx|bada|rim tablet os|maemo|meego|sailfish)[-\/ ]?([\w\.]*)',  # Android/WebOS/QNX/Bada/RIM/Maemo/MeeGo/Sailfish OS
        r'(blackberry)\w*\/([\w\.]*)',  # Blackberry
        r'(tizen|kaios)[\/ ]([\w\.]+)',  # Tizen/KaiOS
        r'\((series40);'  # Series 40
    ], [NAME, VERSION], [
        r'\(bb(10);'  # BlackBerry 10
    ], [VERSION, [NAME, BLACKBERRY]], [
        r'(?:symbian ?os|symbos|s60(?=;)|series60)[-\/ ]?([\w\.]*)'  # Symbian
    ], [VERSION, [NAME, 'Symbian']], [
        r'mozilla\/[\d\.]+ \((?:mobile|tablet|tv|mobile; [\w ]+); rv:.+ gecko\/([\w\.]+)'  # Firefox OS
    ], [VERSION, [NAME, FIREFOX + ' OS']], [
        r'web0s;.+rt(tv)',
        r'\b(?:hp)?wos(?:browser)?\/([\w\.]+)'  # WebOS
    ], [VERSION, [NAME, 'webOS']], [

        # Google Chromecast
        r'crkey\/([\d\.]+)'  # Google Chromecast
    ], [VERSION, [NAME, CHROME + 'cast']], [
        r'(cros) [\w]+ ([\w\.]+\w)'  # Chromium OS
    ], [[NAME, 'Chromium OS'], VERSION], [

        # Console
        r'(nintendo|playstation) ([wids345portablevuch]+)',  # Nintendo/Playstation
        r'(xbox); +xbox ([^\);]+)',  # Microsoft Xbox (360, One, X, S, Series X, Series S)

        # Other
        r'\b(joli|palm)\b ?(?:os)?\/?([\w\.]*)',  # Joli/Palm
        r'(mint)[\/\(\) ]?(\w*)',  # Mint
        r'(mageia|vectorlinux)[; ]',  # Mageia/VectorLinux
        r'([kxln]?ubuntu|debian|suse|opensuse|gentoo|arch(?= linux)|slackware|fedora|mandriva|centos|pclinuxos|red ?hat|zenwalk|linpus|raspbian|plan 9|minix|risc os|contiki|deepin|manjaro|elementary os|sabayon|linspire)(?: gnu\/linux)?(?: enterprise)?(?:[- ]linux)?(?:-gnu)?[-\/ ]?(?!chrom|package)([-\w\.]*)',  # Ubuntu/Debian/SUSE/Gentoo/Arch/Slackware/Fedora/Mandriva/CentOS/PCLinuxOS/RedHat/Zenwalk/Linpus/Raspbian/Plan9/Minix/RISCOS/Contiki/Deepin/Manjaro/elementary/Sabayon/Linspire
        r'(hurd|linux) ?([\w\.]*)',  # Hurd/Linux
        r'(gnu) ?([\w\.]*)',  # GNU
        r'\b([-frentopcghs]{0,5}bsd|dragonfly)[\/ ]?(?!amd|[ix346]{1,2}86)([\w\.]*)',  # FreeBSD/NetBSD/OpenBSD/PC-BSD/GhostBSD/DragonFly
        r'(haiku) (\w+)'  # Haiku
    ], [NAME, VERSION], [
        r'(sunos) ?([\w\.\d]*)'  # Solaris
    ], [[NAME, 'Solaris'], VERSION], [
        r'((?:open)?solaris)[-\/ ]?([\w\.]*)',  # Solaris
        r'(aix) ((\d)(?=\.|\)| )[\w\.])*',  # AIX
        r'\b(beos|os\/2|amigaos|morphos|openvms|fuchsia|hp-ux)',  # BeOS/OS2/AmigaOS/MorphOS/OpenVMS/Fuchsia/HP-UX
        r'(unix) ?([\w\.]*)'  # UNIX
    ], [NAME, VERSION]]
}

# compile regexes
for regexes in REGEXES.values():
    for idx in range(0, len(regexes), 2):
        regexes[idx] = [re.compile(r, re.IGNORECASE) for r in regexes[idx]]


def rgx_mapper(ua, arrays):
    if not ua:
        return None

    i = 0
    matches = False
    # loop through all regexes maps
    while i < len(arrays) and not matches:
        regex = arrays[i]  # even sequence (0,2,4,..)
        props = arrays[i + 1]  # odd sequence (1,3,5,..)
        j = k = 0

        # try matching uastring with regexes
        while j < len(regex) and not matches:
            matches = regex[j].search(ua)
            j += 1
            if matches:
                for p in range(len(props)):
                    k += 1
                    try:
                        match = matches.group(k)
                    except IndexError as _:
                        match = None

                    q = props[p]
                    # check if given property is actually array
                    if isinstance(q, list):
                        if len(q) == 2:
                            if callable(q[1]):
                                # assign modified match
                                yield q[0], q[1](match)
                            else:
                                # assign given value, ignore regex match
                                yield q[0], q[1]
                        elif len(q) == 3:
                            # check whether function or regex
                            if callable(q[1]):
                                # call function (usually string mapper)
                                yield q[0], q[1](match, q[2]) if match else None
                            else:
                                # sanitize match using given regex
                                yield q[0], re.sub(q[1], q[2].replace('$', '\\'), match) if match else None
                        elif len(q) == 4:
                            yield q[0], q[3](re.sub(q[1], q[2].replace('$', '\\'), match)) if match else None
                    else:
                        yield q, match if match else None
        i += 2


class UAParser:
    """Python implementation of User Agent parser. Fork UAParser.js"""

    def __init__(self, ua):
        self._ua = trim(ua)[0:UA_MAX_LENGTH] if ua and len(ua) > UA_MAX_LENGTH else ua

    @classmethod
    def parse(cls, ua):
        self = cls(ua)
        return {
            'ua': self.ua,
            'browser': self.browser,
            'cpu': self.cpu,
            'device': self.device,
            'engine': self.engine,
            'os': self.os
        }

    @property
    def browser(self):
        _browser = {NAME: None, VERSION: None, MAJOR: None}
        for key, value in rgx_mapper(self._ua, REGEXES['browser']):
            _browser[key] = value
        _browser[MAJOR] = majorize(_browser[VERSION])
        return _browser

    @property
    def cpu(self):
        _cpu = {ARCHITECTURE: None}
        for key, value in rgx_mapper(self._ua, REGEXES['cpu']):
            _cpu[key] = value
        return _cpu

    @property
    def device(self):
        _device = {VENDOR: None, MODEL: None, TYPE: None}
        for key, value in rgx_mapper(self._ua, REGEXES['device']):
            _device[key] = value
        return _device

    @property
    def engine(self):
        _engine = {NAME: None, VERSION: None}
        for key, value in rgx_mapper(self._ua, REGEXES['engine']):
            _engine[key] = value
        return _engine

    @property
    def os(self):
        _os = {NAME: None, VERSION: None}
        for key, value in rgx_mapper(self._ua, REGEXES['os']):
            _os[key] = value
        return _os

    @property
    def ua(self):
        return self._ua
