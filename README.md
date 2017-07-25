Notre Dame Student Networks
===========================

**full\_netid.txt** : 

List of NetIDs of all students, faculty, and staff associated with Notre Dame. 
Contains invalid IDs. 

        $ cat /afs/nd.edu/common/etc/passwd | grep -E /afs/nd.edu | grep -Ev ^esqa | cut -d ':' -f 1 | sort | uniq > netid.txt


**req\_students.py**: 

Script that uses the NetIDs in the file "full\_netid.txt" to make requests to the 
ND Enterprise Directory Service using multiprocessing. Processes return a list 
containing the JSON data for each member of ND. JSON encodes the list into JSON 
data and is written to the file "ND\_directory.json".


**ND\_directory.json**:

JSON file of information from the ND Enterprise Directory Service for all valid
NetIDs.


**open\_directory.py**:

Script that uses the JSON data in "ND\_directory.json"


Things to complete
---------------------

- modify Labels for node to interface with mpld3 
