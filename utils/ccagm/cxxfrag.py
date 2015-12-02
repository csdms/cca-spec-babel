#
# all the strings defined in this package make sense (enough for a splicer)
# if UBPKG is replaced with the underbar form of some package name (no trailing _)
# andif DCOLPKG is replaced with the :: form of the name.
# andif DOTPKG is replaced with the dotted form of the name.
# Note that this can get slightly out of date wrt babel because
# all we really care about is the splicer blocks.
# It's just easier to create this file by importing full code from running example
# and doing sed than to manage splicers-only.

pkg_BabelMain_Impl_cxx="""
// 
// File:          UBPKG_BabelMain_Impl.cxx
// Symbol:        DOTPKG.BabelMain-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.BabelMain
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "UBPKG_BabelMain_Impl.hxx"

// 
// Includes for all method dependencies.
// 
#ifndef included_gov_cca_AbstractFramework_hxx
#include "gov_cca_AbstractFramework.hxx"
#endif
#ifndef included_gov_cca_ComponentID_hxx
#include "gov_cca_ComponentID.hxx"
#endif
#ifndef included_gov_cca_Services_hxx
#include "gov_cca_Services.hxx"
#endif
#ifndef included_gov_cca_ports_BuilderService_hxx
#include "gov_cca_ports_BuilderService.hxx"
#endif
#ifndef included_UBPKG_StringMap_hxx
#include "UBPKG_StringMap.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_NotImplementedException_hxx
#include "sidl_NotImplementedException.hxx"
#endif

// DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._includes)
// Put additional includes or other arbitrary code here...
#define WHINE(s) \
gov::cca::CCAException gex; \
 DCOLPKG::Exception ex = DCOLPKG::Exception::_create(); \
 ex.setNote(s); \
 gex = ex; \
 throw gex

#define WHINE2(t,s) \
gov::cca::CCAException gex; \
 DCOLPKG::Exception ex = DCOLPKG::Exception::_create(); \
 ex.setNote(s); \
 ex.setType(t); \
 gex = ex; \
 throw gex

#include "gov_cca.hxx"
#include "gov_cca_ports.hxx"
#include "UBPKG.hxx"
#include <iostream>


/** For keys in both tm and values, copy values to tm in the
appropriate format.
*/
void
DCOLPKG::BabelMain_impl::setParamsFromString(gov::cca::TypeMap & tm, std::map< std::string, std::string > & values)
{
	std::map< std::string, std::string >::const_iterator it;
	std::string key;
	std::string val;
	gov::cca::Type dt;
	for ( it = values.begin(); it != values.end(); ++it ){
            	key =  it->first;
		val = it->second;
		dt = tm.typeOf(key);
		if (dt != gov::cca::Type_NoType) {
			transformString(key, dt, val, tm);
		}
	}
}

//====================== stuff stolen from ccaffeine ================
#if 0
#define REFIX(x,y) if (typeName == y)  return gov::cca::Type_##x
::gov::cca::Type 
DCOLPKG::BabelMain_impl::typeFromString( const ::std::string &typeName)
{
	REFIX(NoType,"NoType");
	REFIX(Int,"Int");
	REFIX(Long,"Long");
	REFIX(Float,"Float");
	REFIX(Double,"Double");
	REFIX(Dcomplex,"Dcomplex");
	REFIX(Fcomplex,"Fcomplex");
	REFIX(Bool,"Bool");
	REFIX(String,"String");
	REFIX(IntArray,"IntArray");
	REFIX(LongArray,"LongArray");
	REFIX(FloatArray,"FloatArray");
	REFIX(DoubleArray,"DoubleArray");
	REFIX(DcomplexArray,"DcomplexArray");
	REFIX(FcomplexArray,"FcomplexArray");
	REFIX(BoolArray,"BoolArray");
	REFIX(StringArray,"StringArray");
	return gov::cca::NoType;
}
#undef REFIX
#endif
/** key, tm, the destination info. dt, the required type.
 * v, the value to parse into type dt. 
*/
void DCOLPKG::BabelMain_impl::transformString(const ::std::string & key,
		::gov::cca::Type dt,
		const ::std::string & v, ::gov::cca::TypeMap & tm)
{
	// fixme. try parsing string v to type dt and put it in tm
	// at present this has the effect of dropping the string onthe floor
	// if the parse is not supported.
	if (!tm) { return; }
	::std::istringstream ist(v);
#define UNSTRINGVAL(FTYPE,PRIM) \
    case ::gov::cca::Type_##FTYPE: \
    { PRIM val = 0; \
      ist >> val; \
      tm.put##FTYPE(key, val); \
    } \
    return 
	switch(dt) 
	{
	case ::gov::cca::Type_String: 
		tm.putString(key, v); 
		return;
	UNSTRINGVAL(Int, int32_t);
	UNSTRINGVAL(Long,  int64_t);
	UNSTRINGVAL(Double, double);
	UNSTRINGVAL(Float, float);
	UNSTRINGVAL(Bool, bool);
	UNSTRINGVAL(Dcomplex, ::std::complex<double> );
	UNSTRINGVAL(Fcomplex, ::std::complex<float> );
	case ::gov::cca::Type_NoType: return ;
	case ::gov::cca::Type_IntArray:
	case ::gov::cca::Type_LongArray:
	case ::gov::cca::Type_FloatArray:
	case ::gov::cca::Type_DoubleArray:
	case ::gov::cca::Type_DcomplexArray:
	case ::gov::cca::Type_FcomplexArray:
	case ::gov::cca::Type_BoolArray: 
	case ::gov::cca::Type_StringArray:
	// fixme whine here.
	default:
		return;
	}
#undef UNSTRINGVAL
}

#if 0
int DCOLPKG::BabelMain_impl::putValueByStrings( ::gov::cca::TypeMap t, const ::std::string & key, const ::std::string &vtype, const ::std::string & val)
{
	if (!t || key.size() == 0) { return -1; }
	::gov::cca::Type kt = typeFromString(vtype); 
	if (kt ==  ::gov::cca::Type_NoType) { return -1; }
	try {
		DCOLPKG::BabelMain_impl::transformString( key, kt, val, t);
		return 0;
	}
	catch ( std::exception &e )
	{
		return -1;
	}

}

//---------------------------------------------------------- 
const ::std::string 
DCOLPKG::BabelMain_impl::typeToName( ::gov::cca::Type t) { 
	switch(t) 
	{
		case ::gov::cca::Type_NoType: return "NoType"; 
		case ::gov::cca::Type_Int: return "Int"; 
		case ::gov::cca::Type_Long: return "Long"; 
		case ::gov::cca::Type_Float: return "Float"; 
		case ::gov::cca::Type_Double: return "Double"; 
		case ::gov::cca::Type_Dcomplex: return "Dcomplex"; 
		case ::gov::cca::Type_Fcomplex: return "Fcomplex"; 
		case ::gov::cca::Type_Bool: return "Bool"; 
		case ::gov::cca::Type_String: return "String"; 

		case ::gov::cca::Type_IntArray: return "IntArray"; 
		case ::gov::cca::Type_LongArray: return "LongArray"; 
		case ::gov::cca::Type_FloatArray: return "FloatArray"; 
		case ::gov::cca::Type_DoubleArray: return "DoubleArray"; 
		case ::gov::cca::Type_DcomplexArray: return "DcomplexArray"; 
		case ::gov::cca::Type_FcomplexArray: return "FcomplexArray"; 
		case ::gov::cca::Type_BoolArray: return "BoolArray"; 
		case ::gov::cca::Type_StringArray: return "StringArray"; 
		default: return "unknown";
	}
}
//
//
//---------------------------------------------------------- 
//
::std::string 
DCOLPKG::BabelMain_impl::stringType( ::gov::cca::TypeMap t, const ::std::string &key)
{
	if (!t) {
		return "";
	}
	enum ::gov::cca::Type kt = t.typeOf(key);
	return DCOLPKG::BabelMain_impl::typeToName(kt);
}

#endif

//---------------------------------------------------------- 
// there's a nice nonportable way to do this with strstream
#define STRINGVAL(BTYPE, FTYPE, DEFVAL, FMT) \
  case ::gov::cca::Type_##FTYPE: \
    { \
      BTYPE v = t.get##FTYPE(key, DEFVAL); \
      sprintf(buf, FMT, v); \
      s += buf; \
      return s; \
    } \
  break
#undef STRINGVAL
#define STRINGVAL(FTYPE,DEFVAL) \
  case ::gov::cca::Type_##FTYPE: \
    ost << t.get##FTYPE(key, DEFVAL); \
    return ost.str(); \
  break
        
#define ARRAYVAL(FTYPE,VTYPE) \
  case ::gov::cca::Type_##FTYPE##Array: \
  { \
    ::sidl::array< VTYPE > v; \
    v = t.get##FTYPE##Array( key, v ); \
    for (int i = v.lower(0); i <= v.upper(0); i++) \
    { \
      ost << v[i] << " "; \
    } \
    return ost.str(); \
  } \
  break
        
::std::string 
DCOLPKG::BabelMain_impl::stringValue( ::gov::cca::TypeMap t, const ::std::string &key)
{
	::std::string s;
	if (!t) { return s; }
	::std::ostringstream ost;
	enum ::gov::cca::Type kt = t.typeOf(key);
	// char buf[128];
	switch (kt) {
	case ::gov::cca::Type_NoType: return s;
	STRINGVAL(Int,0);
	STRINGVAL(Long, 0);
	STRINGVAL(Double, 0);
	STRINGVAL(Float, 0);
	STRINGVAL(Bool, false);
	STRINGVAL(String, "");
	STRINGVAL(Dcomplex, ::std::complex<double>(0,0) );
	STRINGVAL(Fcomplex, ::std::complex<float>(0,0) );
	ARRAYVAL(Int, int32_t);
	ARRAYVAL(Long, int64_t);
	ARRAYVAL(Double, double);
	ARRAYVAL(Float, float);
	ARRAYVAL(Bool, bool);
	ARRAYVAL(String, ::std::string );
	ARRAYVAL(Dcomplex, ::std::complex<double> );
	ARRAYVAL(Fcomplex, ::std::complex<float> );
	default:
		return s;
	}
}
#undef STRINGVAL
#undef ARRAYVAL


#if 0

void 
DCOLPKG::BabelMain_impl::dumpTypeMapStdout(::gov::cca::TypeMap t)
{
	std::vector< std::string > keys = t.getAllKeys( ::gov::cca::Type_NoType );
	std::sort(keys.begin(), keys.end());
	for (size_t i = 0; i < keys.size(); i++) {
		::std::cout << "["<< keys[i] << "](" <<
		       	DCOLPKG::BabelMain_impl::stringType(t,keys[i]) << ") " <<
			DCOLPKG::BabelMain_impl::stringValue(t,keys[i]) << std::endl;
	}
}
#endif 

// DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._includes)


// speical constructor, used for data wrapping(required).  Do not put code here unless you really know what you're doing!
DCOLPKG::BabelMain_impl::BabelMain_impl() : StubBase(
  reinterpret_cast< void*>(::DCOLPKG::BabelMain::_wrapObj(
  reinterpret_cast< void*>(this))),false) , _wrapped(true){ 

  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._ctor2)
  // Insert-Code-Here {DOTPKG.BabelMain._ctor2} (ctor2)
  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._ctor2)

}

// user defined constructor
void DCOLPKG::BabelMain_impl::_ctor() {

  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._ctor)
  // add construction details here
  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._ctor)

}

// user defined destructor
void DCOLPKG::BabelMain_impl::_dtor() {

  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._dtor)
  // add destruction details here
  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._dtor)

}

// static class initializer
void DCOLPKG::BabelMain_impl::_load() {

  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._load)
  // Insert-Code-Here {DOTPKG.BabelMain._load} (class initialization)
  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._load)

}

// user defined static methods: (none)

// user defined non-static methods:
/**
 * Method:  invokeGo[]
 */
int32_t
DCOLPKG::BabelMain_impl::invokeGo_impl (
  /* in */const ::std::string& component,
  /* in */const ::std::string& port,
  /* in */::gov::cca::ComponentID c,
  /* in */::gov::cca::Services services,
  /* in */::gov::cca::ports::BuilderService bs ) 
{

  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain.invokeGo)

        std::string pname = component;
        pname += "_";
        pname += port;
        gov::cca::Port p_go;
	gov::cca::TypeMap dummy;
        services.registerUsesPort(pname, "gov.cca.ports.GoPort",dummy);
        gov::cca::ComponentID myself = services.getComponentID();
        gov::cca::ConnectionID goConn = bs.connect(myself, pname, c, port);
        p_go = services.getPort(pname); 
        gov::cca::ports::GoPort go = ::babel_cast< gov::cca::ports::GoPort >(p_go);
        if (go._is_nil() ) {
                WHINE2( gov::cca::CCAExceptionType_BadPortType, "Port is not of expected type GoPort.") ;
        }
        int result;
        result = go.go();
        if (result != 0) {
                std::cerr << pname <<" returned error code: " << result << std::endl;
        }
        services.releasePort(pname);
        bs.disconnect(goConn, 0.0);
        services.unregisterUsesPort(pname);
	return result;
  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain.invokeGo)

}

/**
 *  This function handles the configuring of 
 * parameters when all we know is the
 * info available from a ccaffeine script (which hides 
 * parameter and port types).
 * If component port and config information were 
 * ubiquitous at code generation time, this wouldn't be needed.
 * @param compName name of the component being configured.
 * @param port name of the port being configured.
 * @param comp ComponentID of the component being configured.
 * @param bs BuilderService controlling the frame.
 * @param services Services of the component/driver 
 * doing the parameter setting.
 * @param values  map of keys and values to assign.
 */
void
DCOLPKG::BabelMain_impl::setParameters_impl (
  /* in */const ::std::string& component,
  /* in */const ::std::string& port,
  /* in */::gov::cca::ComponentID c,
  /* in */::gov::cca::ports::BuilderService bs,
  /* in */::gov::cca::Services services,
  /* in */::DCOLPKG::StringMap sm ) 
{

  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain.setParameters)
	std::string compName = component;
	gov::cca::ComponentID myself = services.getComponentID();
	gov::cca::TypeMap dummy;
	gov::cca::TypeMap pProps = bs.getPortProperties(c, port);
	std::string portType = pProps.getString("cca.portType", "undefined");
 	gov::cca::Port p_param = 0;
	std::string pname = compName;
	pname += "_";
	pname += port;
	if ( portType == "gov::cca::ports::BasicParameterPort" ||
		portType == "::gov::cca::ports::BasicParameterPort" ||
		// portType == "::ccafeopq::ports::BasicParameterPort" ||
		portType ==  "gov.cca.ports.BasicParameterPort") 
	{
		gov::cca::ports::BasicParameterPort  bpp ;
		services.registerUsesPort(pname, "gov::cca::ports::BasicParameterPort", dummy);
		gov::cca::ConnectionID bppconn =
			bs.connect(myself, pname, c, port);
		p_param = services.getPort(pname);
		bpp = ::babel_cast<gov::cca::ports::BasicParameterPort> (p_param); //CAST
		if (bpp._not_nil()) {
			gov::cca::TypeMap params = bpp.readConfigurationMap();
			std::map< std::string, std::string > & stdsm = 
				*(static_cast< std::map< std::string, std::string > * >(sm.getUnderlyingStdMap())) ;
			setParamsFromString(params, stdsm);
			bpp.writeConfigurationMap(params);
		} else {
			std::string msg = "Port ";
			msg += compName; msg += "."; msg += port;
			msg += " is not of expected type BasicParameterPort (cast fail)";
			WHINE2(gov::cca::CCAExceptionType_BadPortType, msg);
		}
		services.releasePort(pname);
		bs.disconnect(bppconn, 0.0);
		services.unregisterUsesPort(pname);
		return;
	}
	if ( portType == "gov::cca::ports::ParameterPort" ||
		portType == "::gov::cca::ports::ParameterPort" ||
		// portType == "::ccafeopq::ports::ParameterPort" ||
		portType ==  "gov.cca.ports.ParameterPort") 
	{
		gov::cca::ports::ParameterPort  pp;
		services.registerUsesPort(pname, "gov::cca::ports::ParameterPort", dummy);
		gov::cca::ConnectionID ppconn =
			bs.connect(myself, pname, c, port);
		p_param = services.getPort(pname);
		pp = ::babel_cast<gov::cca::ports::ParameterPort> (p_param); //CAST
		if (pp._not_nil() ) {
			gov::cca::TypeMap params = pp.readConfigurationMap();
			std::map< std::string, std::string > & stdsm2 = 
				*(static_cast< std::map< std::string, std::string > * >(sm.getUnderlyingStdMap())) ;
			setParamsFromString(params, stdsm2);
			pp.writeConfigurationMap(params);
		} else {
			std::string msg = "Port ";
			msg += compName; msg += "."; msg += port;
			msg += " is not of expected type ParameterPort (cast fail)";
			WHINE2(gov::cca::CCAExceptionType_BadPortType, msg);
		}
		services.releasePort(pname);
		bs.disconnect(ppconn, 0.0);
		services.unregisterUsesPort(pname);
		return;
	}
	std::string msg = "Port ";
	msg += compName; msg += "."; msg += port;
	msg += " is not a parameter port. seems to be a ";
	msg += portType;
	WHINE2(gov::cca::CCAExceptionType_BadPortType, msg);
  

  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain.setParameters)

}

/**
 *  This function returns a stringified version of a parameter value.
 */
::std::string
DCOLPKG::BabelMain_impl::getParameterValue_impl (
  /* in */::gov::cca::ComponentID c,
  /* in */const ::std::string& portName,
  /* in */const ::std::string& var,
  /* in */::gov::cca::Services services,
  /* in */::gov::cca::ports::BuilderService bs ) 
{

  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain.getParameterValue)
	std::string compName = c.getInstanceName();
	std::string port = portName;

	gov::cca::ComponentID myself = services.getComponentID();
	gov::cca::TypeMap dummy;
	gov::cca::TypeMap pProps = bs.getPortProperties(c, port);
	std::string portType = pProps.getString("cca.portType", "undefined");
 	gov::cca::Port p_param = 0;
	std::string pname = compName;
	pname += "_";
	pname += port;
	std::string result;
	if ( portType == "gov::cca::ports::BasicParameterPort" ||
		portType == "::gov::cca::ports::BasicParameterPort" ||
		// portType == "::ccafeopq::ports::BasicParameterPort" ||
		portType ==  "gov.cca.ports.BasicParameterPort") 
	{
		gov::cca::ports::BasicParameterPort  bpp ;
		services.registerUsesPort(pname, "gov::cca::ports::BasicParameterPort", dummy);
		gov::cca::ConnectionID bppconn =
			bs.connect(myself, pname, c, port);
		p_param = services.getPort(pname);
		bpp = ::babel_cast< gov::cca::ports::BasicParameterPort> (p_param); //CAST
		if (bpp._not_nil()) {
			gov::cca::TypeMap params = bpp.readConfigurationMap();
			result = stringValue(params,var);
		} else {
			std::string msg = "Port ";
			msg += compName; msg += "."; msg += port;
			msg += " is not of expected type BasicParameterPort (cast fail)";
			services.releasePort(pname);
			bs.disconnect(bppconn, 0.0);
			services.unregisterUsesPort(pname);
			WHINE2(gov::cca::CCAExceptionType_BadPortType, msg);
			return result ; // not reached we hope.
		}
		services.releasePort(pname);
		bs.disconnect(bppconn, 0.0);
		services.unregisterUsesPort(pname);
		return result;
	}
	if ( portType == "gov::cca::ports::ParameterPort" ||
		portType == "::gov::cca::ports::ParameterPort" ||
		// portType == "::ccafeopq::ports::ParameterPort" ||
		portType ==  "gov.cca.ports.ParameterPort") 
	{
		gov::cca::ports::ParameterPort  pp;
		services.registerUsesPort(pname, "gov::cca::ports::ParameterPort", dummy);
		gov::cca::ConnectionID ppconn =
			bs.connect(myself, pname, c, port);
		p_param = services.getPort(pname);
		pp = ::babel_cast<gov::cca::ports::ParameterPort> (p_param); //CAST
		if (pp._not_nil() ) {
			gov::cca::TypeMap params = pp.readConfigurationMap();
			result = stringValue(params,var);
		} else {
			std::string msg = "Port ";
			msg += compName; msg += "."; msg += port;
			msg += " is not of expected type ParameterPort (cast fail)";
			services.releasePort(pname);
			bs.disconnect(ppconn, 0.0);
			services.unregisterUsesPort(pname);
			WHINE2(gov::cca::CCAExceptionType_BadPortType, msg);
			return result;  // not reached we hope.
		}
		services.releasePort(pname);
		bs.disconnect(ppconn, 0.0);
		services.unregisterUsesPort(pname);
		return result;
	}
	std::string msg = "Port ";
	msg += compName; msg += "."; msg += port;
	msg += " is not a parameter port. seems to be a ";
	msg += portType;
	WHINE2(gov::cca::CCAExceptionType_BadPortType, msg);
	return result; // notreached we hope
  
  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain.getParameterValue)

}

/**
 * Method:  driverBody[]
 */
void
DCOLPKG::BabelMain_impl::driverBody_impl (
  /* inout */::gov::cca::AbstractFramework& af ) 
{

  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain.driverBody)
	gov::cca::TypeMap dummy;
	dummy = af.createTypeMap();

	gov::cca::ports::BuilderService bs, dummybs;
#if 1 //fixme cxxfrag
	DCOLPKG::PrivateRepository pr;
	pr = DCOLPKG::PrivateRepository::_create();
	pr.initialize();
#endif

	gov::cca::Services services;
	// set the script up as a component in the frame it receives.
	services = af.getServices("UBPKG_BabelMain", "UBPKG_BabelMain", dummy);
	// and find its id tag in the frame.
	gov::cca::ComponentID myself = services.getComponentID();

	// tell the framework about the components that come with the driver.
	// the components from PrivateRepository will now be available from
	// the BuilderService port.
	
#if 1 //fixme cxxfrag
	services.addProvidesPort(pr, "UBPKG_PrivateRepository", "ccaffeine.ports.ComponentFactory", dummy);
#endif

	services.registerUsesPort("bs", "gov.cca.ports.BuilderService", dummy);

	gov::cca::Port dummyp;
	gov::cca::Port p;
	p = services.getPort("bs");
	if ( p._is_nil() ) {
		WHINE("Service port bs is missing!");
	}
	bs = ::babel_cast<gov::cca::ports::BuilderService> (p); // CAST
	if ( bs._is_nil() ) {
		WHINE2(gov::cca::CCAExceptionType_BadPortType, "Service port bs is not of expected type neo::cca::ports::BuilderService");
	}
	// scripted source here

#include "UBPKG_BabelMain.driverBody.guts.hh"

	// end script source
	bs = dummybs;
	p = dummyp;
	services.releasePort("bs");
	services.unregisterUsesPort("bs");
	services.removeProvidesPort("UBPKG_PrivateRepository");
	// remove ourselves from the frame.
	af.releaseServices(services);


  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain.driverBody)

}



// DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._misc)
// Put miscellaneous code here
// DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._misc)

"""

