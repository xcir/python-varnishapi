==================
python-varnishapi
==================


------------------------------------
Connect to libvarnish api by ctypes
------------------------------------

:Author: Shohei Tanaka(@xcir)
:Date: 2014-03-11
:Version: 0.3
:Support Varnish Version: 3.0.x
:Manual section: 3



DESCRIPTION
============
Connect to libvarnish api by ctypes


VSLUtil class
---------------------------------------

VSLUtil.tag2VarKey
-------------------

Prototype
        ::

                tag2VarKey(spec, tag)

Parameter
        ::

                INT    spec
                  1 : client
                  2 : backend
                  0 : other
                
                
                STRING tag

Return value
        ::

                STRING Variable name
                

Description
        ::

                Transcode spec and tagname to variable name
Example
        ::

                vut = varnishapi.VSLUtil()

                # output is "resp.response"
                print vut.tag2VarKey(1, 'TxResponse')

VSLUtil.tags
-------------------

Prototype
        ::

                #This is dictionary variable
                tags[spec][tagName]

Parameter
        ::

                INT    spec
                  1 : client
                  2 : backend
                  0 : other
                
                
                STRING tagName

Return value
        ::

                STRING Variable name
                

Description
        ::

                Transcode spec and tagname to variable name
Example
        ::

                vut = varnishapi.VSLUtil()

                # output is "resp.response"
                print vut.tags[1]['TxResponse']



VarnishAPI class
---------------------------------------

VarnishAPI.__init__
-------------------

Prototype
        ::

                varnishapi(opt = '', sopath = 'libvarnishapi.so.1')

Parameter
        ::

                LIST   VSL arg [OPTION]
                STRING libvarnishapi path [OPTION]

Return value
        ::

                class object
                

Description
        ::

                initialize
Example
        ::

                vap = varnishapi.VarnishAPI()
                
                #set VSL arg
                vap = varnishapi.VarnishAPI(['-c', '-i', 'RxUrl'])


VarnishAPI.VSL_Dispatch
-------------------

Prototype
        ::

                VSL_Dispatch(func, priv = False)

Parameter
        ::

                VSL_handler_f func
                object priv

Return value
        ::

                void
                

Description
        ::

                Dispatch callback function
Example
        ::

                def vapCallBack(priv, tag, fd, length, spec, ptr, bm):
                    print 'hello'

                def main():
                    vap = varnishapi.VarnishAPI()
                    while 1:
                        vap.VSL_Dispatch(vapCallBack)
                    
                main()


VarnishAPI.VSL_NonBlockingDispatch
-------------------

Prototype
        ::

                VSL_NonBlockingDispatch(func, priv = False)

Parameter
        ::

                VSL_handler_f func
                object priv

Return value
        ::

                void
                

Description
        ::

                Dispatch callback function.(None blocking)
Example
        ::

                def vapCallBack(priv, tag, fd, length, spec, ptr, bm):
                    print 'hello'

                def main():
                    vap = varnishapi.VarnishAPI()
                    while 1:
                        vap.VSL_NonBlockingDispatch(vapCallBack)
                        sleep(0.1)
                    
                main()

VarnishAPI.VSM_ReOpen
-------------------

Prototype
        ::

                VSM_ReOpen(diag = 0)

Parameter
        ::

                int diag

Return value
        ::

                int

Description
        ::

                Check if shared memory segment needs to be reopened/remapped.
                VSM reopen/remap ,as required.
Example
        ::

                class sample
                    def vapCallBack(self, priv, tag, fd, length, spec, ptr, bm):
                        self.last = time.time()
                        print 'hello'

                    def execute(self):
                        self.vap  = varnishapi.VarnishAPI()
                        self.last = int(time.time())
                        while 1:
                            self.vap.VSL_NonBlockingDispatch(self.vapCallBack)
                            time.sleep(0.1)
                            #Check vsm
                            if int(time.time()) - self.last > 5:
                                self.vap.VSM_ReOpen()
                                self.last  = int(time.time())

                smp = sample()
                smp.execute()


VarnishAPI.VSL_Name2Tag
-------------------

Prototype
        ::

                VSL_Name2Tag(name)

Parameter
        ::

                STRING name

Return value
        ::

                INT tagNumber
                

Description
        ::

                Convert Name to Tag.
Example
        ::

                    vap = varnishapi.VarnishAPI()
                    vap.VSL_Name2Tag("ReqEnd")

VarnishAPI.VSL_NameNormalize
-------------------

Prototype
        ::

                VSL_NameNormalize(name)

Parameter
        ::

                STRING name

Return value
        ::

                STRING name
                

Description
        ::

                Normalize to name
Example
        ::

                    vap = varnishapi.VarnishAPI()
                    # output is ReqEnd
                    print vap.VSL_NameNormalize("rEqeNd")

VarnishAPI.normalizeDic
-------------------

Prototype
        ::

                normalizeDic(priv, tag, fd, length, spec, ptr, bm)

Parameter
        ::

                c_void_p    priv
                c_int       tag
                c_uint      fd
                c_uint      length
                c_uint      spec
                c_char_p    ptr
                c_ulonglong bm

Return value
        ::

                DICT data
                

Description
        ::

                Process to callback data.
Example
        ::

                class sample:
                   def vapCallBack(self, priv, tag, fd, length, spec, ptr, bm):
                       r = self.vap.normalizeDic(priv, tag, fd, length, spec, ptr, bm)
                       print r['fd']
                       print r['type']
                       print r['typeName']
                       print r['tag']
                       print r['msg']
                
                
                   def main(self):
                       self.vap = varnishapi.VarnishAPI('', '/usr/lib64/libvarnishapi.so.1')
                       while 1:
                           self.vap.VSL_NonBlockingDispatch(self.vapCallBack)
                           time.sleep(0.1)
                
                cl=sample()
                cl.main()

HISTORY
===========

Version 0.3: Support VSM_ReOpen

Version 0.2: Support VSL_Arg

Version 0.1: First version



