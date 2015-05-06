==================
python-varnishapi
==================


------------------------------------
Connect to libvarnish api by ctypes
------------------------------------

:Author: Shohei Tanaka(@xcir)
:Date: 2015-03-14
:Version: 0.4-varnish40
:Support Varnish Version: 4.0.x
:Manual section: 3

For Varnish3.0.x
=================
See this link.
https://github.com/xcir/python-varnishapi/tree/varnish30

DESCRIPTION
============
Connect to libvarnish api by ctypes


VSLUtil class
---------------------------------------

VSLUtil.tag2VarName
-------------------

Prototype
        ::

                tag2VarName(tag, data)

Parameter
        ::

                
                STRING tag
                STRING data

Return value
        ::

                STRING Variable name
                

Description
        ::

                Transcode spec and tagname to variable name
Example
        ::

                vut = VSLUtil()

                # output is "resp.http.Host"
                print vut.tag2VarName('RespHeader','Host: example.net')


VarnishStat class
---------------------------------------

VarnishStat.__init__
-----------------------

Prototype
        ::

                VarnishStat(opt = '', sopath = 'libvarnishapi.so.1')

Parameter
        ::

                LIST   arg [OPTION]
                STRING libvarnishapi path [OPTION]

Return value
        ::

                class object
                

Description
        ::

                initialize
Example
        ::

                vsc = VarnishStat()
                
                #set arg
                vsc = VarnishStat(['-n', 'v2'])

VarnishStat.getStats
---------------------

Prototype
        ::

                getStats()

Parameter
        ::

                
                VOID

Return value
        ::

                DICT stats
                

Description
        ::

                Get statistics counter
Example
        ::

                vsc = varnishapi.VarnishStat()
                r= vsc.getStat();
                for k,v in r.iteritems():
                    #output
                    #                         MAIN.fetch_zero                    0 Fetch zero len body
                    #                              MAIN.vmods                    1 Loaded VMODs
                    #                       MAIN.sess_dropped                    0 Sessions dropped for thread
                    #                           LCK.ban.locks              1457831 Lock Operations
                    #...
                    print "%40s %20s %s" % (k,v['val'],v['desc'])


VarnishLog class
---------------------------------------

VarnishLog.__init__
-----------------------

Prototype
        ::

                VarnishLog(opt = '', sopath = 'libvarnishapi.so.1')

Parameter
        ::

                LIST   arg [OPTION]
                STRING libvarnishapi path [OPTION]

Return value
        ::

                class object
                

Description
        ::

                initialize
Example
        ::

                vsl = VarnishLog()
                
                #set arg
                vsl = VarnishLog(['-n', 'v2'])


VarnishLog.Fini
-----------------------

Prototype
        ::

                Fini()

Parameter
        ::

                VOID

Return value
        ::

                VOID
                

Description
        ::

                finish
Example
        ::

                vsl = VarnishLog()
                ...
                vsl.Fini()

VarnishLog.Dispatch
-----------------------

Prototype
        ::

                Dispatch(cb, priv = None)

Parameter
        ::

                FUNC    cb   callback function
                OBJECT  priv 

Return value
        ::

                INT
                

Description
        ::

                Dispatch callback function

Example
        ::

                def cb(vap,cbd,priv):
                    #output
                    #...
                    #{'level': 0L, 'type': 'c', 'reason': 0, 'vxid_parent': 0, 'length': 22L, 'tag': 26L, 'vxid': 65709, 'data': 'Vary: Accept-Encoding\x00', 'isbin': 0L}
                    #{'level': 0L, 'type': 'c', 'reason': 0, 'vxid_parent': 0, 'length': 23L, 'tag': 26L, 'vxid': 65709, 'data': 'Content-Encoding: gzip\x00', 'isbin': 0L}
                    #...
                    print cbd

                vsl = varnishapi.VarnishLog(['-c'])
                while 1:
                    ret = vsl.Dispatch(cb)
                    if 0 == ret:
                        time.sleep(0.5)
                vsl.Fini()

VarnishLog.VSL_tags
-----------------------

Prototype
        ::

                #This is dictionary variable
                VSL_tags[tag]

Return value
        ::

                STRING tagname
                

Description
        ::

                Transcode tag index to tag text

Example
        ::

                def cb(vap,cbd,priv):
                    #output
                    #...
                    #VCL_call
                    #VCL_return
                    #...
                    print vap.VSL_tags[cbd['tag']]

                vsl = varnishapi.VarnishLog(['-c'])
                while 1:
                    ret = vsl.Dispatch(cb)
                    if 0 == ret:
                        time.sleep(0.5)
                vsl.Fini()


HISTORY
===========

Version 0.4-varnish40: Support change to Varnish4

Version 0.3-varnish30: Support VSM_ReOpen

Version 0.2-varnish30: Support VSL_Arg

Version 0.1-varnish30: First version


COPYRIGHT
===========

python-varnishapi

* Copyright (c) 2015 Shohei Tanaka(@xcir)

Varnish Cache

* Copyright (c) 2006-2015 Varnish Software AS
