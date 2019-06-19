# monitoringOrcid

# Synopsis

The code in this repository can be used collect all the Orcid IDs associated with a specific academic institution. The data can be collected in two ways:

1. 'findOrcids.py' can be used to query the ORCID database, using the 3.0 version of the ORCID API. The ORCID database can be queries using the grid ID, the Ringgold ID, the name or the mail domain. The values to be used in these queries firstly need to be defined in the file 'config.py'. The code creates a csv file with the last name, the first name, the ORCID id, the creation date, the number of works and affiliation information. If the number of ORCID ids that are found is very large, running this code may take quite a long time.

2. 'orcidNameSearch.py' can be used to query the ORCID database on the basis of a list of names. The names of all the researchers to be checked firstly needs to be stored in an Excel file named "researchers.xlsx". This Excel file needs to contain a sheet called "Sheet1", and this sheet needs to contain columns named "firstName" and "lastName". The code can be used to check whether the researchers listed in the Excel sheet have claimed an ORCID id. It produced a CSV file listing the first three results of the name search API. After it has been created, the CSV file needs to be edited manually; incorrect results need to be removed. 


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

Usage of orcidNameSearch.py:

1. Create an Excel sheet listing the names of all the researchers active at your university. SUch a list can usually be obtained from the HR department. 
2. Run the code in the Command line: 'python orcidNameSearch.py'

