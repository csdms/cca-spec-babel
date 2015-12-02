#ifndef XMLCCAExtractor_hpp
#define XMLCCAExtractor_hpp

#include <vector>
#include <stdexcept>

/* compilation of this class depends on the preprocessor variable
 * _NO_XML
 * If _NO_XML is defined (-D_NO_XML) then all xml related calls
 * throw exceptions, no xml library need be linked.
 */
namespace sandia {
namespace support {

/**
 * This class just parses an xml input and print
 * s out tuples it finds:
 * binding className paletteClassAlias constructor
 */
class XMLCCAExtractor
{

private:
	/** extract xml descriptions and append to vector. 
	 * @return 0 if ok. */
	int extractXMLDescriptions(  const std::string & filename);

public:
	XMLCCAExtractor();
	~XMLCCAExtractor();

	/** parse a file and print the results on stdout.
	 * Does nothing if xml is not compiled in.
	 */
	void parseDescriptions( const std::string & filename) throw ( std::invalid_argument);

	/** test function.  given a filename, calls parse and prints results. */
	int main(int argc, char *argv[]);

}; // end XMLCCAExtractor

} // end namespace support
} // end namespace sandia
#endif // XMLCCAExtractor_hpp
