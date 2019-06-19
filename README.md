# monitoringOrcid

# Synopsis

The code in this repository can be used collect ORCID IDs associated with a specific academic institution. The data can be collected in two ways:

1. 'findOrcids.py' can be used to query the ORCID database on the basis of a grid ID, a Ringgold ID, the name of the institution or a mail domain. The values to be used in these queries firstly need to be defined in the file 'config.py'. 

2. 'orcidNameSearch.py' can be used to query the ORCID database on the basis of a list of names. The names of all the researchers to be checked firstly needs to be stored in an Excel file named "researchers.xlsx". The code checks whether the researchers listed in the Excel sheet have claimed their ORCID id. It firstly searches exactly using the 'family-name' and the 'given-names' parameters. If this query does not yield any results, the code searches more broadly using the full name. In the latter case, the code returns the first three results of the name search query.

The code makes use of the 3.0 version of the ORCID Api.
More information can be found at https://members.orcid.org/api/resources/find-myresearchers 


# Dependencies


The code makes use of the following libraries and modules:
- urllib.request
- xml.etree.ElementTree 
- re
- pandas

# Tests

Usage of findOrcid.py:

1. Edit the config.py file, and provide the GRID id, the RINGGold Id, the name of the institution and the mail domain.
2. Run the code in the Command line: 'python findOrcid.py'

The code creates a csv file with the last name, the first name, the ORCID id, the creation date, the number of works and affiliation information. If the number of ORCID ids that are found is very large, running this code may take quite a long time. 

Usage of orcidNameSearch.py:

1. Create an Excel sheet listing the names of all the researchers active at your university. Such a list can usually be obtained from the HR department. This Excel file needs to be named 'researchers.xlsx', and it needs to contain a sheet called "Sheet1". This sheet needs to contain columns named "firstName" and "lastName". Save the Excel file in the same directry as the code.
2. Run the code in the Command line: 'python orcidNameSearch.py'

'orcidNameSearch.py' produces a CSV file listing the ORCID IDs that were found. The CSV file may contain incorrect results; these can be removed manually. 

