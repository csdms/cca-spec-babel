#include <vector>
#include <complex>
#include <boost/shared_ptr.hpp>
#include "treeReader/XMLCCAExtractor.hh"
#include "treeReader/treeReaderPublic.hpp"
#include "treeReader/ComponentData.hpp"
#include "treeReader/XMLCCAExtractor.hh"
#include <cstring>

#define DCCC_DEBUG
#undef DCCC_DEBUG // quiet by default

#define PATHSEP "/"
#define PATHSEP_CHAR '/'


sandia::support::XMLCCAExtractor::XMLCCAExtractor()
{
#ifdef DCCC_DEBUG
	std::cerr<< __FILE__ << ": CTOR" << std::endl;
#endif
}

sandia::support::XMLCCAExtractor::~XMLCCAExtractor()
{
#ifdef DCCC_DEBUG
	std::cerr<< __FILE__ << ": DTOR" << std::endl;
#endif
}

void
sandia::support::XMLCCAExtractor::parseDescriptions( const std::string & mypath)
       	throw ( std::invalid_argument)
{
	bool warned = false;
	if (mypath == "") {
		warned = true;
		std::cerr << __FILE__ <<":"<< __LINE__ << ": dying 1..." << std::endl;
		throw std::invalid_argument("sandia::support::XMLCCAExtractor::parseDescriptions: null input file given");
	}

	extractXMLDescriptions(mypath);

}


namespace /* anonymous, to hide local functions */ 
{

// strip leading create_ if there and return rest.
std::string extractClassName(const char *name)
{
	const char *x;
	std::string result = name;
	if (strncmp(name,"create_",7) == 0)
	{
		x = name + 7;
		result = x;
	}
	return result;
}

} // end anonymous namespace


