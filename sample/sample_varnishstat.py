# coding: utf-8
import varnishapi

vap = varnishapi.VarnishStat()
r= vap.getstat();
for k,v in r.iteritems():
    print "%40s %20s %s" % (k,v['val'],v['desc'])
