# Kage Park
import json as _json
import pickle
#import inspect
from sys import modules
from distutils.spawn import find_executable
from klib.MODULE import *
MODULE().Import('from klib.IP import IP')
MODULE().Import('from klib.Misc import *') # import kmisc(file)'s each function to local module's function
MODULE().Import('from klib.Type import Type')
MODULE().Import('from klib.MAC import MAC')
MODULE().Import('from klib.GET import GET')

class IS:
    def __init__(self,src=None,**opts):
        self.src=src
        self.rtd=opts.get('rtd',{'GOOD':[True,'True','Good','Ok','Pass',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'}],'NONE':[None,'None','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Error',{'ERR'}],'WARN':['Warn',{'WAR'}],'UNKN':['Unknown','UNKN',{'UNK'}],'JUMP':['Jump',{'JUMP'}]})

    def Py2(self):
        if py_version[0] < 3:
            return True
        return False

    def Py3(self):
        if py_version[0] >= 3:
            return True
        return False

    def Int(self):
        try:
            int(self.src)
            return True
        except:
            return False

    def Ipv4(self):
        return IP(self.src).IsV4()

    def Mac4(self,**opts):
        return MAC(self.src).IsV4()

    def Ip_with_port(self,port,**opts):
        return IP(self.src).WithPort(port,**opts)

    def File(self):
        if isinstance(self.src,str): return os.path.isfile(self.src)
        return False

    def Dir(self):
        if isinstance(self.src,str): return os.path.isdir(self.src)
        return False

    def Xml(self):
        firstLine=file_rw(self.src,out='string',read='firstline')
        if firstLine is False:
            filename_str=_u_byte2str(self.src)
            if isinstance(filename_str,str):
                firstLine=filename_str.split('\n')[0]
        if isinstance(firstLine,str) and firstLine.split(' ')[0] == '<?xml': return True
        return False

    def Json(self):
        try:
            _json.loads(self.src)
            return True
        except:
            return False

    def Pickle(self):
        if isinstance(self.src,str) and os.path.isfile(self.src):
            try:
                with open(self.src,'rb') as f: # Pickle Type
                    pickle.load(f)
                    return True
            except:
                pass
        return False

    def Matrix(self,**opts):
        default=opts.get('default',False)
        if isinstance(self.src,(tuple,list)) and len(self.src) >= 1:
            if isinstance(self.src[0],(tuple,list)): # |a,b,c|
                first_ln=len(self.src[0])            # |d,e,f|
                for ii in self.src[1:]:
                    if isinstance(ii,(tuple,list)) and len(ii) == first_ln: continue
                    return False
                return True
            else: # |a,b,c,d|
                first_typ=type(self.src[0])
                for ii in self.src[1:]:
                    if type(ii) != first_type: return False
                return True
        return default

    def Lost_network(self,**opts):
        return IP(self.src).LostNetwork(**opts)

    def Comback_network(self,**opts):
        return IP(self.src).Online(**opts)

    def Rc(self,chk='_'):
        def trans(irt):
            type_irt=type(irt)
            for ii in rtd:
                for jj in rtd[ii]:
                    if type(jj) == type_irt and ((type_irt is str and jj.lower() == irt.lower()) or jj == irt):
                        return ii
            return 'UNKN'
        rtc=Get(self.src,'0|rc',out='raw',err='ignore',check=(list,tuple,dict))
        nrtc=trans(rtc)
        if chk != '_':
            if trans(chk) == nrtc:
                return True
            return False
        return nrtc

    def Cancel(self,func=None):
        if func is None:
            func=self.src
        ttt=type(func).__name__
        if ttt in ['function','instancemethod','method']:
            if func():
                return True
        elif ttt in ['bool','str'] and func in [True,'cancel']:
            return True
        return False

    def Window(self):
        return False

    def Android(self):
        return False

    def IOS(self):
        return False

    def Centos(self):
        return False

    def Unbuntu(self):
        return False

    def Suse(self):
        return False

    def Linux(self):
        if self.centos() or self.ubuntu() or self.suse(): return True
        return False

    def Function(self,obj=None,default=False):
        if Type(self.src,'function'): return True
        if obj is None:
            obj=sys.modules.get('__name__',default)
        elif isinstance(obj,str):
            obj=sys.modules.get(obj,default)
        if obj == default: return default
        if Type(obj,'Class','module'):
            if GET(obj).FuncList().get(self.src,default) == default: return default
            return True
            #return vars(obj).get(self.src,default)
        return default

    def Var(self,obj=None,default=False):
        if obj is None:
            obj=sys.modules.get('__main__',default)
        elif isinstance(obj,str):
            obj=sys.modules.get(obj,default)
        if obj == default: return default
        if Type(obj,'class','function','instance'):
            ARGS=GET(obj).Args()
            for tt in ARGS:
                if self.src in ARGS[tt]: return True 
        else:
            get_var=dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"].get(self.src,'_#_')
            if get_var != '_#_':
                if not Type(get_var,'module','class','function'): return True
#        if hasattr(obj,self.src):
#            return True
        return False

    def Exec(self):
        if isinstance(self.src,str):
            if find_executable(self.src):
                return True
        return False

    def Bin(self):
        return self.Exec()
