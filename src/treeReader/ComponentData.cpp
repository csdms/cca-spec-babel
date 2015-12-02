#include "treeReader/ComponentData.hpp"

#define CD_DEBUG 0

class local_exception : public virtual std::exception {
private:
	std::string msg;
public:
	local_exception(std::string m) {
		msg = m;
	}
	~local_exception() throw () {};
	local_exception() {
		msg = "no_message_defined";
	}
	virtual std::string what() { return msg; }
};

sandia::support::ComponentData::ComponentData()
{
#if CD_DEBUG
	std::cerr << __FILE__ << ": ctor" << std::endl;
#endif
	initDummy();
	dead = 0;
}

sandia::support::ComponentData::~ComponentData()
{
#if CD_DEBUG
	std::cerr << __FILE__ << ": dtor" << std::endl;
#endif
	std::string s = "dead_";
	s += componentClassName;
	initDummy();
	componentClassName = s;
	dead = 0xFEEDF00D;
}

std::string sandia::support::ComponentData::getComponentClassName () throw(std::exception)
{
	if (dead != 0xFEEDF00D) {
#if CD_DEBUG
	std::cerr << __FILE__ << ":getComponentClassName " << componentClassName << std::endl;
#endif
		return componentClassName;
	}
#if CD_DEBUG
	std::cerr << __FILE__ << ":getComponentClassName " << "DEAD_!! "<< std::endl;
#endif
	throw local_exception("sandia::support::ComponentData::getComponentClassName called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getSharedLibraryName ()throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return libraryNameShared;
	}
	throw local_exception("sandia::support::ComponentData::getSharedLibraryName called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getStaticLibraryName ()throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return libraryNameStatic;
	}
	throw local_exception("sandia::support::ComponentData::getStaticLibraryName called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getLibtoolLibraryName ()throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return libraryNameLibtool;
	}
	throw local_exception("sandia::support::ComponentData::getLibtoolLibraryName called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getLibraryName ()throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return libraryName;
	}
	throw local_exception("sandia::support::ComponentData::getLibraryName called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getDeploymentClassAlias() throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
#if CD_DEBUG
	std::cerr << __FILE__ << ":getDeploymentClassAlias " << componentClassName << std::endl;
#endif
		return deploymentClassAlias;
	}
#if CD_DEBUG
	std::cerr << __FILE__ << ":getDeploymentClassAlias " << "DEAD_!!"<< std::endl;
#endif
	throw local_exception("sandia::support::ComponentData::getDeploymentClassAlias called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getCCASpecBinding() throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return ccaSpecBinding;
	}
	throw local_exception("sandia::support::ComponentData::getCCASpecBinding called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getLibraryLoading() throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return libraryLoading;
	}
	throw local_exception("sandia::support::ComponentData::getLibraryLoading called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getConstructorName() throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return ctorName;
	}
	throw local_exception("sandia::support::ComponentData::getConstructorName called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getIndexFile() throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return indexFile;
	}
	throw local_exception("sandia::support::ComponentData::getIndexFile called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getLibraryLocation() throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return libraryLocation;
	}
	throw local_exception("sandia::support::ComponentData::getLibraryLocation called on deallocated ComponentData reference");
}

std::string sandia::support::ComponentData::getExecScript () throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return execScript;
	}
	throw local_exception("sandia::support::ComponentData::getExecScript called on deallocated ComponentData reference");
}

void 
sandia::support::ComponentData::getDOMTree () throw (std::exception)
{
}

std::string
sandia::support::ComponentData::getIncludeDirs() throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return incdirs;
	}
	throw local_exception("sandia::support::ComponentData::getIncludeDirs called on deallocated ComponentData reference");
}

std::string 
sandia::support::ComponentData::getIncludeFiles() throw (std::exception)
{
	if (dead != 0xFEEDF00D) {
		return incfiles;
	}
	throw local_exception("sandia::support::ComponentData::getIncludeFiles called on deallocated ComponentData reference");
}

void 
sandia::support::ComponentData::setIncludeDirs( std::string s)
{
	incdirs= s;
#if CD_DEBUG
	std::cerr << __FILE__ << ":setIncludeDirs " << s << std::endl;
#endif
}

void sandia::support::ComponentData::setIncludeFiles( std::string s)
{
	incfiles = s;
#if CD_DEBUG
	std::cerr << __FILE__ << ":setIncludeFiles " << s << std::endl;
#endif
}

void sandia::support::ComponentData::setComponentClassName( std::string s)
{
	componentClassName = s;
#if CD_DEBUG
	std::cerr << __FILE__ << ":setComponentClassName " << s << std::endl;
#endif
}

void sandia::support::ComponentData::setIndexFile( std::string s)
{
	indexFile = s;
#if CD_DEBUG
	std::cerr << __FILE__ << ":setIndexFile " << s << std::endl;
#endif
}

