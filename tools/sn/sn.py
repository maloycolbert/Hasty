#Need to install requests package for python
#easy_install requests
import requests
import json
import cred
import argparse
try:
	import call_templates
except ImportError:
	import tools.sn.call_templates as call_templates
try:
	import transfer_list
except ImportError:
	import tools.sn.transfer_list as transfer_list

#Define Globals
call_doc = {}

def post():
	#Call globals
	global call_doc

	# Set the request parameters
	url = 'https://liberty.service-now.com/api/now/table/new_call?sysparam_fields=number'

	# Eg. User name="admin", Password="admin" for this code sample.
	usr = cred.usr
	pwd = cred.pwd

	# Set proper headers
	headers = {"Content-Type":"application/json","Accept":"application/json"}

	#Clean up call_doc formatting before making POST
	for k, v in call_doc.items():
		if v is None:
			call_doc[k] = ''
	#print(call_doc)

	call_doc['state'] = 1

	# Do the HTTP request
	response = requests.post(url, auth=(usr, pwd), headers=headers ,data=json.dumps(call_doc))

	# Check for HTTP codes other than 200
	#if response.status_code != 200:
	#	print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
	#	exit()

	# Decode the JSON response into a dictionary and use the data
	data = response.json()
	#print(json.dumps(data, indent=4, sort_keys=True))

	return data

def parse():
	#Call globals
	global call_doc

	parser = argparse.ArgumentParser(description='Create Serivce Now documentation')
	parser.add_argument('-t', '--template', help="Template for call", dest='u_template')
	parser.add_argument('-u', '--username', help="Caller's username", dest="u_username")
	parser.add_argument('-c', '--caller', help="Caller's `sys_user` ID. This is automatically retrieved when username is specified.", dest="u_caller")
	parser.add_argument('-i', '--id-number', help="Caller's LU ID", dest="u_id_number")
	parser.add_argument('-p', '--phone', help="Caller's phone number", dest="u_phone_number")
	parser.add_argument('-d', '--department', help="Caller's department", dest="u_department")
	parser.add_argument('-S', '--student-type', help="If caller is a student, the type of student e.g. Alumni, Online", dest="u_student_type")
	parser.add_argument('-I', '--configuration-item', help="Call configuration item", dest="cmdb_ci")
	parser.add_argument('-a', '--assigned-to', help="Agent who opened called", dest="assigned_to")
	parser.add_argument('-W', '--time-worked', help="Length of call", dest="time_worked")
	parser.add_argument('-q', '--queue', help="Queue call originated from", dest="u_queue")
	parser.add_argument('-T', '--call-type', help="Type of call", dest="call_type")
	parser.add_argument('-O', '--operating-system', help="Caller's operating system", dest="u_operating_system")
	parser.add_argument('-D', '--short-description', help="Short description of call", dest="short_description")
	parser.add_argument('-w', '--work-notes', help="Call documentation", dest="work_notes")
	parser.add_argument('-C', '--comments', help="Call comments to be sent to user", dest="comments")
	parser.add_argument('-k', '--used-kb', help="Was a KB used? Boolean", dest="u_used_kb")
	parser.add_argument('-R', '--used-remote', help="Was remote assistance used? Boolean", dest="u_webex")
	parser.add_argument('-F', '--First-call', help="Was resolution acheived on the first call? Boolean", dest="u_firstcall_resolution")
	parser.add_argument('-x', '--Transfer', help="Was the called transfered? Boolean", dest="u_transfer")
	parser.add_argument('-X', '--Transfer-Internal', help="Was the call transferred internally (to HD?) Boolean", dest="u_transfer_internal")
	parser.add_argument('-2', '--Transfer-to', help="To whom was the called transferred to?", dest="u_transfer_list")
	parser.add_argument('-Q', '--Transfer-queue', help="If an internal transfer, which queue was it transferred to?", dest="u_transfer_queue")
	parser.add_argument('-z', '--Complaint', help="Was this call a complaint?", dest="u_complaint")
	parser.add_argument('-Z', '--Complaint-comments', help="Comments for the complaint.", dest="u_complaint_comments")
	parser.add_argument('-P', '--Parent', help="Parent (related tkt)", dest="parent")

	call_doc = vars(parser.parse_args())

