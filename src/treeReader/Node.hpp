#ifndef sandia_support_TreeReaderNode_hpp
#define sandia_support_TreeReaderNode_hpp

#include <string>
#include <vector>

namespace sandia {
namespace support {

class Node : public virtual XMLNode {
private:
	Node_shared parent;
	std::string name;
	std::vector< std::string > attrlist;
	std::string txt;
	std::vector< Node_shared > children;

public:
	Node();
	virtual ~Node();
	void setParent( Node_shared p) {
		parent = p;
	}
	void appendAttrList(const xmlChar **atts);

	virtual XMLNode_shared getParent() { return parent; }
	virtual std::vector< XMLNode_shared > getChildren()
       	{ 
		std::vector< XMLNode_shared > result;
		for (size_t i = 0; i < children.size(); i++) 
		{
			XMLNode_shared xn = children[i];
			result.push_back(xn);
		}
		return result ;
       	}
	virtual std::string getName() { return name; }
	virtual std::string getText() { return txt; }
	virtual const std::vector< std::string > & getAttrList() { return attrlist; }

        virtual std::vector< XMLNode_shared > matchChildren( std::string tag);
	
	virtual std::string getAttribute(const std::string & attrName, const std::string & attrDefault);

	// knock off the back pointers.
	// then, when root leaves scope, children
	// will all die too.
	void clearTree() {
		parent = Node_shared();
		for (size_t i = 0 ; i < children.size(); i++) {
			(children[i])->clearTree();
		}
	}

	static int main(int argc, char *argv[]);

	friend class MetaDataParser;
}; // end class Node


} // end namespace support
} // end namespace sandia

#endif // sandia_support_XmlNode_hpp