pkg_BabelMain_Impl_hxx="""
// 
// File:          UBPKG_BabelMain_Impl.hxx
// Symbol:        DOTPKG.BabelMain-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.BabelMain
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 

#ifndef included_UBPKG_BabelMain_Impl_hxx
#define included_UBPKG_BabelMain_Impl_hxx

#ifndef included_sidl_cxx_hxx
#include "sidl_cxx.hxx"
#endif
#ifndef included_UBPKG_BabelMain_IOR_h
#include "UBPKG_BabelMain_IOR.h"
#endif
#ifndef included_ccaffeine_BabelMain_hxx
#include "ccaffeine_BabelMain.hxx"
#endif
#ifndef included_gov_cca_AbstractFramework_hxx
#include "gov_cca_AbstractFramework.hxx"
#endif
#ifndef included_gov_cca_ComponentID_hxx
#include "gov_cca_ComponentID.hxx"
#endif
#ifndef included_gov_cca_Services_hxx
#include "gov_cca_Services.hxx"
#endif
#ifndef included_gov_cca_ports_BuilderService_hxx
#include "gov_cca_ports_BuilderService.hxx"
#endif
#ifndef included_UBPKG_BabelMain_hxx
#include "UBPKG_BabelMain.hxx"
#endif
#ifndef included_UBPKG_StringMap_hxx
#include "UBPKG_StringMap.hxx"
#endif
#ifndef included_sidl_BaseClass_hxx
#include "sidl_BaseClass.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif


// DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._includes)
#include <map>
#include <string>
// DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._includes)

namespace mpitest { 
  namespace script { 
    namespace babel { 

      /**
       * Symbol "DOTPKG.BabelMain" (version 0.0)
       */
      class BabelMain_impl : public virtual ::DCOLPKG::BabelMain 
  // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._inherits)
  // Put additional inheritance here...
  // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._inherits)
      {

      // All data marked protected will be accessable by 
      // descendant Impl classes
      protected:

        bool _wrapped;

    // DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._implementation)
    
    /** stl - babel converter */
    void
    setParamsFromString(gov::cca::TypeMap & tm, std::map< std::string, std::string > & values);

    /* not used just yet */
    // ::gov::cca::Type typeFromString( const ::std::string &typeName);
    
    /** set key with type t from string value v on tm */
    void transformString(const ::std::string & key,
			    ::gov::cca::Type dt,
			    const ::std::string & v, ::gov::cca::TypeMap & tm);

    /** get string value for key in t */
    ::std::string stringValue( ::gov::cca::TypeMap t, const ::std::string &key) ;
    

    // DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._implementation)

      public:
        // default constructor, used for data wrapping(required)
        BabelMain_impl();
        // sidl constructor (required)
        // Note: alternate Skel constructor doesn't call addref()
        // (fixes bug #275)
        BabelMain_impl( struct UBPKG_BabelMain__object * s ) : 
          StubBase(s,true), _wrapped(false) { _ctor(); }

        // user defined construction
        void _ctor();

        // virtual destructor (required)
        virtual ~BabelMain_impl() { _dtor(); }

        // user defined destruction
        void _dtor();

        // true if this object was created by a user newing the impl
        inline bool _isWrapped() {return _wrapped;}

        // static class initializer
        static void _load();

      public:

        /**
         * user defined non-static method.
         */
        int32_t
        invokeGo_impl (
          /* in */const ::std::string& component,
          /* in */const ::std::string& port,
          /* in */::gov::cca::ComponentID c,
          /* in */::gov::cca::Services services,
          /* in */::gov::cca::ports::BuilderService bs
        )
        ;


        /**
         *  This function handles the configuring of 
         * parameters when all we know is the
         * info available from a ccaffeine script (which hides 
         * parameter and port types).
         * If component port and config information were 
         * ubiquitous at code generation time, this wouldn't be needed.
         * @param compName name of the component being configured.
         * @param port name of the port being configured.
         * @param comp ComponentID of the component being configured.
         * @param bs BuilderService controlling the frame.
         * @param services Services of the component/driver 
         * doing the parameter setting.
         * @param values  map of keys and values to assign.
         */
        void
        setParameters_impl (
          /* in */const ::std::string& component,
          /* in */const ::std::string& port,
          /* in */::gov::cca::ComponentID c,
          /* in */::gov::cca::ports::BuilderService bs,
          /* in */::gov::cca::Services services,
          /* in */::DCOLPKG::StringMap sm
        )
        ;


        /**
         *  This function returns a stringified version of a parameter value.
         */
        ::std::string
        getParameterValue_impl (
          /* in */::gov::cca::ComponentID c,
          /* in */const ::std::string& portName,
          /* in */const ::std::string& var,
          /* in */::gov::cca::Services services,
          /* in */::gov::cca::ports::BuilderService bs
        )
        ;

        /**
         * user defined non-static method.
         */
        void
        driverBody_impl (
          /* inout */::gov::cca::AbstractFramework& af
        )
        ;

      };  // end class BabelMain_impl

    } // end namespace babel
  } // end namespace script
} // end namespace mpitest

// DO-NOT-DELETE splicer.begin(DOTPKG.BabelMain._misc)
// Put miscellaneous things here...
// DO-NOT-DELETE splicer.end(DOTPKG.BabelMain._misc)

#endif
"""