int
sandia::support::XMLCCAExtractor::extractXMLDescriptions(const std::string & path)
{
	std::vector< sandia::support::ComponentData_shared > ccdv;
#ifdef _NO_XML
	std::cerr << __FILE__ <<":"<< __LINE__ << "built without XML support." << std::endl;
	throw std::invalid_argument("sandia::support::XMLCCAExtractor: built without XML support.");
#else
	sandia::support::Parser parser;
	parser.parse(path); // return 1 if we have an error detectable here.
	std::vector< XMLNode_shared > depls = parser.findNodes("componentDeployment");
	
	// iterate list to create and append ccds on ccdv.
	std::string componentClassName;
	std::string deploymentClassAlias;
	std::string ccaSpecBinding;
	std::string libraryLoading;
	std::string libraryLocation;
	std::string libraryName;
	std::string libtoolName;
	std::string staticName;
	std::string sharedName;
	std::string execScript;
	std::string cctor;
	std::string incdirs;
	std::string incfiles;

	for ( size_t i =0; i < depls.size(); i++) {
		XMLNode_shared x = depls[i];
		componentClassName = 
			x->getAttribute("name","_BoGuS_");
		if (componentClassName == "_BoGuS_") {
			continue; // skip records w/out name.
		}
		deploymentClassAlias = 
			x->getAttribute("palletClassAlias", componentClassName);
		std::vector< XMLNode_shared > envs = 
			x->matchChildren("environment");
		if (envs.size() != 1) {
			continue; // skip records w/out env or w/multiple.
		}
		std::vector< XMLNode_shared > specs =
			envs[0]->matchChildren("ccaSpec");
		if (specs.size() > 1) {
			continue; // skip records w/out env or w/multiple.
		}
		if (specs.size() == 0) {
			ccaSpecBinding = "babel";
		} else {
			ccaSpecBinding = specs[0]->getAttribute("binding","babel");
		}

		std::vector< XMLNode_shared > libs =
			envs[0]->matchChildren("library");
		if (libs.size() != 1) {
			continue; // skip records w/out env or w/multiple.
		}
		XMLNode_shared lib = libs[0];
		libraryLoading = lib->getAttribute("loading","_BoGuS_");
		libraryLocation = lib->getAttribute("location","_BoGuS_");
		libraryName = lib->getAttribute("name", "_BoGuS_");
		libtoolName = lib->getAttribute("libtool-archive", "_BoGuS_FIX.depl.cca");
		staticName = lib->getAttribute("static-archive", "_BoGuS_FIX.depl.cca");
		sharedName = lib->getAttribute("shared-archive", "_BoGuS_FIX.depl.cca");
		cctor = lib->getAttribute("constructor", "_BoGuS_");

		if (	libraryLoading == "_BoGuS_" 
			// || libraryLocation == "_BoGuS_" || libraryName == "_BoGuS_"
		   ) {
			continue; // skip records w/out complete location.
		}

		std::vector< XMLNode_shared > headers =
			envs[0]->matchChildren("headers");
		if (headers.size() != 1) {
			continue; // skip records w/out header or w/multiple.
		}
		XMLNode_shared header = headers[0];
		incdirs = header->getAttribute("path","_BoGuS_FIX.depl.cca");
		incfiles = header->getAttribute("files","_BoGuS_FIX.depl.cca");

		// create the class description instance.
		sandia::support::ComponentData *cd = new sandia::support::ComponentData();
		if (cctor != "_BoGuS_") {
			cd->setConstructorName(cctor);
		}
		cd-> setComponentClassName( componentClassName );
		cd-> setDeploymentClassAlias( deploymentClassAlias );
		cd-> setCCASpecBinding( ccaSpecBinding ); 
		cd-> setLibraryLoading( libraryLoading );
		cd-> setLibraryLocation( libraryLocation );
		cd-> setLibraryName( libraryName );
		cd-> setStaticLibraryName( staticName );
		cd-> setSharedLibraryName( sharedName );
		cd-> setLibtoolLibraryName( libtoolName );
		cd-> setExecScript("");
		cd-> setIndexFile( path );
		cd-> setIncludeDirs( incdirs );
		cd-> setIncludeFiles( incfiles );
		sandia::support::ComponentData_shared ccd(cd);
		ccdv.push_back(ccd);

	}
	sandia::support::ComponentData_shared cds;
	for (size_t k = 0, n = ccdv.size(); k < n; k++)
	{
		cds = ccdv[k];
		ccaSpecBinding = cds->getCCASpecBinding();
		componentClassName = cds->getComponentClassName();
		deploymentClassAlias = cds->getDeploymentClassAlias();
		cctor = cds->getConstructorName();
		incdirs = cds->getIncludeDirs() ;
		incfiles = cds->getIncludeFiles() ;
		staticName =  cds->getStaticLibraryName();
		sharedName =  cds->getSharedLibraryName();
		libtoolName =  cds->getLibtoolLibraryName();
		if ( ccaSpecBinding == "babel" ) {
			std::cout << 
				ccaSpecBinding << " " <<
				componentClassName << " " <<
				deploymentClassAlias << " " <<
				libraryName << " " <<
				incdirs << " " <<
				incfiles << " " <<
				libtoolName << " " <<
				sharedName << " " <<
				staticName << " " <<
				std::endl;
		} else {
			std::cout << 
				ccaSpecBinding << " " <<
				componentClassName << " " <<
				deploymentClassAlias << " " <<
				cctor <<
				std::endl;
		}

	}
#endif // no xml
	return 0;
}

int
sandia::support::XMLCCAExtractor::main(int argc, char *argv[])
{
	sandia::support::XMLCCAExtractor dcc;
	
	// actual test code
	if (argc != 2) {
		std::cerr << argv[0] << ": " << "<filepathName> required" << std::endl;
		return 1;
	}

	std::string path = argv[1];
	dcc.parseDescriptions(path);
	return 0;
}

#ifdef XMLCCAExtractor_MAIN
int main(int argc, char *argv[])
{
	sandia::support::XMLCCAExtractor dcc;
	return dcc.main(argc,argv);
}
#endif // XMLCCAExtractor_MAIN
