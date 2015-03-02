# coding: utf-8

from ctypes import *
import sys,getopt


class VSLC_ptr(Structure):
  #_fields_ = [("ptr" , POINTER(c_uint32)), #const uint32_t        *ptr; /* Record pointer */
  _fields_ = [("ptr" , POINTER(c_uint32)),  #const uint32_t        *ptr; /* Record pointer */
        ("priv", c_uint)                    #unsigned              priv;
         ]

class VSL_cursor(Structure):
  _fields_ = [("rec" , VSLC_ptr),        #struct VSLC_ptr rec;
        ("priv_tbl", c_void_p),          #const void      *priv_tbl;
        ("priv_data", c_void_p)          #void            *priv_data;
         ]

class VSL_transaction(Structure):
  _fields_ = [("level" , c_uint),   #unsigned               level;
        ("vxid", c_int32),          #int32_t                vxid;
        ("vxid_parent", c_int32),   #int32_t                vxid_parent;
        ("type", c_int),            #enum VSL_transaction_e type;
        ("reason", c_int),          #enum VSL_reason_e      reason;
        ("c", POINTER(VSL_cursor))  #struct VSL_cursor      *c;

         ]



class VTAILQ_HEAD(Structure):
  _fields_ = [("vtqh_first" , c_void_p),       #struct type *vtqh_first;    /* first element */        \
        ("vtqh_last", POINTER(c_void_p))       #struct type **vtqh_last;    /* addr of last next element */    \
         ]

class vbitmap(Structure):
  _fields_ = [("bits" , c_void_p),  #VBITMAP_TYPE    *bits;
        ("nbits", c_uint)           #unsigned        nbits;
         ]

class vsb(Structure):
  _fields_ = [("magic" , c_uint), #unsigned   magic;
        ("s_buf", c_char_p),      #char       *s_buf;    /* storage buffer */
        ("s_error", c_int),       #int        s_error;   /* current error code */
        ("s_size", c_ssize_t),    #ssize_t    s_size;    /* size of storage buffer */
        ("s_len", c_ssize_t),     #ssize_t    s_len;     /* current length of string */
        ("s_flags", c_int)        #int        s_flags;   /* flags */
         ]

class VSL_data(Structure):
  _fields_ = [("magic", c_uint),           #unsigned           magic;
        ("diag", POINTER(vsb)),            #struct vsb         *diag;
        ("flags", c_uint),                 #unsigned           flags;
        ("vbm_select", POINTER(vbitmap)),  #struct vbitmap     *vbm_select;
        ("vbm_supress", POINTER(vbitmap)), #struct vbitmap     *vbm_supress;
        ("vslf_select", VTAILQ_HEAD),      #vslf_list          vslf_select;
        ("vslf_suppress", VTAILQ_HEAD),    #vslf_list          vslf_suppress;
        ("b_opt", c_int),                  #int                b_opt;
        ("c_opt", c_int),                  #int                c_opt;
        ("C_opt", c_int),                  #int                C_opt;
        ("L_opt", c_int),                  #int                L_opt;
        ("T_opt", c_double),               #double             T_opt;
        ("v_opt", c_int)                   #int                v_opt;
         ]

#typedef int VSLQ_dispatch_f(struct VSL_data *vsl, struct VSL_transaction * const trans[], void *priv);

VSLQ_dispatch_f = CFUNCTYPE(c_int,
  POINTER(VSL_data),POINTER(POINTER(VSL_transaction)),c_void_p
  )


class VarnishAPIDefine40:
    def __init__(self):
        self.VSL_COPT_TAIL     = (1 << 0)
        self.VSL_COPT_BATCH    = (1 << 1)
        self.VSL_COPT_TAILSTOP = (1 << 2)
        self.SLT_F_BINARY      = (1 << 1)
        
        '''
        //////////////////////////////
        enum VSL_transaction_e {
            VSL_t_unknown,
            VSL_t_sess,
            VSL_t_req,
            VSL_t_bereq,
            VSL_t_raw,
            VSL_t__MAX,
        };
        '''
        self.VSL_t_unknown = 0
        self.VSL_t_sess    = 1
        self.VSL_t_req     = 2
        self.VSL_t_bereq   = 3
        self.VSL_t_raw     = 4
        self.VSL_t__MAX    = 5