pkg_ComponentClassDescription_Impl_cxx="""
// 
// File:          UBPKG_ComponentClassDescription_Impl.cxx
// Symbol:        DOTPKG.ComponentClassDescription-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.ComponentClassDescription
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "UBPKG_ComponentClassDescription_Impl.hxx"

// 
// Includes for all method dependencies.
// 
#ifndef included_gov_cca_CCAException_hxx
#include "gov_cca_CCAException.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_RuntimeException_hxx
#include "sidl_RuntimeException.hxx"
#endif
#ifndef included_sidl_NotImplementedException_hxx
#include "sidl_NotImplementedException.hxx"
#endif
// DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._includes)

#define WHINE(s) \
gov::cca::CCAException gex; \
 DCOLPKG::Exception ex = DCOLPKG::Exception::_create(); \
 ex.setNote(s); \
 gex = ex; \
 throw gex


// DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._includes)

// speical constructor, used for data wrapping(required).  Do not put code here unless you really know what you're doing!
DCOLPKG::ComponentClassDescription_impl::ComponentClassDescription_impl
  () : StubBase(reinterpret_cast< void*>(
  ::DCOLPKG::ComponentClassDescription::_wrapObj(
  reinterpret_cast< void*>(this))),false) , _wrapped(true){ 
  // DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._ctor2)
  // Insert-Code-Here {DOTPKG.ComponentClassDescription._ctor2} (ctor2)
  // DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._ctor2)
}

// user defined constructor
void DCOLPKG::ComponentClassDescription_impl::_ctor() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._ctor)
  // add construction details here
  // DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._ctor)
}

// user defined destructor
void DCOLPKG::ComponentClassDescription_impl::_dtor() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._dtor)
  // add destruction details here
  // DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._dtor)
}

// static class initializer
void DCOLPKG::ComponentClassDescription_impl::_load() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._load)
  // Insert-Code-Here {DOTPKG.ComponentClassDescription._load} (class initialization)
  // DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._load)
}

// user defined static methods: (none)

// user defined non-static methods:
/**
 * Method:  initialize[]
 */
void
DCOLPKG::ComponentClassDescription_impl::initialize_impl (
  /* in */const ::std::string& className,
  /* in */const ::std::string& classAlias ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription.initialize)
  cName = className;
  cAlias = classAlias;
  // DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription.initialize)
}

/**
 *  
 * Returns the class name provided in 
 * <code>BuilderService.createInstance()</code>
 * or in
 * <code>AbstractFramework.getServices()</code>.
 * <p>
 * Throws <code>CCAException</code> if <code>ComponentClassDescription</code> is invalid.
 */
::std::string
DCOLPKG::ComponentClassDescription_impl::getComponentClassName_impl
  () 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException

{
  // DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription.getComponentClassName)
  return cName;
  // DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription.getComponentClassName)
}


// DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._misc)
// Put miscellaneous code here
// DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._misc)
"""

