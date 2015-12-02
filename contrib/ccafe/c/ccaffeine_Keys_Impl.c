/*
 * File:          ccaffeine_Keys_Impl.c
 * Symbol:        ccaffeine.Keys-v0.3
 * Symbol Type:   class
 * Babel Version: 1.0.0
 * Description:   Server-side implementation for ccaffeine.Keys
 * 
 * WARNING: Automatically generated; only changes within splicers preserved
 * 
 */

/*
 * DEVELOPERS ARE EXPECTED TO PROVIDE IMPLEMENTATIONS
 * FOR THE FOLLOWING METHODS BETWEEN SPLICER PAIRS.
 */

/*
 * Symbol "ccaffeine.Keys" (version 0.3)
 * 
 * We would really like to make this a cross-language list of static final
 * string constants in the package namespace. Babel doesn't support final data
 * classes, however, so we must define a bunch of static methods to get
 * the same effect. Rather than keeping track of string spellings,
 * this lets the user make C macro-looking function calls which return
 * the exactly needed string if they've used the correct function.
 * <p>
 * Class defining some keys that will be found in various property maps.
 * These are useful either internally or for a user interface.
 * Obviously, this is just a first stab. Various agents are likely
 * define their own keys. GUI authors are encouraged to get together
 * and define a more complete set, which should perhaps be kept in
 * a separate package instead of as part of CCAFE.
 * Items marked 'Protected' may not be changable after an initial
 * value is set (by the framework).
 * </p>
 * 
 * <p>
 * The reason we need keys that are UI-implementation independent
 * and storable on component properties is that during long running
 * apps on big machines the gui comes and goes. The user will want
 * the gui to save state. a gui can of course keep it in its own keys,
 * on the component properties, but a better solution in a multi-
 * user/multi-desktop accessing the same big job scenario is to
 * have at least a base set of keys that all gui's understand.
 * </p>
 * 
 * 
 * <p>
 * Some keys and types that are protected
 * by the framework for its own use and cannot be set by user.
 * Attempts to reset them inappropriately will be ignored.
 * <ul>
 * <li> Int: CCAFE_FRAMEX, CCAFE_FRAMEY </li>
 * <li> String: CCAFE_CONNTYPE, CCAFE_CONNUSERPORT, CCAFE_CONNPROVIDERPORT,
 * CCAFE_CONNUSER, CCAFE_CONNPROVIDER, CCAFE_CLASS_SHORT_NAME </li>
 * <li> Bool: CCAFE_EXTERNAL_INSTANCE </li>
 * </ul>
 * </p>
 * <p>
 * Some keys and types that are protected
 * by the framework after initial definition from the user.
 * Attempts to reset them inappropriately may be ignored.
 * <ul>
 * <li> Int: CCA_MAXCONNECT, CCA_MINCONNECT </li>
 * <li> String: CCA_PORTNAME, CCA_PORTTYPE, CCAFE_CLASS_NAME </li>
 * <li> Bool: CCA_PROXYABLE </li>
 * </ul>
 * </p>
 */

#include "ccaffeine_Keys_Impl.h"
#include "sidl_NotImplementedException.h"
#include "sidl_Exception.h"

/* DO-NOT-DELETE splicer.begin(ccaffeine.Keys._includes) */
#include "sidl_String.h"
#define KEYS_RETURN(x) return sidl_String_strdup(x)
/* DO-NOT-DELETE splicer.end(ccaffeine.Keys._includes) */

#define SIDL_IOR_MAJOR_VERSION 1
#define SIDL_IOR_MINOR_VERSION 0
/*
 * Static class initializer called exactly once before any user-defined method is dispatched
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys__load"

#ifdef __cplusplus
extern "C"
#endif
void
impl_ccaffeine_Keys__load(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys._load) */
    /*
     * Nothing to do.
     */

    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys._load) */
  }
}
/*
 * Class constructor called when the class is created.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys__ctor"

#ifdef __cplusplus
extern "C"
#endif
void
impl_ccaffeine_Keys__ctor(
  /* in */ ccaffeine_Keys self,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys._ctor) */
    /*
     * Nothing to do.
     */
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys._ctor) */
  }
}

