/*  This is the header that may be used with some legacy builds.
 *  The proper include, of course, is
 *  gov_cca.hh and gov_cca_ports.hh.
 */
#if !defined(CXX_HEADER_SUFFIX_HXX)

#include "gov_cca_AbstractFramework.hh"
#include "gov_cca_CCAException.hh"
#include "gov_cca_CCAExceptionType.hh"
#include "gov_cca_Port.hh"
#include "gov_cca_Type.hh"
#include "gov_cca_TypeMap.hh"
#include "gov_cca_TypeMismatchException.hh"
#include "gov_cca_ComponentID.hh"
#include "gov_cca_Services.hh"
#include "gov_cca_Component.hh"
#include "gov_cca_ConnectionID.hh"
#include "gov_cca_ComponentClassDescription.hh"
#include "gov_cca_ports_BuilderService.hh"
#include "gov_cca_ports_ComponentRepository.hh"
#include "gov_cca_ports_EventType.hh"
#include "gov_cca_ports_ConnectionEvent.hh"
#include "gov_cca_ports_ConnectionEventListener.hh"
#include "gov_cca_ports_ConnectionEventService.hh"
#include "gov_cca_ports_GoPort.hh"
#include "gov_cca_ports_ServiceProvider.hh"
#include "gov_cca_ports_ServiceRegistry.hh"

#else    /* header suffix is hxx */

#include "gov_cca_AbstractFramework.hxx"
#include "gov_cca_CCAException.hxx"
#include "gov_cca_CCAExceptionType.hxx"
#include "gov_cca_Port.hxx"
#include "gov_cca_Type.hxx"
#include "gov_cca_TypeMap.hxx"
#include "gov_cca_TypeMismatchException.hxx"
#include "gov_cca_ComponentID.hxx"
#include "gov_cca_Services.hxx"
#include "gov_cca_Component.hxx"
#include "gov_cca_ConnectionID.hxx"
#include "gov_cca_ComponentClassDescription.hxx"
#include "gov_cca_ports_BuilderService.hxx"
#include "gov_cca_ports_ComponentRepository.hxx"
#include "gov_cca_ports_EventType.hxx"
#include "gov_cca_ports_ConnectionEvent.hxx"
#include "gov_cca_ports_ConnectionEventListener.hxx"
#include "gov_cca_ports_ConnectionEventService.hxx"
#include "gov_cca_ports_GoPort.hxx"
#include "gov_cca_ports_ServiceProvider.hxx"
#include "gov_cca_ports_ServiceRegistry.hxx"

#endif

#include "babel_compat.hh"



