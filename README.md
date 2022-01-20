# sokqlovia
Azure Resource Graph Helper

Usage:
```
 ____        _         _            _       
/ ___|  ___ | | ____ _| | _____   _(_) __ _ 
\___ \ / _ \| |/ / _` | |/ _ \ \ / / |/ _` |
 ___) | (_) |   < (_| | | (_) \ V /| | (_| |
|____/ \___/|_|\_\__, |_|\___/ \_/ |_|\__,_|
                    |_|                     

usage: sokqlovia.py [-h] [-x] [-o OUTFILE] [-c CUSTOM_QUERY] [-d] [-s SAVED_QUERY] [-p P]

optional arguments:
  -h, --help       show this help message and exit
  -x               Demo Query. i.e. outputs results of query saved in testquery()
  -o OUTFILE       Override default output file/path. Default is sokqlovia_output.csv in cwd
  -c CUSTOM_QUERY  Quote encapsulated KQL query to be executed
  -d               Displays List of Pre-define templates for use with -t flag
  -s SAVED_QUERY   Select Saved Query by ID, provide param -p for positional argument
  -p P             Parameter needed. Used in conjuction with -S ```



Saved Queries in stored_queries.json

example format

    {
      "QueryID": "2",
      "QueryName": "AllVms_orderDesc",
      "ShortDescription": "Output all Compute VMs",
      "KQL": "Resources | where type =~ 'Microsoft.Compute/virtualMachines' | project id, name, location, resourceGroup, properties.storageProfile.osDisk.osType | order by id desc",
      "PositionalArg": "N"
    }
    
 for a query requiring positional argument. <soklovia> is used for substition
  
      {
      "QueryID": "4",
      "QueryName": "Find_By_Hostname",
      "ShortDescription": "Find Resource by Hostname",
      "KQL": "Resources | where name =~ '<sokqlovia>'",
      "PositionalArg": "Y"
    }
