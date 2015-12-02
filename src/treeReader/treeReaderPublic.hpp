#ifndef sandia_support_treeReaderPublic_h_seen
#define sandia_support_treeReaderPublic_h_seen

#include <string>
#include <vector>
#include <boost/smart_ptr.hpp>

namespace sandia {
namespace support {

class XMLNode;
typedef boost::shared_ptr< XMLNode > XMLNode_shared;

} // end  namespace support
} // end  namespace sandia

#include "treeReader/XMLNode.hpp"
#include "treeReader/Parser.hpp"

#endif // sandia_support_treeReaderPublic_h_seen
