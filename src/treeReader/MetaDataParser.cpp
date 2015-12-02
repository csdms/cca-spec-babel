#include "treeReader/treeParser_internal.hpp"
#include "treeReader/MetaDataParser.hpp"
#include "treeReader/XMLNode.hpp"
#include "treeReader/Node.hpp"
#include <cstring>

sandia::support::MetaDataParser::MetaDataParser()
{
  initialize();
}

sandia::support::MetaDataParser::~MetaDataParser()
{
  // Insert cleanup here (handler, etc)
  if (current) {
    current->clearTree();
  }
  xmlCleanupParser();
}


void
sandia::support::MetaDataParser::initialize() {

  rootNode = Node_shared(new Node);
  rootNode->name = "ROOT";
  current = rootNode;

  memset((void *)(&handler), 0, sizeof(xmlSAXHandler));
#if CCAFE_SAX2
  xmlSAXVersion(&handler,1);
#endif
  INITHANDLER(&handler, 0);

  if (!handler.initialized) {
    std::cerr << "Failed to initialize SAX handler" << std::endl;
    return;
  } 

  handler.startElement = (startElementSAXFunc)(MetaDataParser::startElement);
  handler.endElement   = (endElementSAXFunc)(MetaDataParser::endElement);
  handler.characters   = (charactersSAXFunc)(MetaDataParser::characters);
  handler.startDocument  = (startDocumentSAXFunc)(MetaDataParser::startDocument);
  handler.endDocument  = (endDocumentSAXFunc)(MetaDataParser::endDocument);
  handler.comment      = (commentSAXFunc)(MetaDataParser::comment);
  // handler.warning      = (warningSAXFunc)(MetaDataParser::warning);
  handler.cdataBlock   = (cdataBlockSAXFunc)(MetaDataParser::cdataBlock);
}

void
sandia::support::MetaDataParser::parse(const std::string & filename) {
  xmlSAXUserParseFile(&handler, this, filename.c_str());
  fname = filename;
}


void
sandia::support::MetaDataParser::startElement(void *ctx, const xmlChar *name, const xmlChar **atts) {
#if MDP_DEBUG
  std::cout << "Start element: " << name << std::endl;
#endif
  MetaDataParser *mdp = (MetaDataParser*) ctx;

  // make new child node for new element
  Node_shared parent = mdp->current;
  Node_shared child = Node_shared(new Node());

  // init child
  child->setParent(parent);
  child->name = xmlChar2String(name);
  child->appendAttrList(atts);
#if MDP_DEBUG
  if (atts != 0) {
	  std::cout << "atts= " << std::endl;
	  const xmlChar **t = atts;
	  while (*t != 0) {
		  std::cout << *t << " " << std::endl;
		  t++;
	  }
  }
#endif

  // add child to parent
  mdp->current->children.push_back(child);

  // make child current
  mdp->current = child;
#if MDP_DEBUG
  std::cout << "CURRENT= " << mdp->current->name << std::endl;
#endif

}

void 
sandia::support::MetaDataParser::endElement(void *ctx, const xmlChar *name) {
#if MDP_DEBUG
  std::cout << "End element: " << name << std::endl;
#endif
  MetaDataParser *mdp = (MetaDataParser*) ctx;

  // check tag, though probably not needed if xml parser is 
  // checking for us.
  std::string endname = xmlChar2String(name);
  if ( endname != mdp->current->name ) {
	  std::cerr << "found element end tag " << endname <<
		  " while parsing element " << mdp->current->name <<
		  std::endl;
	  std::cerr << "Fix your xml" << endname <<
		  std::endl;
	  exit(1);
  }
  mdp->current = mdp->current->parent;
#if MDP_DEBUG
  std::cout << "CURRENT= " << mdp->current->name << std::endl;
#endif

}

void 
sandia::support::MetaDataParser::characters(void *ctx, const xmlChar *ch, int len) {
  MetaDataParser *mdp = (MetaDataParser *) ctx;
  std::string s = xmlChar2String(ch,len);
#if MDP_DEBUG
   std::cout << "Characters: " << s << std::endl;
#endif
  mdp->current->txt += s;
}