/*
 * Special Class constructor called when the user wants to wrap his own private data.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys__ctor2"

#ifdef __cplusplus
extern "C"
#endif
void
impl_ccaffeine_Keys__ctor2(
  /* in */ ccaffeine_Keys self,
  /* in */ void* private_data,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys._ctor2) */
    /*
     * Nothing to do.
     */
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys._ctor2) */
  }
}
/*
 * Class destructor called when the class is deleted.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys__dtor"

#ifdef __cplusplus
extern "C"
#endif
void
impl_ccaffeine_Keys__dtor(
  /* in */ ccaffeine_Keys self,
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys._dtor) */
    /*
     * Nothing to do.
     */
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys._dtor) */
  }
}

/*
 *  Protected typemap port property (String) instance name. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCA_PORTNAME"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCA_PORTNAME(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCA_PORTNAME) */
	KEYS_RETURN("cca.portName");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCA_PORTNAME) */
  }
}

/*
 *  Protected typemap port property (String) class name. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCA_PORTTYPE"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCA_PORTTYPE(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCA_PORTTYPE) */
	KEYS_RETURN("cca.portType");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCA_PORTTYPE) */
  }
}

/*
 *  Protected typemap port property (String) proxy friendly. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCA_PROXYABLE"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCA_PROXYABLE(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCA_PROXYABLE) */
	KEYS_RETURN("ABLE_TO_PROXY");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCA_PROXYABLE) */
  }
}

/*
 *  Protected typemap port property (Int) maximum connections on port. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCA_MAXCONNECT"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCA_MAXCONNECT(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCA_MAXCONNECT) */
	KEYS_RETURN("MAX_CONNECTIONS");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCA_MAXCONNECT) */
  }
}

/*
 *  Protected typemap port property (Int) minimum connections on port. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCA_MINCONNECT"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCA_MINCONNECT(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCA_MINCONNECT) */
	KEYS_RETURN("MIN_CONNECTIONS");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCA_MINCONNECT) */
  }
}

/*
 *  Typemap component instance, port, or connection instance visibility.
 * (Bool). Items tagged false can be omitted from lists
 * rendered to the user unless the user has opted to see hidden items.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_VISIBLE"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_VISIBLE(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_VISIBLE) */
	KEYS_RETURN("gov.ccafe.visible");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_VISIBLE) */
  }
}

/*
 *  Typemap component instance semantics.
 * (Bool). Items tagged true cannot safely have more than one instance
 * globally in a runtime. Thus their rendering may be handled specially
 * by a UI.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_SINGLETON"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_SINGLETON(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_SINGLETON) */
	KEYS_RETURN("gov.ccafe.singleton");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_SINGLETON) */
  }
}

/*
 *  Typemap component class name alias property
 * (String) abbreviated class name for user consumption,
 * which may be strictly political in origin.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_USER_CLASS_ALIAS"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_USER_CLASS_ALIAS(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_USER_CLASS_ALIAS) */
	KEYS_RETURN("gov.ccafe.PalletClassAlias");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_USER_CLASS_ALIAS) */
  }
}

/*
 *  Typemap component class name property
 * (String) unqualified class name. e.g. Vector, not Lib.Vector.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CLASS_SHORT_NAME"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CLASS_SHORT_NAME(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CLASS_SHORT_NAME) */
	KEYS_RETURN("gov.ccafe.PalletLeafName");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CLASS_SHORT_NAME) */
  }
}

