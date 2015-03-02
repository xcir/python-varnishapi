# coding: utf-8
import varnishapi,time,os,sys,syslog,traceback

class SampleVarnishLog:
	def execute(self,vap):
		#connect varnishapi
		self.vap     = vap
		self.vap.Setup()
		while 1:
			ret = self.vap.DispatchMulti(self.vapCallBack)
			if 0 == ret:
				time.sleep(0.5)
		
		
	def vapCallBack(self,vap,level,vxid,vxid_parent,tag,type,data,isbin,length):
	    t_tag = vap.VSL_tags[tag]
	    print "level:%d vxid:%d vxid_parent:%d tag:%s type:%s data:%s (isbin=%d,len=%d)" % (level,vxid,vxid_parent,t_tag,type,data,isbin,length)

def main(smp):
	try:
		vap = varnishapi.VarnishAPI(['-q','requrl ~ "/hello"','-g','request'])
		smp.execute(vap)
	except KeyboardInterrupt:
		vap.Fini()
	except Exception as e:
		syslog.openlog(sys.argv[0], syslog.LOG_PID|syslog.LOG_PERROR, syslog.LOG_LOCAL0)
		syslog.syslog(syslog.LOG_ERR, traceback.format_exc())

if __name__ == '__main__':
	smp = SampleVarnishLog()
	main(smp)

	    
