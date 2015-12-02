splices = dict()
drivers= dict()
# table by file type
for i in ['cxx','c','f90','java','python','f77','hxx','h','mod', 'extensions']:
    splices[i] = dict()
    drivers[i] = dict()

from cxxfrag import *

drivers['extensions']['cxx'] = ('cxx', None)
drivers['extensions']['c'] = ('c', None)
drivers['extensions']['f90'] = ('f90', None)
drivers['extensions']['python'] = ('py', None)
drivers['extensions']['java'] = ('java', None)

splices['extensions']['cxx'] = ('cxx', 'hxx')
splices['extensions']['c'] = ('c', 'h')
splices['extensions']['f90'] = ('f90', 'mod')
splices['extensions']['f77'] = ('f', None)
splices['extensions']['python'] = ('py', None)
splices['extensions']['java'] = ('java', None)

splices['cxx']["BabelMain"] = pkg_BabelMain_Impl_cxx
splices['cxx']["ComponentClassDescription"]= pkg_ComponentClassDescription_Impl_cxx
splices['cxx']["Exception"]= pkg_Exception_Impl_cxx
splices['cxx']["PrivateRepository"]= pkg_PrivateRepository_Impl_cxx
splices['cxx']["StringMap"]= pkg_StringMap_Impl_cxx

splices['hxx']["BabelMain"] = pkg_BabelMain_Impl_hxx
splices['hxx']["StringMap"]= pkg_StringMap_Impl_hxx
splices['hxx']["ComponentClassDescription"]= pkg_ComponentClassDescription_Impl_hxx
splices['hxx']["PrivateRepository"]= pkg_PrivateRepository_Impl_hxx
splices['hxx']["Exception"]= pkg_Exception_Impl_hxx

drivers['cxx']["genmain.cxx"] = driver_cxx

# repeat for cfrag, pyfrag, f90frag, javafrag