pkg_ComponentClassDescription_Impl_hxx="""
// 
// File:          UBPKG_ComponentClassDescription_Impl.hxx
// Symbol:        DOTPKG.ComponentClassDescription-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.ComponentClassDescription
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 

#ifndef included_UBPKG_ComponentClassDescription_Impl_hxx
#define included_UBPKG_ComponentClassDescription_Impl_hxx

#ifndef included_sidl_cxx_hxx
#include "sidl_cxx.hxx"
#endif
#ifndef included_UBPKG_ComponentClassDescription_IOR_h
#include "UBPKG_ComponentClassDescription_IOR.h"
#endif
#ifndef included_gov_cca_CCAException_hxx
#include "gov_cca_CCAException.hxx"
#endif
#ifndef included_gov_cca_ComponentClassDescription_hxx
#include "gov_cca_ComponentClassDescription.hxx"
#endif
#ifndef included_UBPKG_ComponentClassDescription_hxx
#include "UBPKG_ComponentClassDescription.hxx"
#endif
#ifndef included_sidl_BaseClass_hxx
#include "sidl_BaseClass.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_RuntimeException_hxx
#include "sidl_RuntimeException.hxx"
#endif


// DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._includes)
// Put additional includes or other arbitrary code here...
// DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._includes)

namespace mpitest { 
  namespace script { 
    namespace babel { 

      /**
       * Symbol "DOTPKG.ComponentClassDescription" (version 0.0)
       */
      class ComponentClassDescription_impl : public virtual 
        ::DCOLPKG::ComponentClassDescription 
  // DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._inherits)
  // Put additional inheritance here...
  // DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._inherits)
      {

      // All data marked protected will be accessable by 
      // descendant Impl classes
      protected:

        bool _wrapped;

    // DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._implementation)
    std::string cName;
    std::string cAlias;
    // DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._implementation)

      public:
        // default constructor, used for data wrapping(required)
        ComponentClassDescription_impl();
        // sidl constructor (required)
        // Note: alternate Skel constructor doesn't call addref()
        // (fixes bug #275)
        ComponentClassDescription_impl( struct 
          UBPKG_ComponentClassDescription__object * s ) : 
          StubBase(s,true), _wrapped(false) { _ctor(); }

        // user defined construction
        void _ctor();

        // virtual destructor (required)
        virtual ~ComponentClassDescription_impl() { _dtor(); }

        // user defined destruction
        void _dtor();

        // true if this object was created by a user newing the impl
        inline bool _isWrapped() {return _wrapped;}

        // static class initializer
        static void _load();

      public:

        /**
         * user defined non-static method.
         */
        void
        initialize_impl (
          /* in */const ::std::string& className,
          /* in */const ::std::string& classAlias
        )
        ;


        /**
         *  
         * Returns the class name provided in 
         * <code>BuilderService.createInstance()</code>
         * or in
         * <code>AbstractFramework.getServices()</code>.
         * <p>
         * Throws <code>CCAException</code> if <code>ComponentClassDescription</code> is invalid.
         */
        ::std::string
        getComponentClassName_impl() // throws:
        //     ::gov::cca::CCAException
        //     ::sidl::RuntimeException
        ;
      };  // end class ComponentClassDescription_impl

    } // end namespace babel
  } // end namespace script
} // end namespace mpitest

// DO-NOT-DELETE splicer.begin(DOTPKG.ComponentClassDescription._misc)
// Put miscellaneous things here...
// DO-NOT-DELETE splicer.end(DOTPKG.ComponentClassDescription._misc)

#endif
"""

