# azure-instance-auditor
How many instances are running in each region, grouped by name.

This takes inputs of Azure app credentials of app_client_id, app_client_secret, app_tenant_id, scans through all Azure regions, and will output the total number in each region, and number of each unique instance name.

**Usage:**  
The cred_file is under secret server. Look for 'Azure credential to execute vm-audit-application' \
The script can take in client id/secret/tenant id or the credential file. You must specify the environment (dev/prod)

optional arguments:  \
-h, --help            show this help message and exit\
--env ENV             azure environment (prod or dev). \
--cred-file CRED_FILE.
                    credential file. \
--verbose             verbose output. 


**Examples:**  
`docker build --tag name_of_auditor .`

`docker run name_of_auditor  --cred-file CRED_FILE --verbose` 

output:\
`Total number of VM in prod Azure environment: 19`
