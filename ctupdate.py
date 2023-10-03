import requests
import json
import cred
import pprint
# Set the request parameters

url = f'https://liberty.service-now.com/api/now/table/new_call?sysparm_query=groupDYNAMICd6435e965f510100a9ad2572f2b47744^EQ&sysparm_fields=u_name%2Csys_id%2Cshort_description%2Ccmdb_ci%2Ccomments%2Cu_kb%2Cu_call_type%2Cu_queue%2Cu_firstcall_resolution%2Cactive%2Cgroup'

# url = f'https://liberty.service-now.com/api/now/table/new_call?sysparm_fields=name%2Csys_id%2Cshort_description%2Ccmdb_ci%2Ccomments%2Cu_kb%2Cu_call_type%2Cu_queue%2Cu_firstcall_resolution%2Cactive%2Cgroup'

# url = f'https://liberty.service-now.com/api/now/table/sys_template?sysparm_query=active%3Dtrue&sysparm_fields=name%2Csys_id%2Cshort_description%2Ccmdb_ci%2Ccomments%2Cu_kb%2Cu_call_type%2Cu_queue%2Cu_firstcall_resolution%2Cactive%2Cgroup'
#?&sysparm_fields=name%2Csys_id%2Cshort_description%2Ccmdb_ci%2Ccomments%2Cu_kb%2Cu_call_type%2Cu_queue%2Cu_firstcall_resolution%2C
# Eg. User name="admin", Password="admin" for this code sample.
usr = cred.usr
pwd = cred.pwd

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(usr, pwd), headers=headers )

# Check for HTTP codes other than 200
if response.status_code != 200:
	print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
	exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
pprint.pprint(data)
