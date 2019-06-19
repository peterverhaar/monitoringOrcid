from config import *
from orcidData import *
import urllib.request
import xml.etree.ElementTree as ET
import lxml.etree as ET
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


orcids = dict()

def findOrcids(url):
    token = 200
    attempts = 0
    numFound = 0

    url += '&rows=' + str(token)

    print( url )
    try:
        root = getTree( url )
        numFound = int( root.attrib['num-found'] )
        print( str(numFound) + ' orcid Ids found.' )

        for result in root.findall('s:result' , ns ):
            orcidId = result.find('c:orcid-identifier/c:path' , ns ).text
            orcids[  orcidId ] = orcids.get( orcidId , 0 ) + 1
    except:
        print('Url cannot be accessed!')


    while numFound > token:
        token += 1
        try:
            if attempts < 10:
                url2 = url + '&start=' + str( token )
                print(url2)
                root = getTree( url2 )
                for result in root.findall('s:result' , ns ):
                    orcidId = result.find('c:orcid-identifier/c:path' , ns ).text
                    orcids[  orcidId ] = orcids.get( orcidId , 0 ) + 1
                token += 200
        except:
            print('Url cannot be accessed!')
            # the num-found appears to give the wrong information occassionally
            # the process terminates after 10 failed attempts
            attempts += 1




baseUrl = 'https://pub.orcid.org/v3.0/search/'

url = f'{ baseUrl }?q=email:*{ urlEncode(domain) }*'
findOrcids( url )

url = f'{ baseUrl }?q=ringgold-org-id:{ ringgoldId }'
findOrcids( url )

url = f'{ baseUrl }?q=affiliation-org-name:*{ urlEncode(institutionName) }*'
findOrcids( url )

url = f'https://pub.orcid.org/v3.0/search/?q=grid-org-id:{ gridId }'
findOrcids( url )

print( f'{len(orcids)} found.\n' )



out = open( 'orcids.csv' , 'w' )
out.write( 'lastName,firstName,orcid,creationDate,nrWorks,organisation1,department1,organisation2,department2\n' )


def readOrcidRecord( o ):
    #print( o )
    data = dict()
    apiRequest = 'https://pub.orcid.org/v3.0/' + o + '/record'

    try:
        tree = getTree( apiRequest )
        data['lastName'] = getLastName( tree )
        data['firstName'] = getFirstName( tree )
        data['creationDate'] = getCreationDate( tree )
        data['nrWorks'] = getNumberOfWorks( tree )
        aff = getAffiliations( tree )

        out.write( f"{ data.get('lastName' , '' ) }," )
        out.write( f"{ data.get('firstName' , '' ) }," )
        out.write( f"{ o }," )
        out.write( f"{ data.get('creationDate' , '' ) }," )
        out.write( f"{ data.get('nrWorks' , '' ) }," )

        if len(aff) > 0:
            out.write( f"{ aff[0][0] }," )
            out.write( f"{ aff[0][1] }," )
        else:
            out.write( ',,')

        if len(aff) > 1:
            out.write( f"{ aff[1][0] }," )
            out.write( f"{ aff[1][1] }\n" )
        else:
            out.write( ',\n')



    except:
        print(f'{o}: Orcid account could not be accessed.')

count = 0
for o in orcids:

    count += 1
    print( f'{count}/{len(orcids)}' )
    readOrcidRecord( o )


out.close()