/*
 *  Typemap component class name property
 * (String) fully qualified class name. e.g. Lib.Vector, not Vector.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_COMPONENT_INSTANCE_NAME"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_COMPONENT_INSTANCE_NAME(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_COMPONENT_INSTANCE_NAME) */
	KEYS_RETURN("gov.ccafe.instanceName");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_COMPONENT_INSTANCE_NAME) */
  }
}

/*
 *  Typemap component class name property
 * (String) fully qualified class name. e.g. Lib.Vector, not Vector.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CLASS_NAME"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CLASS_NAME(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CLASS_NAME) */
	KEYS_RETURN("gov.ccafe.PalletClassName");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CLASS_NAME) */
  }
}

/*
 *  Typemap component class name property
 * (String) url of image file for class in a user interface.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CLASS_IMAGE_FILE"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CLASS_IMAGE_FILE(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CLASS_IMAGE_FILE) */
	KEYS_RETURN("gov.ccafe.PalletImageURL");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CLASS_IMAGE_FILE) */
  }
}

/*
 *  Protected typemap component class name property
 * (String) xbm string of image file for class in a user interface.
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CLASS_IMAGE"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CLASS_IMAGE(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CLASS_IMAGE) */
	KEYS_RETURN("gov.ccafe.PalletImage");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CLASS_IMAGE) */
  }
}

/*
 *  Typemap component instance frame position (integer) X. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_FRAMEX"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_FRAMEX(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_FRAMEX) */
	KEYS_RETURN("gov.ccafe.frameX");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_FRAMEX) */
  }
}

/*
 *  Typemap component instance frame position (integer) Y. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_FRAMEY"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_FRAMEY(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_FRAMEY) */
	KEYS_RETURN("gov.ccafe.frameY");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_FRAMEY) */
  }
}

/*
 *  Protected typemap connectionid property (String)
 * user/provider port class name. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CONNTYPE"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CONNTYPE(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CONNTYPE) */
	KEYS_RETURN("gov.ccafe.ConnectionType");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CONNTYPE) */
  }
}

/*
 *  Protected typemap connectionid property (String) 
 * user port instance name. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CONNUSERPORT"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CONNUSERPORT(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CONNUSERPORT) */
	KEYS_RETURN("gov.ccafe.UserPortInstance");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CONNUSERPORT) */
  }
}

/*
 *  Protected typemap connectionid property (String)
 * provider port instance name. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CONNPROVIDERPORT"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CONNPROVIDERPORT(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CONNPROVIDERPORT) */
	KEYS_RETURN("gov.ccafe.ProviderPortInstance");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CONNPROVIDERPORT) */
  }
}

/*
 *  Protected typemap connectionid property (String)
 * user component instance name. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CONNUSER"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CONNUSER(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CONNUSER) */
	KEYS_RETURN("gov.ccafe.UserComponentInstance");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CONNUSER) */
  }
}

/*
 *  Protected typemap connectionid property (String)
 * provider component instance name. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_CONNPROVIDER"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_CONNPROVIDER(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_CONNPROVIDER) */
	KEYS_RETURN("gov.ccafe.ProviderComponentInstance");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_CONNPROVIDER) */
  }
}

/*
 *  Protected typemap component instance property 
 * (Bool) inserted via AbstractFramework. 
 */

#undef __FUNC__
#define __FUNC__ "impl_ccaffeine_Keys_CCAFE_EXTERNAL_INSTANCE"

#ifdef __cplusplus
extern "C"
#endif
char*
impl_ccaffeine_Keys_CCAFE_EXTERNAL_INSTANCE(
  /* out */ sidl_BaseInterface *_ex)
{
  *_ex = 0;
  {
    /* DO-NOT-DELETE splicer.begin(ccaffeine.Keys.CCAFE_EXTERNAL_INSTANCE) */
	KEYS_RETURN("gov.ccafe.ExternalComponentInstance");
    /* DO-NOT-DELETE splicer.end(ccaffeine.Keys.CCAFE_EXTERNAL_INSTANCE) */
  }
}
