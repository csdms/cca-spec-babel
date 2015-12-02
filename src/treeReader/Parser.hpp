#ifndef sandia_support_XMLParser_hpp
#define sandia_support_XMLParser_hpp

#include <string>
#include <vector>
#include <boost/smart_ptr.hpp>

namespace sandia {
namespace support {

class MetaDataParser;

/** This is a sax parser wrapper that keeps
 * all the implementation headers invisible
 * to the outside clients.
 */
class Parser {
public:
  Parser();
  ~Parser();

  /** load up a tree attached to this parser instance
   * using a file.
   */
  void parse(const std::string & file);
  void displayAll();

  std::vector< XMLNode_shared > findNodes(const std::string & tag);

private:
  MetaDataParser *p;

}; // end parser

} // end namespace support
} // end namespace sandia

#endif // sandia_support_XMLParser_hpp
