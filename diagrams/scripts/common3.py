import sys, os
sys.path.insert(0, "/home/claude/blog/tools")
from build_avd_post00_common import *
import build_avd_post00_common as _c
OUTD = "/home/claude/cloud-ai-notes-rewritten/src/img/avd/"
_c.OUTD = OUTD
ICONS.update({
 "avd": "other/00327-icon-service-Azure-Virtual-Desktop.svg",
 "afd": "networking/10073-icon-service-Front-Door-and-CDN-Profiles.svg",
 "tm": "networking/10065-icon-service-Traffic-Manager-Profiles.svg",
 "sql": "databases/10130-icon-service-SQL-Database.svg",
 "hostpool": "compute/00328-icon-service-Host-Pools.svg",
 "resolver": "networking/02882-icon-service-DNS-Private-Resolver.svg",
 "plink": "networking/00427-icon-service-Private-Link.svg",
 "dnsz": "networking/10064-icon-service-DNS-Zones.svg",
 "vwanhub": "networking/00860-icon-service-Virtual-WAN-Hub.svg",
})
def finish3(d, name, did, dname):
    check(d, name)
    svg = d.svg().replace('markerWidth="8" markerHeight="8"', 'markerWidth="4" markerHeight="4"')
    open(OUTD+name+".svg", "w", encoding="utf-8").write(svg)
    open(OUTD+name+".drawio", "w", encoding="utf-8").write(d.drawio(did, dname))
    render_png(OUTD+name+".svg", OUTD+name+".png", d.w, d.h)
