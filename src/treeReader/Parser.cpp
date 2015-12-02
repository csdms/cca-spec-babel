#include <string>
#include <vector>
#include <iostream>
#include <map>
#include <boost/smart_ptr.hpp>
#include <libxml/SAX.h>    // libxml2 header, usually in /usr/include/libxml2

#include "treeReader/treeParser_internal.hpp"
#include "treeReader/XMLNode.hpp"
#include "treeReader/Node.hpp"
#include "treeReader/MetaDataParser.hpp"
#include "treeReader/Parser.hpp"

sandia::support::Parser::Parser()
{
	p = new sandia::support::MetaDataParser();
}

sandia::support::Parser::~Parser()
{
	delete p;
	p = 0;
}

void
sandia::support::Parser::parse(const std::string & file)
{
	p->parse(file);
}

void 
sandia::support::Parser::displayAll()
{
	p->displayAll();
}

std::vector< sandia::support::XMLNode_shared > 
sandia::support::Parser::findNodes(const std::string & tag)
{
	return p->findNodes( tag );
}
