#!/usr/bin/python

# coding: utf-8
import time,os,sys,syslog,traceback,varnishapi

class SampleVarnishLog:
	def execute(self, vap):
		#connect varnishapi
		self.vap     = vap
		self.headline = None
		self.buf = ""
		self.tnames = {
			vap.defi.VSL_t_unknown : 'unknown',
			vap.defi.VSL_t_sess : 'sess',
			vap.defi.VSL_t_req : 'req',
			vap.defi.VSL_t_bereq : 'bereq',
			vap.defi.VSL_t_raw : 'raw',
		}
		while 1:
			ret = self.vap.Dispatch(self.vapLineCallBack,None,0,self.vapVxidCallBack,self.vapGroupCallBack)
			if 0 >= ret:
				time.sleep(0.5)
		
		
	def vapGroupCallBack(self,vap, priv):
		print("-"*100)
	def vapVxidCallBack(self,vap, priv):
		trx_type    = self.headline['transaction_type']
		vxid        = self.headline['vxid']
		level       = self.headline['level']
		print("\n%s << %s >> %d" % ('*'*level,self.tnames[trx_type],vxid))
		print(self.buf.rstrip("\n"))
		self.headline = None
		self.buf = ""

	def vapLineCallBack(self, vap, cbd, priv):
		level       = cbd['level']
		vxid        = cbd['vxid']
		vxid_parent = cbd['vxid_parent']
		type        = cbd['type']
		trx_type    = cbd['transaction_type']
		tag         = cbd['tag']
		data        = cbd['data']
		isbin       = cbd['isbin']
		length      = cbd['length']
		t_tag = vap.VSL_tags[tag]
		var   = vap.vut.tag2VarName(t_tag,data)
		if self.headline is None:
			self.headline = cbd

		self.buf +="%s level:%d vxid:%d vxid_parent:%d tag:%s var:%s type:%s data:%s (isbin=%d,len=%d)\n" % ('-'*level,level,vxid,vxid_parent,t_tag,var,type,data,isbin,length)


def main(smp):
	try:
		arg          = {}
		arg["opt"]   = ['-g','session']
		vap = varnishapi.VarnishLog(**arg)
		if vap.error:
			print(vap.error)
			exit(1)
		smp.execute(vap)
	except KeyboardInterrupt:
		vap.Fini()
	except Exception as e:
		syslog.openlog(sys.argv[0], syslog.LOG_PID|syslog.LOG_PERROR, syslog.LOG_LOCAL0)
		syslog.syslog(syslog.LOG_ERR, traceback.format_exc())

if __name__ == '__main__':
	smp = SampleVarnishLog()
	main(smp)

	    
