# coding: utf-8
import varnishapi

vsc = varnishapi.VarnishStat()
r= vsc.getStats();
for k,v in r.iteritems():
    print "%40s %20s %s" % (k,v['val'],v['desc'])
