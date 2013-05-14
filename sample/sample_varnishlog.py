# coding: utf-8

import varnishapi,time

def main():
	smp = SampleVarnishLog()
	smp.execute()

class SampleVarnishLog:
	def __init__(self):
		#connect varnishapi
		self.vap     = varnishapi.VarnishAPI()
		#utils
		self.vslutil = varnishapi.VSLUtil()

	def execute(self):
		while 1:
			#dispatch
			self.vap.VSL_NonBlockingDispatch(self.vapCallBack)
			time.sleep(0.1)

	def vapCallBack(self, priv, tag, fd, length, spec, ptr, bm):
		if spec == 0:
			return

		nml = self.vap.normalizeDic(priv, tag, fd, length, spec, ptr, bm)
		'''
			[rawdata]
			12 ObjHeader    c Cache-Control: max-age=0, no-cache
			
			[dict]
			'fd'      : 12,
			'type'    : 1,
			'typeName': 'c',
			'tag'     : 'ObjHeader',
			'msg'     : 'Cache-Control: max-age=0, no-cache',
		'''
		if spec == 1:
			if nml['tag'][0:2] == "Rx":
				nml['rxtx'] = 'Client -> Varnish'
			elif nml['tag'][0:2] == "Tx":
				nml['rxtx'] = 'Client <- Varnish'
			else:
				nml['rxtx'] = "Client"
		elif spec == 2:
			if nml['tag'][0:2] == "Rx":
				nml['rxtx'] = 'Varnish <- Backend'
			elif nml['tag'][0:2] == "Tx":
				nml['rxtx'] = 'Varnish -> Backend'
			else:
				nml['rxtx'] = "Backend"

		nml['var'] = self.vslutil.tags[spec][nml['tag']]
		print "%5d %-20s %-12s %-16s %s" % (nml['fd'], nml['rxtx'], nml['tag'], nml['var'], nml['msg'])

main()