void 
sandia::support::MetaDataParser::endDocument(void *ctx) {
#if MDP_DEBUG
  std::cout << "End document" << std::endl;
#endif
  MetaDataParser *mdp = (MetaDataParser *) ctx;
  // so now find the top and set root there
  while (mdp->current != 0 && mdp->current->parent != 0) {
	  mdp->current = mdp->current->parent;
#if MDP_DEBUG
  std::cout << "CURRENT= " << mdp->current->name << std::endl;
#endif
  }
}

void 
sandia::support::MetaDataParser::startDocument(void *ctx) {
#if MDP_DEBUG
  std::cout << "Start document" << std::endl;
#endif
  MetaDataParser *mdp = (MetaDataParser *) ctx;
  if (mdp == 0) {
	  std::cerr<< "null parser in doc start!" << ::std::endl;
	  exit(1);
  }
}

void 
sandia::support::MetaDataParser::comment(void *ctx, const xmlChar *val) {
#if MDP_DEBUG
   std::cout << "Comment:" <<  xmlChar2String(val) << std::endl;
#endif
}

void
sandia::support::MetaDataParser::warning (void *ctx, const char *msg, ...) {
  std::cerr << "warning:" << msg << std::endl;
}

void
sandia::support::MetaDataParser::cdataBlock (void *ctx, const xmlChar *value, int len) {
#if MDP_DEBUG
  std::cout << "cdataBlock" << xmlChar2String(value,len) << std::endl;
#endif
}

std::string
sandia::support::MetaDataParser::xmlChar2String(const xmlChar *value, int len)
{
	xmlChar *subset = (xmlChar *)malloc((len+1)*sizeof(xmlChar));
	for (int i = 0; i < len; i++) {
		subset[i] = value[i];
	}
	subset[len] = 0;
	std::string result = reinterpret_cast<const char*>(subset);
	free(subset);
	return result;
}

std::string
sandia::support::MetaDataParser::xmlChar2String(const xmlChar *value)
{
	std::string result = reinterpret_cast<const char*>(value);
	return result;
}

void 
sandia::support::MetaDataParser::displayAll()
{
	std::cout<<"==============" << std::endl;
	std::cout<<"file: " << fname << std::endl;
	std::cout<<"==============" << std::endl;
	displayNode(current,0,4);
}

void 
sandia::support::MetaDataParser::displayNode(Node_shared & n, int depth, int tabwidth)
{
	int blanks = depth*tabwidth;
	depth++;

#define BLANKS for (int i = 0; i < blanks; i++) std::cout << " "

	BLANKS;
	std::cout << "<" << n->name;
	const std::vector< std::string > & al = n->getAttrList();
	size_t nats = al.size()/2;
	for (size_t j = 0; j < nats; j += 2 ) {
		std::cout << " " << al[j] << "=\"" << al[j+1] <<"\"";
	}
	std::cout << ">" << std::endl;
#if MDP_ECHO_TEXT
	std::cout << n->txt << std::endl;
	BLANKS;
#endif
	size_t nc = n->children.size(); 
	size_t k;
	for (k = 0; k < nc; k++) {
		Node_shared child = n->children[k];
		displayNode(child,depth,tabwidth);
	}
	BLANKS;
	std::cout << "</" << n->name << ">" << std::endl;
#undef BLANKS
}

std::vector< sandia::support::XMLNode_shared >
sandia::support::MetaDataParser::findNodes(const std::string & tag)
{
	std::vector< XMLNode_shared > v;
	searchNode(rootNode, tag, v);
	return v;
}

void 
sandia::support::MetaDataParser::searchNode( Node_shared & r, const std::string & tag, std::vector< XMLNode_shared > & results)
{

	if (r->name == tag) {
		results.push_back(r);
	}
	size_t nc = r->children.size(); 
	size_t k;
	for (k = 0; k < nc; k++) {
		Node_shared child = r->children[k];
		searchNode(child,tag,results);
	}
}


