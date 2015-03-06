==================
python-varnishapi
==================


------------------------------------
Connect to libvarnish api by ctypes
------------------------------------

:Author: Shohei Tanaka(@xcir)
:Date: 2015-03-07
:Version: x.x-varnish40
:Support Varnish Version: 4.0.x
:Manual section: 3

For Varnish3.0.x
=================
See this link.
https://github.com/xcir/python-varnishapi/tree/varnish30

DESCRIPTION
============
Connect to libvarnish api by ctypes

IN DEVELOPMENT.

DON'T USE PRODUCTION.

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

                vut = varnishapi.VSLUtil()

                # output is "resp.http.Host"
                print vut.tag2VarName('RespHeader','Host: example.net')



HISTORY
===========

Version x.x-varnish40: Support change to Varnish4

Version 0.3-varnish30: Support VSM_ReOpen

Version 0.2-varnish30: Support VSL_Arg

Version 0.1-varnish30: First version


COPYRIGHT
===========

python-varnishapi

* Copyright (c) 2015 Shohei Tanaka(@xcir)

Varnish Cache

* Copyright (c) 2006-2015 Varnish Software AS