class LIBVARNISHAPI13:
    def __init__(self,lib):
        self.VSL_CursorFile         = lib.VSL_CursorFile
        self.VSL_CursorFile.restype = c_void_p

        self.VSL_CursorVSM         = lib.VSL_CursorVSM
        self.VSL_CursorVSM.restype = c_void_p

        self.VSL_Error         = lib.VSL_Error
        self.VSL_Error.restype = c_char_p

        self.VSM_Error         = lib.VSM_Error
        self.VSM_Error.restype = c_char_p
        
        self.VSM_Name         = lib.VSM_Name
        self.VSM_Name.restype = c_char_p

        self.VSLQ_New          = lib.VSLQ_New
        self.VSLQ_New.restype  = c_void_p
        self.VSLQ_New.argtypes = [c_void_p, POINTER(c_void_p),c_int,c_char_p]

        self.VSLQ_Delete          = lib.VSLQ_Delete
        self.VSLQ_Delete.argtypes = [POINTER(c_void_p)]

        #self.VSLQ_Dispatch          = lib.VSLQ_Dispatch
        #self.VSLQ_Dispatch.restype  = c_int
        #self.VSLQ_Dispatch.argtypes = (c_void_p, CFUNCTYPE ,c_void_p)
        
        

class VarnishAPI:
    def __init__(self, opt = '', sopath = 'libvarnishapi.so.1'):
        self.lib     = cdll[sopath]
        self.lva     = LIBVARNISHAPI13(self.lib)
        self.defi    = VarnishAPIDefine40()
        self.__cb    = None
        
        VSLTAGS           = c_char_p * 256
        self.VSL_tags     = VSLTAGS.in_dll(self.lib, "VSL_tags")
        
        VSLTAGFLAGS       = c_uint * 256
        self.VSL_tagflags = VSLTAGFLAGS.in_dll(self.lib, "VSL_tagflags")
        
        
        VSLQGROUPING       = c_char_p * 4
        self.VSLQ_grouping = VSLQGROUPING.in_dll(self.lib, "VSLQ_grouping")
        
        self.vsl     = self.lib.VSL_New()
        
        self.vsm     = None
        self.vslq    = None
        self.error   = ''
        self.__d_opt = 0
        self.__g_arg = 0
        self.__q_arg = None
        self.__r_arg = 0
        self.name    = ''
        
        if len(opt)>0:
            self.__Arg(opt)
        
    def __Arg(self, opt):
        opts, args = getopt.getopt(opt,"bcCdx:X:r:q:N:n:I:i:g:")
        error = 0
        for o in opts:
            op  = o[0].lstrip('-')
            arg = o[1]
            if   op == "d":
                #先頭から
                self.__d_opt = 1
            elif op == "g":
                #グルーピング指定
                self.__g_arg =  self.lib.VSLQ_Name2Grouping(arg, -1)
                if   self.__g_arg == -2:
                    error = "Ambiguous grouping type: %s" % (arg)
                    break
                elif self.__g_arg < 0:
                    error = "Unknown grouping type: %s" % (arg)
                    break
            elif op == "n":
                #インスタンス指定
                if not self.vsm:
                    self.vsm = self.lib.VSM_New()
                if self.lib.VSM_n_Arg(self.vsm, arg) <= 0:
                    error = "%s" % self.lib.VSM_Error(self.vsm)
                    break
            elif op == "N":
                #VSMファイル指定
                if not self.vsm:
                    self.vsm = self.lib.VSM_New()
                if self.lib.VSM_N_Arg(self.vsm, arg) <= 0:
                    error = "%s" % self.lib.VSM_Error(self.vsm)
                    break
                self.__d_opt = 1
            #elif op == "P":
            #    #PID指定は対応しない
            elif op == "q":
                #VSL-query
                self.__q_arg = arg
            elif op == "r":
                #バイナリファイル
                self.__r_arg = arg
            else:
                #default
                i = self.VSL_Arg(op, arg);
                if i < 0:
                    error = "%s" % self.lib.VSL_Error(self.vsl)
                    break
        #Check
        if self.__r_arg and self.vsm:
            error = "Can't have both -n and -r options"
        
        if error:
            self.error = error
            return(0)
        return(1)
        
    def Setup(self):
        if self.__r_arg:
            c = self.lva.VSL_CursorFile(self.vsl, self.__r_arg, 0);
        else:
            if not self.vsm:
                self.vsm = self.lib.VSM_New()
            if self.lib.VSM_Open(self.vsm):
                self.error = "Can't open VSM file (%s)" % self.VSM_Error(self.vsm)
                return(0)
            self.name = self.lva.VSM_Name(self.vsm)

            c = self.lva.VSL_CursorVSM(self.vsl, self.vsm,
                (self.defi.VSL_COPT_TAILSTOP if self.__d_opt else self.defi.VSL_COPT_TAIL) | self.defi.VSL_COPT_BATCH
                )
            
        if not c:
            self.error = "Can't open log (%s)" % self.lva.VSL_Error(self.vsl)
            print self.error
            return(0)
        #query
        z = cast(c,c_void_p)
        self.vslq = self.lva.VSLQ_New(self.vsl,z, self.__g_arg, self.__q_arg);
        if not self.vslq:
            self.error = "Query expression error:\n%s" % self.lib.VSL_Error(self.vsl)
            return(0)
        
        return(1)
        
    def __cbMain(self,cb):
        self.__cb = cb
        if not self.vslq:
            if self.lib.VSM_Open(self.vsm):
                self.lib.VSM_ResetError(self.vsm)
                return(1)
            c = self.lva.VSL_CursorVSM(self.vsl, self.vsm,self.defi.VSL_COPT_TAIL | self.defi.VSL_COPT_BATCH);
            if not c:
                self.lib.VSM_ResetError(self.vsm)
                self.lib.VSM_Close(self.vsm)
                return(1)
            self.vslq = self.lva.VSLQ_New(self.vsl, POINTER(c), self.__g_arg, self.__q_arg);
            self.error = 'Log reacquired'
        i = self.lib.VSLQ_Dispatch(self.vslq, VSLQ_dispatch_f(self.__callBack), None);
        return(i)
    
    #old func
    def VSL_NonBlockingDispatch(self, cb):
        self.DispatchSingle(cb)

    def DispatchSingle(self,cb):
        i = self.__cbMain(cb)
        if i > -2:
            return i
        if not self.vsm:
            return i
        
        self.lib.VSLQ_Flush(self.vslq, VSLQ_dispatch_f(self.__callBack), None);
        self.lva.VSLQ_Delete(byref(cast(self.vslq,c_void_p)))
        self.vslq = None
        if i == -2:
            self.error = "Log abandoned"
            self.lib.VSM_Close(self.vsm)
        if i < -2:
            self.error = "Log overrun"
        return i
        
    def DispatchMulti(self,cb):
        while 1:
            i = self.DispatchSingle(cb)
            if i==0:
                return(i)

        
    def Fini(self):
        if self.vslq:
            self.lva.VSLQ_Delete(byref(cast(self.vslq,c_void_p)))
            self.vslq = 0
        if self.vsl:
            self.lib.VSL_Delete(self.vsl)
            self.vsl = 0
        if self.vsm:
            self.lib.VSM_Delete(self.vsm)
            self.vsm = 0
    


    def VSL_Arg(self, opt, arg = '\0'):
        return self.lib.VSL_Arg(self.vsl, ord(opt), arg)

    def VSLQ_Name2Grouping(self, arg):
        return self.lib.VSLQ_Name2Grouping(arg, -1)
    
    def __callBack(self,vsl, pt, fo):
        i = -1
        while 1:
            i=i+1
            t = pt[i]
            if not bool(t):
                break
            tra=t[0]
            c  =tra.c[0]
            
            if vsl[0].c_opt or vsl[0].b_opt:
                if   tra.type == self.defi.VSL_t_req and not vsl[0].c_opt:
                    continue
                elif tra.type == self.defi.VSL_t_bereq and not vsl[0].b_opt:
                    continue
                elif tra.type != self.defi.VSL_t_raw:
                    continue
            
            while 1:
                i = self.lib.VSL_Next(tra.c);
                if i < 0:
                    return (i)
                if i == 0:
                    break
                if not self.lib.VSL_Match(self.vsl, tra.c):
                    continue
                
                #decode vxid type ...
                length =c.rec.ptr[0] & 0xffff
                vxid   =c.rec.ptr[1] & (~(3<<30))
                data   =string_at(c.rec.ptr,length + 8)[8:]
                tag    =c.rec.ptr[0] >> 24
                if c.rec.ptr[1] &(1<< 30):
                    type = 'c'
                elif c.rec.ptr[1] &(1<< 31):
                    type = 'b'
                else:
                    type = '-'
                isbin = self.VSL_tagflags[tag] & self.defi.SLT_F_BINARY
                if self.__cb:
                    self.__cb(self,vxid,tag,type,data,isbin,length)
                #print "vxid:%d tag:%d type:%s data:%s (len=%d)" % (vxid,tag,type,data,length)
        return(0)