pkg_Exception_Impl_cxx="""
// 
// File:          UBPKG_Exception_Impl.cxx
// Symbol:        DOTPKG.Exception-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.Exception
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "UBPKG_Exception_Impl.hxx"

// 
// Includes for all method dependencies.
// 
#ifndef included_gov_cca_CCAExceptionType_hxx
#include "gov_cca_CCAExceptionType.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_io_Deserializer_hxx
#include "sidl_io_Deserializer.hxx"
#endif
#ifndef included_sidl_io_Serializer_hxx
#include "sidl_io_Serializer.hxx"
#endif
#ifndef included_sidl_NotImplementedException_hxx
#include "sidl_NotImplementedException.hxx"
#endif
// DO-NOT-DELETE splicer.begin(DOTPKG.Exception._includes)
// Put additional includes or other arbitrary code here...
// DO-NOT-DELETE splicer.end(DOTPKG.Exception._includes)

// speical constructor, used for data wrapping(required).  Do not put code here unless you really know what you're doing!
DCOLPKG::Exception_impl::Exception_impl() : StubBase(
  reinterpret_cast< void*>(::DCOLPKG::Exception::_wrapObj(
  reinterpret_cast< void*>(this))),false) , _wrapped(true){ 
  // DO-NOT-DELETE splicer.begin(DOTPKG.Exception._ctor2)
  // Insert-Code-Here {DOTPKG.Exception._ctor2} (ctor2)
  // DO-NOT-DELETE splicer.end(DOTPKG.Exception._ctor2)
}

// user defined constructor
void DCOLPKG::Exception_impl::_ctor() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.Exception._ctor)
  myType = gov::cca::CCAExceptionType_Nonstandard;
  // DO-NOT-DELETE splicer.end(DOTPKG.Exception._ctor)
}

// user defined destructor
void DCOLPKG::Exception_impl::_dtor() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.Exception._dtor)
  // add destruction details here
  // DO-NOT-DELETE splicer.end(DOTPKG.Exception._dtor)
}

// static class initializer
void DCOLPKG::Exception_impl::_load() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.Exception._load)
  // Insert-Code-Here {DOTPKG.Exception._load} (class initialization)
  // DO-NOT-DELETE splicer.end(DOTPKG.Exception._load)
}

// user defined static methods: (none)

// user defined non-static methods:
/**
 * Method:  setType[]
 */
void
DCOLPKG::Exception_impl::setType_impl (
  /* in */::gov::cca::CCAExceptionType t ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.Exception.setType)
  myType = t;
  // DO-NOT-DELETE splicer.end(DOTPKG.Exception.setType)
}

/**
 * Method:  getCCAExceptionType[]
 */
::gov::cca::CCAExceptionType
DCOLPKG::Exception_impl::getCCAExceptionType_impl () 

{
  // DO-NOT-DELETE splicer.begin(DOTPKG.Exception.getCCAExceptionType)
  return myType;
  // DO-NOT-DELETE splicer.end(DOTPKG.Exception.getCCAExceptionType)
}


// DO-NOT-DELETE splicer.begin(DOTPKG.Exception._misc)
// Put miscellaneous code here
// DO-NOT-DELETE splicer.end(DOTPKG.Exception._misc)

"""

