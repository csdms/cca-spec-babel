#ifndef __sandia_support_ComponentData_hpp
#define __sandia_support_ComponentData_hpp

#include <string>
#include <vector>
#include <iostream>
#include <map>
#include <exception>

#include <boost/smart_ptr.hpp>


namespace sandia {
namespace support {

class ComponentData;
typedef boost::shared_ptr< ComponentData > ComponentData_shared;

/* Looks exactly like opq componentclassdescription, but not bound to 
 * ccaffeine exceptions or any particular cca spec binding.
 */
class ComponentData {

public:

  ComponentData() ;
  virtual ~ComponentData() ;

  virtual std::string getComponentClassName () throw (std::exception) ;
  virtual std::string getDeploymentClassAlias() throw (std::exception);
  virtual std::string getConstructorName () throw (std::exception) ;
  virtual std::string getCCASpecBinding() throw (std::exception);
  virtual std::string getLibraryLoading() throw (std::exception);
  virtual std::string getLibraryLocation() throw (std::exception);
  virtual std::string getLibraryName () throw (std::exception);
  virtual std::string getStaticLibraryName () throw (std::exception);
  virtual std::string getSharedLibraryName () throw (std::exception);
  virtual std::string getLibtoolLibraryName () throw (std::exception);
  virtual std::string getExecScript () throw (std::exception);
  virtual std::string getIndexFile() throw (std::exception);
  virtual std::string getIncludeDirs() throw (std::exception);
  virtual std::string getIncludeFiles() throw (std::exception);
  virtual void getDOMTree () throw (std::exception);

  static int main(int argc, char **argv);
  
  void setComponentClassName( std::string s);
  void setDeploymentClassAlias( std::string s);
  void setConstructorName( std::string s);
  void setCCASpecBinding( std::string s);
  void setLibraryLoading( std::string s);
  void setLibraryLocation( std::string s);
  void setLibraryName( std::string s);
  void setSharedLibraryName( std::string s);
  void setStaticLibraryName( std::string s);
  void setLibtoolLibraryName( std::string s);
  void setExecScript( std::string s);
  void setIndexFile( std::string s);
  void setIncludeDirs( std::string s);
  void setIncludeFiles( std::string s);

private:
  unsigned int dead;
  std::string componentClassName;
  std::string deploymentClassAlias;
  std::string ccaSpecBinding;
  std::string libraryLoading;
  std::string libraryLocation;
  std::string libraryName;
  std::string libraryNameLibtool;
  std::string libraryNameStatic;
  std::string libraryNameShared;
  std::string execScript;
  std::string ctorName;
  std::string indexFile;
  std::string incdirs;
  std::string incfiles;

  void initDummy();

};

} // end namespace support
} // end namespace sandia
#endif // __sandia_support_ComponentData_hpp
