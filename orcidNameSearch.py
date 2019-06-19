
import urllib.request
import xml.etree.ElementTree as ET
import re
import pandas as pd
from orcidData import *



ns = {'o': 'http://www.orcid.org/ns/orcid' ,
's' : 'http://www.orcid.org/ns/search' ,
'h': 'http://www.orcid.org/ns/history' ,
'p': 'http://www.orcid.org/ns/person' ,
'pd': 'http://www.orcid.org/ns/personal-details' ,
'a': 'http://www.orcid.org/ns/activities' ,
'e': 'http://www.orcid.org/ns/employment' ,
'c': 'http://www.orcid.org/ns/common' }





def getData( firstName , lastName  ):

    queryName = firstName + ' ' + lastName

    fullOutput = ''

    query = f'https://pub.orcid.org/v2.1/search?q=family-name:{ urlEncode(lastName) }+AND+given-names:{ urlEncode(firstName) }'
    root = getTree( query )
    hits = root.findall('s:result' , ns )


    if len(hits) == 0:
        queryName = urlEncode( queryName )
        query = "https://pub.orcid.org/v3.0/search?q=" + queryName
        root = getTree( query )
        print(query)
        hits = root.findall('s:result' , ns )

    count = 0
    for result in hits:
        count += 1

        data = dict()
        orcidId = result.find('c:orcid-identifier/c:path' , ns ).text
        orcidUrl = "https://pub.orcid.org/v3.0/" + orcidId +  "/record"
        xml = getTree( orcidUrl )

        data['lastName'] = getLastName( xml )
        data['firstName'] = getFirstName( xml )
        data['creationDate'] = getCreationDate( xml )
        data['nrWorks'] = getNumberOfWorks( xml )
        aff = getAffiliations( xml )

        fullOutput += f"{ lastName },"
        fullOutput += f"{ firstName },"
        fullOutput += f"{ orcidId },"
        fullOutput += f"{ data.get('lastName' , '' ) },"
        fullOutput += f"{ data.get('firstName' , '' ) },"
        fullOutput += f"{ data.get('creationDate' , '' ) },"
        fullOutput += f"{ data.get('nrWorks' , '' ) },"

        if len(aff) > 0:
            fullOutput += f"{ aff[0][0] },"
            fullOutput += f"{ aff[0][1] },"
        else:
            fullOutput += ',,'

        if len(aff) > 1:
            fullOutput += f"{ aff[1][0] },"
            fullOutput += f"{ aff[1][1] }\n"
        else:
            fullOutput += ',\n'
        if count == 3:
            break

    return fullOutput


out = open( 'researchers.csv' , 'w' )
out.write( 'lastName,firstName,orcid,OrcidlastName,OrcidfirstName,creationDate,nrWorks,organisation1,department1,organisation2,department2\n' )


xl = pd.ExcelFile( 'researchers.xlsx'  )
df = xl.parse( 'Sheet1' )
for index , column in df.iterrows():
    firstName = column['firstName']
    lastName = column['lastName']
    if pd.notnull( column['lastName'] ):
        print( firstName , lastName )
        out.write( getData( firstName , lastName  ) )

out.close()