pkg_Exception_Impl_hxx="""
// 
// File:          UBPKG_Exception_Impl.hxx
// Symbol:        DOTPKG.Exception-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.Exception
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 

#ifndef included_UBPKG_Exception_Impl_hxx
#define included_UBPKG_Exception_Impl_hxx

#ifndef included_sidl_cxx_hxx
#include "sidl_cxx.hxx"
#endif
#ifndef included_UBPKG_Exception_IOR_h
#include "UBPKG_Exception_IOR.h"
#endif
#ifndef included_gov_cca_CCAException_hxx
#include "gov_cca_CCAException.hxx"
#endif
#ifndef included_gov_cca_CCAExceptionType_hxx
#include "gov_cca_CCAExceptionType.hxx"
#endif
#ifndef included_UBPKG_Exception_hxx
#include "UBPKG_Exception.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_SIDLException_hxx
#include "sidl_SIDLException.hxx"
#endif
#ifndef included_sidl_io_Deserializer_hxx
#include "sidl_io_Deserializer.hxx"
#endif
#ifndef included_sidl_io_Serializer_hxx
#include "sidl_io_Serializer.hxx"
#endif


// DO-NOT-DELETE splicer.begin(DOTPKG.Exception._includes)
// Put additional includes or other arbitrary code here...
// DO-NOT-DELETE splicer.end(DOTPKG.Exception._includes)

namespace mpitest { 
  namespace script { 
    namespace babel { 

      /**
       * Symbol "DOTPKG.Exception" (version 0.0)
       */
      class Exception_impl : public virtual ::DCOLPKG::Exception 
  // DO-NOT-DELETE splicer.begin(DOTPKG.Exception._inherits)
  // Put additional inheritance here...
  // DO-NOT-DELETE splicer.end(DOTPKG.Exception._inherits)
      {

      // All data marked protected will be accessable by 
      // descendant Impl classes
      protected:

        bool _wrapped;

    // DO-NOT-DELETE splicer.begin(DOTPKG.Exception._implementation)
    // Put additional implementation details here...
    ::gov::cca::CCAExceptionType myType;
    // DO-NOT-DELETE splicer.end(DOTPKG.Exception._implementation)

      public:
        // default constructor, used for data wrapping(required)
        Exception_impl();
        // sidl constructor (required)
        // Note: alternate Skel constructor doesn't call addref()
        // (fixes bug #275)
        Exception_impl( struct UBPKG_Exception__object * s ) : 
          StubBase(s,true), _wrapped(false) { _ctor(); }

        // user defined construction
        void _ctor();

        // virtual destructor (required)
        virtual ~Exception_impl() { _dtor(); }

        // user defined destruction
        void _dtor();

        // true if this object was created by a user newing the impl
        inline bool _isWrapped() {return _wrapped;}

        // static class initializer
        static void _load();

      public:

        /**
         * user defined non-static method.
         */
        void
        setType_impl (
          /* in */::gov::cca::CCAExceptionType t
        )
        ;

        /**
         * user defined non-static method.
         */
        ::gov::cca::CCAExceptionType
        getCCAExceptionType_impl() ;
      };  // end class Exception_impl

    } // end namespace babel
  } // end namespace script
} // end namespace mpitest

// DO-NOT-DELETE splicer.begin(DOTPKG.Exception._misc)
// Put miscellaneous things here...
// DO-NOT-DELETE splicer.end(DOTPKG.Exception._misc)

#endif
"""

pkg_PrivateRepository_Impl_cxx="""
// 
// File:          UBPKG_PrivateRepository_Impl.cxx
// Symbol:        DOTPKG.PrivateRepository-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.PrivateRepository
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "UBPKG_PrivateRepository_Impl.hxx"

// 
// Includes for all method dependencies.
// 
#ifndef included_gov_cca_CCAException_hxx
#include "gov_cca_CCAException.hxx"
#endif
#ifndef included_gov_cca_Component_hxx
#include "gov_cca_Component.hxx"
#endif
#ifndef included_gov_cca_ComponentClassDescription_hxx
#include "gov_cca_ComponentClassDescription.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_RuntimeException_hxx
#include "sidl_RuntimeException.hxx"
#endif
#ifndef included_sidl_NotImplementedException_hxx
#include "sidl_NotImplementedException.hxx"
#endif
// DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._includes)
// #include "dc/babel.new/babel-cca/AllBabelCCA.hxx"
#include "UBPKG.hxx"
#include "UBPKG_PrivateRepository._includes.guts.hh" // INC
// DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._includes)

// speical constructor, used for data wrapping(required).  Do not put code here unless you really know what you're doing!
DCOLPKG::PrivateRepository_impl::PrivateRepository_impl() : 
  StubBase(reinterpret_cast< void*>(
  ::DCOLPKG::PrivateRepository::_wrapObj(reinterpret_cast< 
  void*>(this))),false) , _wrapped(true){ 
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._ctor2)
  // Insert-Code-Here {DOTPKG.PrivateRepository._ctor2} (ctor2)
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._ctor2)
}

// user defined constructor
void DCOLPKG::PrivateRepository_impl::_ctor() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._ctor)
// #include "UBPKG_PrivateRepository._ctor.guts.hh" // INC
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._ctor)
}

// user defined destructor
void DCOLPKG::PrivateRepository_impl::_dtor() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._dtor)
  // add destruction details here
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._dtor)
}

// static class initializer
void DCOLPKG::PrivateRepository_impl::_load() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._load)
  // Insert-Code-Here {DOTPKG.PrivateRepository._load} (class initialization)
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._load)
}

// user defined static methods: (none)

// user defined non-static methods:
/**
 * Method:  initialize[]
 */
void
DCOLPKG::PrivateRepository_impl::initialize_impl () 

{
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository.initialize)
 #include "UBPKG_PrivateRepository._ctor.guts.hh" // INC
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository.initialize)
}

/**
 * Method:  addDescription[]
 */
void
DCOLPKG::PrivateRepository_impl::addDescription_impl (
  /* in */const ::std::string& className,
  /* in */const ::std::string& classAlias ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository.addDescription)
	DCOLPKG::ComponentClassDescription cccd;
	cccd = DCOLPKG::ComponentClassDescription::_create();
	cccd.initialize(className, classAlias);
	gov::cca::ComponentClassDescription gcccd = cccd;
	descriptions.push_back(gcccd);
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository.addDescription)
}

/**
 *  
 * Collect the currently obtainable class name strings from
 * factories known to the builder and the from the
 * already instantiated components.
 * @return The list of class description, which may be empty, that are
 * known a priori to contain valid values for the className
 * argument of createInstance. 
 * @throws CCAException in the event of error.
 */
::sidl::array< ::gov::cca::ComponentClassDescription>
DCOLPKG::PrivateRepository_impl::getAvailableComponentClasses_impl
  () 
// throws:
//     ::gov::cca::CCAException
//     ::sidl::RuntimeException

{
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository.getAvailableComponentClasses)
	// this code is the same regardless of the components named
	// in the input bld file.

	size_t nd = descriptions.size();
	::sidl::array< ::gov::cca::ComponentClassDescription> descArray  =
	::sidl::array< ::gov::cca::ComponentClassDescription>::create1d(nd);
	for (size_t i = 0; i < nd; i++) {
		descArray.set(i, descriptions[i]);
	}
	return descArray;

  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository.getAvailableComponentClasses)
}

/**
 *  the component instance returned is nil if the name is unknown
 * to the factory. The component is raw: it has been constructed
 * but not initialized via setServices.
 */
::gov::cca::Component
DCOLPKG::PrivateRepository_impl::createComponentInstance_impl (
  /* in */const ::std::string& className ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository.createComponentInstance)
#include "UBPKG_PrivateRepository.createComponentInstance.guts.hh" //INC
  gov::cca::Component dummy;
  return dummy;
  // the wrangler that handles all factories is supposed to 
  // deal with the nil and maybe convert it to an exception.
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository.createComponentInstance)
}

/**
 *  reclaim any resources the factory may have associated with
 * the port it is using. This will occur after the
 * normal component shutdown  (ala componentrelease) is finished. 
 */
void
DCOLPKG::PrivateRepository_impl::destroyComponentInstance_impl (
  /* in */const ::std::string& className,
  /* in */::gov::cca::Component c ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository.destroyComponentInstance)
  // do nothing
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository.destroyComponentInstance)
}


// DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._misc)
#if 0
  ::gov::cca::TypeMap props;
  return self.createComponentInstance(className, props);
#endif
// DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._misc)
"""