def get_user():
	#Call globals
	global call_doc

	username = call_doc['u_username']

	# Set the request parameters
	url = f'https://liberty.service-now.com/api/now/table/sys_user?sysparm_query=user_name%3D{username}&sysparm_fields=sys_id%2Cdepartment%2Cphone'

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
	print(data)

	# Set applicable data
	try:
		call_doc['u_caller'] = data['result'][0]['sys_id']
		try:
			if data['result'][0]['department']['value'] is not '':
				call_doc['u_department'] = data['result'][0]['department']['value']
		except TypeError:
			call_doc['u_department'] = "Student"
		if data['result'][0]['phone'] is not '':
			call_doc['u_phone_number'] = data['result'][0]['phone']

	except IndexError:
		call_doc['u_username'] = 'ithelpdesk'
		get_user()


def get_tkt():
	call_doc['parent'] = call_doc['parent']
	# global call_doc
	#
	# tkt = call_doc['parent']
	#
	# url = f'https://liberty.service-now.com/api/now/table/ticket?sysparam_query=number%3D{tkt}&sysparam_field=sys_id'
	# #url = f'https://libertydev.service-now.com/api/now/table/ticket?sysparam_query=number%3D{tkt}&sysparam_field=sys_id'
	#
	# usr = cred.usr
	# pwd = cred.pwd
	#
	# headers = {"Content-Type":"application/json","Accept":"application/json"}
	# response = requests.get(url, auth=(usr, pwd), headers=headers )
	#
	# if response.status_code != 200:
	# 	print('Status:', response.status_code, 'Headers:', response.headers, 'Erro Response:', response.json())
	# 	exit()
	#
	# data = response.json()
	# print(data)
	#
	# call_doc['parent'] = data['result'][0]['number']

def template():
	templates = call_templates.templates
	template = call_doc['u_template']
	try:
		call_doc['cmdb_ci'] = templates[template]['cmdb_ci']
	except Keyerror:
		call_doc['cmdb_ci'] = ''
	call_doc['short_description'] = templates[template]['short_description']
	try:
		call_doc['comments'] = templates[template]['comments']
	except KeyError:
		call_doc['comments'] = ''
	call_doc['u_template'] = templates[template]['sys_id']
	if 'u_kb' in templates[template]:
		call_doc['u_used_kb'] = templates[template]['u_kb']
	if 'u_call_type' in templates[template]:
		call_doc['call_type'] = templates[template]['u_call_type']
	if 'u_queue' in templates[template]:
		call_doc['u_queue'] = templates[template]['u_queue']
	if 'u_transfer_internal' in templates[template]:
		call_doc['u_transfer_internal'] = templates[template]['u_transfer_internal']
	if 'u_transfer_queue' in templates[template]:
		call_doc['u_transfer_queue'] = templates[template]['u_transfer_queue']

	#Options from GUI
	if 'u_firstcall_resolution' in templates[template]:
		call_doc['u_firstcall_resolution'] = templates[template]['u_firstcall_resolution']
	if 'u_transfer' in templates[template]:
		call_doc['u_transfer'] = templates[template]['u_transfer']



	if 'u_transfer_internal' in templates[template]:
		call_doc['u_transfer_internal'] = templates[template]['u_transfer_internal']
	if 'u_transfer_queue' in templates[template]:
		call_doc['u_transfer_queue'] = templates[template]['u_transfer_queue']


def external_transfer():
	dept_list = transfer_list.transfer_external
	dept = call_doc['u_transfer_list']
	call_doc['u_transfer_list'] = dept_list[dept]
	call_doc['u_transfer'] = True

def internal_transfer():
	call_doc['u_transfer_list'] = "9916ce750a0a3c9e01bc78b1c8da0678"
	call_doc['u_transfer'] = True
	call_doc['u_transfer_internal'] = True

def main():
	get_user()
	if call_doc['parent'] is not None:
		get_tkt()
	if call_doc['u_template'] is not None:
		template()
	if call_doc['u_transfer_list'] is not None:
		external_transfer()
	if call_doc['u_transfer_queue'] is not None:
		internal_transfer()
	data = post()
#	print(json.dumps(data, indent=4, sort_keys=True))
	call_number = data['result']['number']
	print(call_number)

def fromGUI(doc):
	global call_doc
	call_doc = doc
	main()

if __name__ == "__main__":
	parse()
	main()
