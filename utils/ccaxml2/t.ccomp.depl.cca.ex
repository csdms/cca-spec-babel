<?xml version="1.0" ?>
<libInfo>
    <!-- # generated index. -->
    <!--  -->
    <classDeployment name="t.ccomp" paletteAlias="t.ccomp" uniqueID="fixmeuuid">
        <sidlBaseSymbols>
            gov.cca.ComponentRelease, t.bcomp, gov.cca.Component
        </sidlBaseSymbols>
        <sidlOtherSymbols>
            t.type1, t.ptype, t.type2, t.type4
        </sidlOtherSymbols>
        <client_c>
            <include>
                /home/baallan/work/sc04/install/ccafe10/include
            </include>
            <libtool>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-c.la
            </libtool>
            <static>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-c.a
            </static>
            <shared>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-c.so
            </shared>
        </client_c>
        <client_cxx>
            <include>
                /home/baallan/work/sc04/install/ccafe10/include
            </include>
            <libtool>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-cxx.la
            </libtool>
            <static>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-cxx.a
            </static>
            <shared>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-cxx.so
            </shared>
        </client_cxx>
        <client_f77 unsupported="true"/>
        <client_f90>
            <include>
                /home/baallan/work/sc04/install/ccafe10/include
            </include>
            <libtool>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f90.la
            </libtool>
            <static>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f90.a
            </static>
            <shared>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f90.so
            </shared>
        </client_f90>
        <client_java>
            <classpath>
                /home/baallan/work/sc04/install/ccafe10/java
            </classpath>
        </client_java>
        <client_python>
            <pythonpath>
                /home/baallan/work/sc04/install/ccafe10/python2.5/site-packages
            </pythonpath>
        </client_python>
        <server language="c">
            <include>
                /home/baallan/work/sc04/install/ccafe10/include
            </include>
            <libtool>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp.la
            </libtool>
            <static>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp.a
            </static>
            <shared>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp.so
            </shared>
            <sharedDependenciesFlags>
                -L/home/ben/pvm/lib -lpvm -Wl,-rpath,/home/ben/pvm/lib
            </sharedDependenciesFlags>
            <staticDependenciesFlags>
                /home/ben/pvm/lib/libpvm.a
            </staticDependenciesFlags>
            <libtoolDependenciesFlags>
                /home/ben/pvm/lib/libpvm.la
            </libtoolDependenciesFlags>
        </server>
        <ports>
            <provides name="name3" type="t.type1"/>
            <provides name="name4" type="t.type4"/>
            <uses name="name1" type="t.type1"/>
            <uses name="name2" type="t.type2"/>
        </ports>
    </classDeployment>
    <classDeployment name="t.jcomp" paletteAlias="t.jcomp" uniqueID="fixmeuuid">
        <sidlBaseSymbols>
            gov.cca.ComponentRelease, t.bcomp, gov.cca.Component
        </sidlBaseSymbols>
        <sidlOtherSymbols>
            t.type1, t.ptype, t.type2, t.type4
        </sidlOtherSymbols>
        <client_c>
            <include>
                /home/baallan/work/sc04/install/ccafe10/include
            </include>
            <libtool>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-c.la
            </libtool>
            <static>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-c.a
            </static>
            <shared>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-c.so
            </shared>
        </client_c>
        <client_cxx>
            <include>
                /home/baallan/work/sc04/install/ccafe10/include
            </include>
            <libtool>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-cxx.la
            </libtool>
            <static>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-cxx.a
            </static>
            <shared>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-cxx.so
            </shared>
        </client_cxx>
        <client_f77>
            <include>
                /home/baallan/work/sc04/install/ccafe10/include
            </include>
            <libtool>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f77.la
            </libtool>
            <static>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f77.a
            </static>
            <shared>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f77.so
            </shared>
        </client_f77>
        <client_f90>
            <include>
                /home/baallan/work/sc04/install/ccafe10/include
            </include>
            <libtool>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f90.la
            </libtool>
            <static>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f90.a
            </static>
            <shared>
                /home/baallan/work/sc04/install/ccafe10/libt.ccomp-f90.so
            </shared>
        </client_f90>
        <client_java>
            <classpath>
                /home/baallan/work/sc04/install/ccafe10/java
            </classpath>
        </client_java>
        <client_python>
            <pythonpath>
                /home/baallan/work/sc04/install/ccafe10/python2.5/site-packages
            </pythonpath>
        </client_python>
        <server language="java">
            <classpath>
                /home/baallan/work/sc04/install/ccafe10/java
            </classpath>
        </server>
        <ports>
            <provides name="name3" type="t.type1"/>
            <provides name="name4" type="t.type4">
                <property name="joe" type="String">
                    text
                </property>
                <property name="fred" type="Int">
                    1
                </property>
            </provides>
            <uses name="name2" type="t.type2"/>
            <uses name="name1" type="t.type1">
                <property name="joe" type="String">
                    text
                </property>
                <property name="fred" type="Int">
                    1
                </property>
            </uses>
        </ports>
    </classDeployment>
</libInfo>