pkg_PrivateRepository_Impl_hxx="""
// 
// File:          UBPKG_PrivateRepository_Impl.hxx
// Symbol:        DOTPKG.PrivateRepository-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.PrivateRepository
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 

#ifndef included_UBPKG_PrivateRepository_Impl_hxx
#define included_UBPKG_PrivateRepository_Impl_hxx

#ifndef included_sidl_cxx_hxx
#include "sidl_cxx.hxx"
#endif
#ifndef included_UBPKG_PrivateRepository_IOR_h
#include "UBPKG_PrivateRepository_IOR.h"
#endif
#ifndef included_ccaffeine_ports_ComponentFactory_hxx
#include "ccaffeine_ports_ComponentFactory.hxx"
#endif
#ifndef included_gov_cca_CCAException_hxx
#include "gov_cca_CCAException.hxx"
#endif
#ifndef included_gov_cca_Component_hxx
#include "gov_cca_Component.hxx"
#endif
#ifndef included_gov_cca_ComponentClassDescription_hxx
#include "gov_cca_ComponentClassDescription.hxx"
#endif
#ifndef included_gov_cca_ports_ComponentRepository_hxx
#include "gov_cca_ports_ComponentRepository.hxx"
#endif
#ifndef included_UBPKG_PrivateRepository_hxx
#include "UBPKG_PrivateRepository.hxx"
#endif
#ifndef included_sidl_BaseClass_hxx
#include "sidl_BaseClass.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_RuntimeException_hxx
#include "sidl_RuntimeException.hxx"
#endif


// DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._includes)
// Put additional includes or other arbitrary code here...
// DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._includes)

namespace mpitest { 
  namespace script { 
    namespace babel { 

      /**
       * Symbol "DOTPKG.PrivateRepository" (version 0.0)
       */
      class PrivateRepository_impl : public virtual 
        ::DCOLPKG::PrivateRepository 
  // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._inherits)
  // Put additional inheritance here...
  // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._inherits)
      {

      // All data marked protected will be accessable by 
      // descendant Impl classes
      protected:

        bool _wrapped;

    // DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._implementation)
    
	std::vector< gov::cca::ComponentClassDescription > descriptions;

    // DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._implementation)

      public:
        // default constructor, used for data wrapping(required)
        PrivateRepository_impl();
        // sidl constructor (required)
        // Note: alternate Skel constructor doesn't call addref()
        // (fixes bug #275)
        PrivateRepository_impl( struct 
          UBPKG_PrivateRepository__object * s ) : StubBase(s,
          true), _wrapped(false) { _ctor(); }

        // user defined construction
        void _ctor();

        // virtual destructor (required)
        virtual ~PrivateRepository_impl() { _dtor(); }

        // user defined destruction
        void _dtor();

        // true if this object was created by a user newing the impl
        inline bool _isWrapped() {return _wrapped;}

        // static class initializer
        static void _load();

      public:

        /**
         * user defined non-static method.
         */
        void
        initialize_impl() ;
        /**
         * user defined non-static method.
         */
        void
        addDescription_impl (
          /* in */const ::std::string& className,
          /* in */const ::std::string& classAlias
        )
        ;


        /**
         *  
         * Collect the currently obtainable class name strings from
         * factories known to the builder and the from the
         * already instantiated components.
         * @return The list of class description, which may be empty, that are
         * known a priori to contain valid values for the className
         * argument of createInstance. 
         * @throws CCAException in the event of error.
         */
        ::sidl::array< ::gov::cca::ComponentClassDescription>
        getAvailableComponentClasses_impl() // throws:
        //     ::gov::cca::CCAException
        //     ::sidl::RuntimeException
        ;

        /**
         *  the component instance returned is nil if the name is unknown
         * to the factory. The component is raw: it has been constructed
         * but not initialized via setServices.
         */
        ::gov::cca::Component
        createComponentInstance_impl (
          /* in */const ::std::string& className
        )
        ;


        /**
         *  reclaim any resources the factory may have associated with
         * the port it is using. This will occur after the
         * normal component shutdown  (ala componentrelease) is finished. 
         */
        void
        destroyComponentInstance_impl (
          /* in */const ::std::string& className,
          /* in */::gov::cca::Component c
        )
        ;

      };  // end class PrivateRepository_impl

    } // end namespace babel
  } // end namespace script
} // end namespace mpitest

// DO-NOT-DELETE splicer.begin(DOTPKG.PrivateRepository._misc)
// Put miscellaneous things here...
// DO-NOT-DELETE splicer.end(DOTPKG.PrivateRepository._misc)

#endif
"""

