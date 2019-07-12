
import urllib.request
import xml.etree.ElementTree as ET
import re


ns = { 's': 'http://www.orcid.org/ns/search' ,
'o': 'http://www.orcid.org/ns/orcid' ,
'h': 'http://www.orcid.org/ns/history' ,
'p': 'http://www.orcid.org/ns/person' ,
'pd': 'http://www.orcid.org/ns/personal-details' ,
'a': 'http://www.orcid.org/ns/activities' ,
'e': 'http://www.orcid.org/ns/employment' ,
'edu': 'http://www.orcid.org/ns/education' ,
'c': 'http://www.orcid.org/ns/common' }


def getTree( url):
    fp = urllib.request.urlopen( url )
    mybytes = fp.read()
    xml = mybytes.decode("utf8")
    fp.close()
    root = ET.fromstring(xml)
    return root

def getXml( url ):
    fp = urllib.request.urlopen( url )
    xml = fp.read()
    fp.close()
    return xml

def urlEncode( url ):
    url = re.sub( r'\s+' , '+' , url )
    return url.lower()

def getCreationDate( recordXml ):
    creationDate = recordXml.find('h:history/h:submission-date' , ns ).text
    return creationDate.split( "T" )[0]

def getLastName( recordXml ):
    value = ''
    lastName = recordXml.find( 'p:person/p:name/pd:family-name' , ns )
    if lastName is not None:
        value = lastName.text
    return value

def getFirstName( recordXml ):
    value = ''
    firstName = recordXml.find( 'p:person/p:name/pd:given-names' , ns )
    if firstName is not None:
        value = firstName.text
    return value

def getNumberOfWorks( recordXml ):
    works = recordXml.findall('a:activities-summary/a:works/a:group' , ns )
    nrWorks = 0 ;
    for w in works:
        nrWorks += 1
    return nrWorks

def getAffiliations( recordXml ):

    affiliations = []
    empl = recordXml.findall('a:activities-summary/a:employments/a:affiliation-group' , ns )
    eCount = 0

    for e in empl:
        orgName = ''
        departmentName = ''
        
        org = e.find( 'e:employment-summary/c:organization/c:name' , ns )
        if org is not None:
            orgName = org.text
        department = e.find( 'e:employment-summary/c:department-name' , ns )
        if department is not None:
            departmentName = department.text

        affiliations.append( (orgName , departmentName) )

    return affiliations
