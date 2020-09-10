# azure-instance-auditor
How many instances are running in each region, grouped by name.

This takes inputs of Azure app credentials of app_client_id, app_client_secret, app_tenant_id, scans through all Azure regions, and will output the total number in each region, and number of each unique instance name.

**Usage:**  
The cred_file is azure credential file.Put the cred.json at the same directory as the audit.py is located before running the docker cli in the next step\
For additional control, the audit.py script can also take in client id/secret/tenant id. the credentials must be corresponding with the environment (dev/prod)

optional arguments:  \
 -h, --help                      show this help message and exit\
 --client-id CLIENT_ID           (if chose to input manually/do not need the CRED_FILE flag)\
 --client-secret CLIENT_SECRET   (if chose to input manually/do not need the CRED_FILE flag)\
 --tenant-id TENANT_ID           (if chose to input manually/do not need the CRED_FILE flag)\
 --env ENV                       azure environment (prod or dev). \
 --cred-file CRED_FILE           credential file. \
 --verbose                       verbose output. 


**Examples:(local)**  
`docker build --tag name_of_auditor .`

`docker run name_of_auditor  --cred-file CRED_FILE --verbose` 

**Examples:(dockerhub)**
`docker run --rm -t -v ~/Downloads/cred.json:/root/cred.json:ro signiant/azure-instance-auditor --cred-file /root/cred.json --verbose`

output:\
`(if verbose vm will be listed by region follow by) 
Total number of VM in prod Azure environment: 19`