pkg_StringMap_Impl_cxx="""
// 
// File:          UBPKG_StringMap_Impl.cxx
// Symbol:        DOTPKG.StringMap-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.StringMap
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 
#include "UBPKG_StringMap_Impl.hxx"

// 
// Includes for all method dependencies.
// 
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif
#ifndef included_sidl_NotImplementedException_hxx
#include "sidl_NotImplementedException.hxx"
#endif
// DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._includes)
// Put additional includes or other arbitrary code here...
// DO-NOT-DELETE splicer.end(DOTPKG.StringMap._includes)

// speical constructor, used for data wrapping(required).  Do not put code here unless you really know what you're doing!
DCOLPKG::StringMap_impl::StringMap_impl() : StubBase(
  reinterpret_cast< void*>(::DCOLPKG::StringMap::_wrapObj(
  reinterpret_cast< void*>(this))),false) , _wrapped(true){ 
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._ctor2)
  // Insert-Code-Here {DOTPKG.StringMap._ctor2} (ctor2)
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap._ctor2)
}

// user defined constructor
void DCOLPKG::StringMap_impl::_ctor() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._ctor)
  // add construction details here
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap._ctor)
}

// user defined destructor
void DCOLPKG::StringMap_impl::_dtor() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._dtor)
  // add destruction details here
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap._dtor)
}

// static class initializer
void DCOLPKG::StringMap_impl::_load() {
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._load)
  // Insert-Code-Here {DOTPKG.StringMap._load} (class initialization)
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap._load)
}

// user defined static methods: (none)

// user defined non-static methods:
/**
 *  return true if key exists in map. 
 */
bool
DCOLPKG::StringMap_impl::has_impl (
  /* in */const ::std::string& key ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap.has)
	std::map<std::string, std::string >::iterator it = sm.find(key);
	if (it != sm.end())  { return true; }
	return false;
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap.has)
}

/**
 *  return value of key. if key is not defined in the map,
 * has side effect of defining the key with the empty
 * string value before returning the empty string.
 */
::std::string
DCOLPKG::StringMap_impl::get_impl (
  /* in */const ::std::string& key ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap.get)
  return sm[key];
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap.get)
}

/**
 *  add or change the value for a key 
 */
void
DCOLPKG::StringMap_impl::set_impl (
  /* in */const ::std::string& key,
  /* in */const ::std::string& value ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap.set)
  sm[key] = value;
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap.set)
}

/**
 *  remove the key and its value, if it is there. 
 */
void
DCOLPKG::StringMap_impl::erase_impl (
  /* in */const ::std::string& key ) 
{
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap.erase)
  sm.erase(key);
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap.erase)
}

/**
 *  ugly c++ pointer returned; type in c++
 * 'std::map<std::string, std::string> '
 * This pointer will be valid until the underlying
 * babel object (which contains the underlying
 * c++ object) is destroyed.
 */
void*
DCOLPKG::StringMap_impl::getUnderlyingStdMap_impl () 

{
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap.getUnderlyingStdMap)
  return &sm;
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap.getUnderlyingStdMap)
}


// DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._misc)
// Put miscellaneous code here
// DO-NOT-DELETE splicer.end(DOTPKG.StringMap._misc)
"""

pkg_StringMap_Impl_hxx="""
// 
// File:          UBPKG_StringMap_Impl.hxx
// Symbol:        DOTPKG.StringMap-v0.0
// Symbol Type:   class
// Babel Version: 1.0.4
// Description:   Server-side implementation for DOTPKG.StringMap
// 
// WARNING: Automatically generated; only changes within splicers preserved
// 
// 

#ifndef included_UBPKG_StringMap_Impl_hxx
#define included_UBPKG_StringMap_Impl_hxx

#ifndef included_sidl_cxx_hxx
#include "sidl_cxx.hxx"
#endif
#ifndef included_UBPKG_StringMap_IOR_h
#include "UBPKG_StringMap_IOR.h"
#endif
#ifndef included_UBPKG_StringMap_hxx
#include "UBPKG_StringMap.hxx"
#endif
#ifndef included_sidl_BaseClass_hxx
#include "sidl_BaseClass.hxx"
#endif
#ifndef included_sidl_BaseInterface_hxx
#include "sidl_BaseInterface.hxx"
#endif
#ifndef included_sidl_ClassInfo_hxx
#include "sidl_ClassInfo.hxx"
#endif


// DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._includes)
#include <string>
#include <map>
// DO-NOT-DELETE splicer.end(DOTPKG.StringMap._includes)

namespace mpitest { 
  namespace script { 
    namespace babel { 

      /**
       * Symbol "DOTPKG.StringMap" (version 0.0)
       */
      class StringMap_impl : public virtual ::DCOLPKG::StringMap 
  // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._inherits)
  // Put additional inheritance here...
  // DO-NOT-DELETE splicer.end(DOTPKG.StringMap._inherits)
      {

      // All data marked protected will be accessable by 
      // descendant Impl classes
      protected:

        bool _wrapped;

    // DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._implementation)
    // Put additional implementation details here...
    std::map< std::string, std::string> sm;
    // DO-NOT-DELETE splicer.end(DOTPKG.StringMap._implementation)

      public:
        // default constructor, used for data wrapping(required)
        StringMap_impl();
        // sidl constructor (required)
        // Note: alternate Skel constructor doesn't call addref()
        // (fixes bug #275)
        StringMap_impl( struct UBPKG_StringMap__object * s ) : 
          StubBase(s,true), _wrapped(false) { _ctor(); }

        // user defined construction
        void _ctor();

        // virtual destructor (required)
        virtual ~StringMap_impl() { _dtor(); }

        // user defined destruction
        void _dtor();

        // true if this object was created by a user newing the impl
        inline bool _isWrapped() {return _wrapped;}

        // static class initializer
        static void _load();

      public:


        /**
         *  return true if key exists in map. 
         */
        bool
        has_impl (
          /* in */const ::std::string& key
        )
        ;


        /**
         *  return value of key. if key is not defined in the map,
         * has side effect of defining the key with the empty
         * string value before returning the empty string.
         */
        ::std::string
        get_impl (
          /* in */const ::std::string& key
        )
        ;


        /**
         *  add or change the value for a key 
         */
        void
        set_impl (
          /* in */const ::std::string& key,
          /* in */const ::std::string& value
        )
        ;


        /**
         *  remove the key and its value, if it is there. 
         */
        void
        erase_impl (
          /* in */const ::std::string& key
        )
        ;


        /**
         *  ugly c++ pointer returned; type in c++
         * 'std::map<std::string, std::string> '
         * This pointer will be valid until the underlying
         * babel object (which contains the underlying
         * c++ object) is destroyed.
         */
        void*
        getUnderlyingStdMap_impl() ;
      };  // end class StringMap_impl

    } // end namespace babel
  } // end namespace script
} // end namespace mpitest

// DO-NOT-DELETE splicer.begin(DOTPKG.StringMap._misc)
// Put miscellaneous things here...
// DO-NOT-DELETE splicer.end(DOTPKG.StringMap._misc)

#endif
"""

driver_cxx="""
#include "UBPKG_BabelMain.hxx"
#include "dc/babel/babel-cca/AllBabelCCA.hh"
#include <iostream>

int UBPKG_genmain(int argc, char **argv) {


	DCOLPKG::BabelMain myScript =
		DCOLPKG::BabelMain::_create();
	ccaffeine::BabelMain cbm = myScript; // CAST

	ccaffeine::AbstractFramework caf = 
		ccaffeine::AbstractFramework::_create();
	caf.initialize("",0);

	try {
		caf.run( cbm );
	}
	catch ( ::gov::cca::CCAException oe)
	{
		::std::cout << "UBPKG_genmain caught fatal error:" << ::std::endl;
		::std::cout << oe.getNote() << ::std::endl;
		::std::cerr << "UBPKG_genmain caught fatal error:" << ::std::endl;
		::std::cerr << oe.getNote() << ::std::endl;
		return -2;
	}
	catch ( ::std::exception &e)
	{
		::std::cout << "UBPKG_genmain caught fatal error:" << ::std::endl;
		::std::cout << e.what() << ::std::endl;
		::std::cerr << "UBPKG_genmain caught fatal error:" << ::std::endl;
		::std::cerr << e.what() << ::std::endl;
		return -2;
	}

	return 0;
}

int main(int argc, char **argv) {
	return	UBPKG_genmain(argc,argv);
}	
"""
