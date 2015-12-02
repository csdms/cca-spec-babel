from xml.dom import minidom

class CCAXMLEntity (object):
    def __init__(self):
        self.kind = ''
        self.deploymentXML = None
    
    def generateXML(self):
        pass
    
    def getXMLRep(self):
        return self.deploymentXML.toprettyxml(indent="   ")
    
    def writeXMLRep(self, fileName):
        return