void sandia::support::ComponentData::setDeploymentClassAlias( std::string s)
{
#if CD_DEBUG
	std::cerr << __FILE__ << ":setDeploymentClassAlias " << s << std::endl;
#endif
	deploymentClassAlias = s;
}

void sandia::support::ComponentData::setCCASpecBinding( std::string s)
{
#if CD_DEBUG
	std::cerr << __FILE__ << ":setCCASpecBinding " << s << std::endl;
#endif
	ccaSpecBinding = s;
}

void sandia::support::ComponentData::setLibraryLoading( std::string s)
{
	libraryLoading = s;
}

void sandia::support::ComponentData::setLibraryLocation( std::string s)
{
	libraryLocation = s;
}

void sandia::support::ComponentData::setLibtoolLibraryName( std::string s)
{
	libraryNameLibtool = s;
}

void sandia::support::ComponentData::setStaticLibraryName( std::string s)
{
	libraryNameStatic = s;
}

void sandia::support::ComponentData::setSharedLibraryName( std::string s)
{
	libraryNameShared = s;
}

void sandia::support::ComponentData::setLibraryName( std::string s)
{
	libraryName = s;
}

void sandia::support::ComponentData::setConstructorName( std::string s)
{
	ctorName = s;
}

void sandia::support::ComponentData::setExecScript( std::string s)
{
	execScript = s;
}

void sandia::support::ComponentData::initDummy()
{
	componentClassName = "uninit_componentClassName";
	deploymentClassAlias = "uninit_deploymentClassAlias";
	ccaSpecBinding = "uninit_ccaSpecBinding";
	libraryLoading = "uninit_libraryLoading";
	libraryLocation = "uninit_libraryLocation";
	libraryName = "uninit_libraryName";
	libraryNameStatic = "uninit_libraryNameStatic";
	libraryNameShared = "uninit_libraryNameShared";
	libraryNameLibtool = "uninit_libraryNameLibtool";
	execScript = "uninit_execScript";
	incdirs = "uninit_incdirs";
	incfiles = "uninit_incfiles";
}

#include <iostream>

int sandia::support::ComponentData::main(int argc, char **argv)
{
	ComponentData c;

	std::string s = c.getComponentClassName();
	std::cout << "class= " << s << std::endl;

	s = c.getDeploymentClassAlias();
	std::cout << "alias= " << s << std::endl;

	s = c.getCCASpecBinding();
	std::cout << "binding= " << s << std::endl;

	s = c.getLibraryLoading();
	std::cout << "loading= " << s << std::endl;

	s = c.getLibraryLocation();
	std::cout << "location= " << s << std::endl;

	s = c.getLibraryName ();
	std::cout << "name= " << s << std::endl;

	s = c.getLibtoolLibraryName ();
	std::cout << "libtool= " << s << std::endl;

	s = c.getSharedLibraryName ();
	std::cout << "shared= " << s << std::endl;

	s = c.getStaticLibraryName ();
	std::cout << "static= " << s << std::endl;

	s = c.getLibraryName ();
	std::cout << "name= " << s << std::endl;

	s = c.getExecScript ();
	std::cout << "script= " << s << std::endl;

	c.setComponentClassName( "myclass");
	c.setDeploymentClassAlias( "myalias");
	c.setConstructorName( "myclassicCTOR");
	c.setCCASpecBinding( "mybinding");
	c.setLibraryLoading( "myload");
	c.setLibraryLocation( "mydir");
	c.setLibraryName( "mylib");
	c.setSharedLibraryName( "mylib.so");
	c.setStaticLibraryName( "mylib.a");
	c.setLibtoolLibraryName( "mylib.la");
	c.setIncludeDirs( "mydirs");
	c.setIncludeFiles( "myfiles");
	c.setExecScript( "myscript");

	s = c.getComponentClassName();
	std::cout << "class= " << s << std::endl;

	s = c.getDeploymentClassAlias();
	std::cout << "alias= " << s << std::endl;

	s = c.getCCASpecBinding();
	std::cout << "binding= " << s << std::endl;

	s = c.getLibraryLoading();
	std::cout << "loading= " << s << std::endl;

	s = c.getConstructorName();
	std::cout << "ctorname= " << s << std::endl;

	s = c.getLibraryLocation();
	std::cout << "location= " << s << std::endl;

	s = c.getLibraryName ();
	std::cout << "name= " << s << std::endl;

	s = c.getLibtoolLibraryName ();
	std::cout << "libtool= " << s << std::endl;

	s = c.getStaticLibraryName ();
	std::cout << "static= " << s << std::endl;

	s = c.getSharedLibraryName ();
	std::cout << "shared= " << s << std::endl;

	s = c.getExecScript ();
	std::cout << "script= " << s << std::endl;

	s = c.getIncludeFiles ();
	std::cout << "incfiles= " << s << std::endl;

	s = c.getIncludeDirs ();
	std::cout << "incdirs= " << s << std::endl;

	return 0;

}

#ifdef ComponentData_MAIN
int main(int argc, char *argv[])
{
	return ::sandia::support::ComponentData::main(argc, argv);
}
#endif
