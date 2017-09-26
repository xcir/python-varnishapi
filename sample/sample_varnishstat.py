#!/usr/bin/python

# coding: utf-8
import varnishapi

arg           = {}

vsc = varnishapi.VarnishStat(**arg)
if vsc.error:
	print(vsc.error)
	exit(1)
r= vsc.getStats()
for k,v in r.items():
	print("%40s %20s %s" % (k,v['val'],v['desc']))
vsc.Fini()
