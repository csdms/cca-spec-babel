#ifndef sandia_support_portData_hpp
#define sandia_support_portData_hpp

#include <string>
#include <map>

namespace sandia {
namespace support {

class PortData {
public:
  PortData() {}
  ~PortData() {}

  std::string summary; 
  std::string description;
  std::map<std::string, std::string> properties;

  int main(char **argv, int argc);

}; // end class portdata

} // end namespace support
} // end namespace sandia
#endif // sandia_support_portData_hpp
