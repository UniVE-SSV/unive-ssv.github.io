#########################################################################################
#                                                                                       #
# Script to auto-update publications, people, and news for the ssv website.             #
# This script pulls data from ORCID using their public APIs. To use them, it            #
# is necessary to define an application that can interact with the APIs.                #
#                                                                                       #
# Follow the insructions at https://info.orcid.org/documentation/features/public-api/   #
# to generate an application, and retrieve its ID and SECRET.                           #
#                                                                                       #
# The, use the following command to generate a token for using the API:                 #
# curl -i -L -H 'Accept: application/json' -d 'client_id=[APP ID]' -d 'client_secret=[APP SECRET]' -d 'scope=/read-public' -d 'grant_type=client_credentials' 'https://orcid.org/oauth/token'
#                                                                                       #
# The response will have the following structure:                                       #
# {                                                                                     #
#   "access_token": "[ACCESS_TOKEN]",                                                   #
#   "token_type": "bearer",                                                             #
#   "refresh_token": "[REFRESH_TOKEN]",                                                 #
#   "expires_in": [EXPIRATION],                                                         #
#   "scope": "/read-public",                                                            #
#   "orcid":null                                                                        #
# }                                                                                     #
# Note that the access token lasts ~20 years.                                           #
#                                                                                       #
# You can then use the generated access token as argument for this script:              #
# python3 orcid-crawl.py [ACCESS_TOKEN]                                                 #
#                                                                                       #
# The script will use such token to issue requests to the ORCID web API:                #
# https://github.com/ORCID/ORCID-Source/tree/main/orcid-api-web                         #
#                                                                                       #
# This script works by taking information out of the 'users.yaml' file located          #
# in the same directory. Such a file should be split in two sections, each              #
# containing a list of user information with <orcid, photo, from, to, student> where    #
# - <orcid> is the user's identifiaction number on ORCID                                #
# - <photo> is the filename of the image living under website_root/images/ to           #
#   use as profile picture for them                                                     #
# - <from> is the date (YYYY-MM-DD) when they joined the lab, used to filter out        #
#   publications published before they joined                                           #
# - <to> is the date (YYYY-MM-DD) when they left the lab, used to filter out            #
#   publications published after they joined (if they are still part of the lab,        #
#   'today' can be used)                                                                #
# - <student> is either 'yes' or 'no' and forces the role to PhD student                #
#                                                                                       #
# An example file is:                                                                   #
# users:                                                                                #
#   - id: 0000-0000-0000-0000                                                           #
#     photo: img1.png                                                                   #
#     from: 2019-01-01                                                                  #
#     to: today                                                                         #
#     student: no                                                                       #
#   - id: 0000-0000-0000-0001                                                           #
#     photo: img2.png                                                                   #
#     from: 2019-09-15                                                                  #
#     to: today                                                                         #
#     student: yes                                                                      #
# past_users:                                                                           #
#   - id: 0000-0000-0000-0002                                                           #
#     photo: img3.png                                                                   #
#     from: 2019-09-01                                                                  #
#     to: 2021-09-30                                                                    #
#     student: no                                                                       #
# external_users:                                                                       #
#   - id: 0000-0000-0000-0003                                                           #
#     photo: img4.png                                                                   #
#     from: 2019-09-01                                                                  #
#     to: 2021-09-30                                                                    #
#     student: no                                                                       #
#                                                                                       #
# The script then will:                                                                 #
# - fill up '../people.md' with the info crawled for each entry in 'users',             #
#   'past_users' and 'external_users', placing them in their respective sections        #
# - fill up '../publications.md' with works from both present and past users that       #
#   were published within the time window of at least one of the autors (to avoid       #
#   duplicates, we discriminate publications based on DOI)                              #
# - generate the includes/index_people.html page with the updated photos of all         #
#   and external members, but not the past ones                                         #
#                                                                                       #
#########################################################################################

import requests
import json
import yaml
import sys
from datetime import *
import hashlib
import os
import shutil

class User:
	def __init__(self, name, surname, photo, mail, website, role, org, bio, raw_works):
		self.name = name.title() if name is not None else None
		self.surname = surname.title() if surname is not None else None
		self.photo = photo
		self.mail = mail
		self.website = website
		self.role = role.title() if role is not None else None
		self.org = org.title() if org is not None else None
		self.bio = bio
		self.raw_works = raw_works

	def dump(self):
		with open('templates/single-member.template', 'r') as file:
			content = file.read()
		position = f'{self.role} @ {self.org}' if self.role is not None and self.org is not None else ''
		email = f'Email: <a href="mailto:{self.mail}">{self.mail}</a><br/>' if self.mail is not None else ''
		website = f'Website: <a href="{self.website}">{self.website}</a>' if self.website is not None else ''
		bio = f'{self.bio}' if self.bio is not None else ''
		return content.replace('${PHOTO}', self.photo) \
					.replace('${NAME}', self.name) \
					.replace('${SURNAME}', self.surname) \
					.replace('${POSITION}', position) \
					.replace('${EMAIL}', email) \
					.replace('${WEBSITE}', website) \
					.replace('${BIO}', bio)

class Pub(yaml.YAMLObject):
	yaml_tag = u'!Publication'
	def __init__(self, workid, title, pub_date, where, doi, url, contribs):
		self.workid = workid
		self.title = title
		self.pub_date = pub_date
		self.venue = where
		self.doi = doi
		self.url = url
		self.contribs = contribs

	def dump(self):
		authors = ', '.join(self.contribs)
		link = f' [[LINK]]({self.url})' if self.url is not None else ''
		return f'{authors}: _"{self.title}"_, in {self.venue} [[DOI]](https://doi.org/{self.doi}){link}'

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		authors = ', '.join(self.contribs)
		link = f'\nLINK: {self.url}' if self.url is not None else ''
		return f'''AUTHORS: {authors}
TITLE: _"{self.title}"_
IN: {self.venue}
DOI: https://doi.org/{self.doi}{link}'''

	def __eq__(self, other):
		return isinstance(other, Pub) and self.workid == other.workid

def log(*messages):
	if verbose:
		print(*messages)

def query_api(access_token, user_id, method, do_log=False):
	return query_path(access_token, '/' + user_id + '/' + method, do_log)

def query_path(access_token, path, do_log=False):
	headers_dict = {
		'Accept': 'application/vnd.orcid+json',
		'Authorization':'Bearer ' + access_token
	}
	response = requests.get('https://pub.orcid.org/v3.0' + path, headers=headers_dict)
	if do_log:
		log('## Result of querying', path, '##')
		log(response.text)
	return json.loads(response.text)

def access_field(accessor, element, field, default=None, do_log=True):
	try:
		el = accessor(element)
		if do_log:
			log('\t' + field + ':', el)
		return el
	except Exception as e:
		log('\tUnable to retrieve value for', field, ', will use default value', default, '. Reason:', str(e))
		return default

def parse_user(access_token, user):
	user_id = user['id']
	print('Processing', user_id)

	record = query_api(access_token, user_id, 'person')
	name = access_field(lambda r: r['name']['given-names']['value'], record, 'name')
	surname = access_field(lambda r: r['name']['family-name']['value'], record, 'surname')
	bio = access_field(lambda r: r['biography']['content'], record, 'bio')
	mail = access_field(lambda r: r['emails']['email'][0]['email'], record, 'mail')
	website = access_field(lambda r: r['researcher-urls']['researcher-url'][0]['url']['value'], record, 'website')

	record = query_api(access_token, user_id, 'activities')

	if user['student']:
		log('\tForcing role to PhD Student')
		role = 'PhD Student'
		org = 'Università Ca\' Foscari Venezia'
	else:
		role = access_field(lambda r: r['employments']['affiliation-group'][0]['summaries'][0]['employment-summary']['role-title'], record, 'role')
		org = access_field(lambda r: r['employments']['affiliation-group'][0]['summaries'][0]['employment-summary']['organization']['name'], record, 'org')

	raw_works = access_field(lambda r: r['works']['group'], record, 'works', default=list(), do_log=False)
	return User(name, surname, user['photo'], mail, website, role, org, bio, raw_works)

def parse_work(access_token, owner, min_date, max_date, work, publications_list, excluded_publications, incomplete_publications):
	path = access_field(lambda r: r['work-summary'][0]['path'], work, 'work path', do_log=False)
	if any(path == pub.workid for pub in publications_list):
		print(f'Publication {path} already in the database')
		return
	if path in excluded_publications:
		print(f'Publication {path} is in the database of excluded publications')
		return
	incomplete = False
	in_incomplete = (path in incomplete_publications)

	workrecord = query_path(access_token, path, do_log=False)
	title = access_field(lambda r: r['title']['title']['value'], workrecord, 'title', do_log=False)
	print('Processing', title)
	if incomplete:
		print(f'\tPublication is in the database of incomplete publications, trying to parse it again')

	creation_raw = access_field(lambda r: r['created-date']['value'], workrecord, 'creation')
	year_raw = access_field(lambda r: r['publication-date']['year']['value'], workrecord, 'year')
	month_raw = access_field(lambda r: r['publication-date']['month']['value'], workrecord, 'month')
	day_raw = access_field(lambda r: r['publication-date']['day']['value'], workrecord, 'day')

	year = int(year_raw) if year_raw is not None else None
	month = int(month_raw) if month_raw is not None else 1
	day = int(day_raw) if day_raw is not None else 1

	if year is not None:
		pub_date = date(year, month, day)
	elif creation_raw is not None:
		log('\tMissing date, using creation timestamp instead')
		# according to the docs, creation_raw should contain a formatted ISO timestamp
		# but it seems that it instead contains the milliseconds relative to EPOCH.
		# should this stop working, we need to investigate a new workaround
		pub_date = date(1970, 1, 1) + timedelta(milliseconds=creation_raw)
		log('\t\tProduced date: ' + str(date))
	else:
		# we do not exclude it permanently since it might get updated in the future
		print('\tMissing publication date')
		if not in_incomplete:
			incomplete_publications[path] = (owner, title, set())
			in_incomplete = True
		incomplete = True
		incomplete_publications[path][2].add('publication date')

	if pub_date < min_date or pub_date > max_date:
		print('\tPublication discarded since it is outside of the specified date range')
		excluded_publications += [path]
		return

	where = access_field(lambda r: r['journal-title']['value'], workrecord, 'venue')
	if where is not None:
		where = where.replace("'", "")
	url = access_field(lambda r: r['url']['value'], workrecord, 'url')
	doi = None
	extids = access_field(lambda r: r['external-ids']['external-id'], workrecord, 'external ids', default=list(), do_log=False)
	if extids is not None:
		for extid in extids:
			if access_field(lambda r: r['external-id-type'], extid, 'external id type', do_log=False) == 'doi':
				doi = access_field(lambda r: r['external-id-value'], extid, 'external id')
				break
	contribs = list()
	for contributor in access_field(lambda r: r['contributors']['contributor'], workrecord, 'contributors', default=list(), do_log=False):
		contribs += [access_field(lambda r: r['credit-name']['value'], contributor, 'contributor name')]

	if doi is None:
		# we do not exclude it permanently since it might get updated in the future
		print('\tMissing doi')
		if not in_incomplete:
			incomplete_publications[path] = (owner, title, set())
			in_incomplete = True
		incomplete = True
		incomplete_publications[path][2].add('doi')
	if where is None:
		# we do not exclude it permanently since it might get updated in the future
		print('\tMissing journal/conference')
		if not in_incomplete:
			incomplete_publications[path] = (owner, title, set())
			in_incomplete = True
		incomplete = True
		incomplete_publications[path][2].add('journal/conference')
	if contribs is None or len(contribs) < 1:
		# we do not exclude it permanently since it might get updated in the future
		print('\tMissing authors')
		if not in_incomplete:
			incomplete_publications[path] = (owner, title, set())
			in_incomplete = True
		incomplete = True
		incomplete_publications[path][2].add('authors')
	if incomplete:
		print('\tPublication discarded due to missing fields')
		return
	elif in_incomplete:
		# this was previously in incomplete_publications, but now we found all fields
		# and we can remove it from the database
		del incomplete_publications[path]
	
	if any(doi == pub.doi for pub in publications_list):
		print('\tPublication discarded due to duplicate doi')
		excluded_publications += [path]
		return

	publication = Pub(path, title, pub_date, where, doi, url, contribs)
	publications_list += [publication]

def populate_publications_page(publications):
	with open('../publications.md', 'w') as file:
		file.write('''---
layout: page
title: Publications
---
''')
		curryear = None
		for publication in publications:
			year = publication.pub_date.year
			if curryear is None:
				curryear = year
				file.write(f'## {curryear}\n\n')
			elif year != curryear:
				curryear = year
				file.write(f'## {curryear}\n\n')

			log('Adding', publication.title, 'to the Publications page')
			file.write(publication.dump() + '\n\n')

def populate_people_page(people, past_people, external_people):
	with open('../people.md', 'w') as file:
		file.write('''---
layout: page
title: People
---
''')
		for person in people:
			log('Adding', person.name, person.surname, 'to the People page')
			file.write(person.dump())
		if len(external_people) > 0:
			file.write('## External members\n')
			for person in external_people:
				log('Adding', person.name, person.surname, 'to the People page')
				file.write(person.dump())
		if len(past_people) > 0:
			file.write('## Past members\n')
			for person in past_people:
				log('Adding', person.name, person.surname, 'to the People page')
				file.write(person.dump())

def process_user_and_add(user, people_list, publications_list, excluded_publications, incomplete_publications):
	person = parse_user(access_token, user)
	if person.name is None:
		raise ValueError(f'User {person.surname} discarded due to missing name')
	elif person.surname is None:
		raise ValueError(f'User {person.name} discarded due to missing surname')
	elif person.photo is None:
		raise ValueError(f'User {person.name} {person.surname} discarded due to missing photo')
	else:
		people_list += [person]

	min_date = user['from']
	max_date = date.today() if user['to'] == 'today' else user['to']
	for work in person.raw_works:
		parse_work(access_token, f'{person.name} {person.surname}', min_date, max_date, work, publications_list, excluded_publications, incomplete_publications)

def populate_index_people(people, external_people):
	print('Populating ../_includes/index_people.html')
	with open('templates/index-people.template', 'r') as file:
		section = file.read()
	with open('templates/index-people-single.template', 'r') as file:
		person = file.read()
	with open('../_includes/index_people.html', 'w') as file:
		all_people = '\n'.join([person.replace('${PERSON_PHOTO}', p.photo) for p in people])
		all_people += '\n'
		all_people += '\n'.join([person.replace('${PERSON_PHOTO}', p.photo) for p in external_people])
		all_people += '\n'

		full_section = section.replace('${PEOPLE_FACES}', all_people)
		file.write(full_section)

if __name__ == '__main__':
	access_token = sys.argv[1]
	webhook_id = sys.argv[2]
	webhook_token = sys.argv[3]
	global verbose
	verbose = False
	if len(sys.argv) > 4 and sys.argv[4] == 'verbose':
		verbose = True

	with open('users.yaml', 'r') as yamlfile:
		data = yaml.load(yamlfile, Loader=yaml.FullLoader)
	print('Configuration read successfully')

	people = list()
	past_people = list()
	external_people = list()
	publications = list()
	excluded_publications = list()
	incomplete_publications = dict()
	
	if os.path.isfile('pub_db.yaml'):
		with open('pub_db.yaml', 'r') as yamlfile:
			print('Reading publications database')
			publications = yaml.load(yamlfile, Loader=yaml.FullLoader)
	if os.path.isfile('excluded_pub_db.yaml'):
		with open('excluded_pub_db.yaml', 'r') as yamlfile:
			print('Reading excluded publications database')
			excluded_publications = yaml.load(yamlfile, Loader=yaml.FullLoader)
	if os.path.isfile('incomplete_pub_db.yaml'):
		with open('incomplete_pub_db.yaml', 'r') as yamlfile:
			print('Reading incomplete publications database')
			incomplete_publications = yaml.load(yamlfile, Loader=yaml.FullLoader)

	old_publications = publications.copy()
	old_incomplete_publications = incomplete_publications.copy()

	for user in data['users']:
		process_user_and_add(user, people, publications, excluded_publications, incomplete_publications)

	if 'external_users' in data:
		for user in data['external_users']:
			process_user_and_add(user, external_people, publications, excluded_publications, incomplete_publications)

	if 'past_users' in data:
		for user in data['past_users']:
			process_user_and_add(user, past_people, publications, excluded_publications, incomplete_publications)

	publications = sorted(publications, key=lambda p: p.pub_date)
	populate_people_page(people, past_people, external_people)
	populate_publications_page(reversed(publications))
	populate_index_people(people, external_people)

	with open('pub_db.yaml', 'w') as yamlfile:
		print('Updating publications database')
		yamlfile.write(yaml.dump(publications))
	with open('excluded_pub_db.yaml', 'w') as yamlfile:
		print('Updating excluded publications database')
		yamlfile.write(yaml.dump(excluded_publications))
	with open('incomplete_pub_db.yaml', 'w') as yamlfile:
		print('Updating incomplete publications database')
		yamlfile.write(yaml.dump(incomplete_publications))

	webhook_url = f'https://discord.com/api/webhooks/{webhook_id}/{webhook_token}'
	new_publications = [p.dump() for p in publications if p not in old_publications]
	while len(new_publications) > 0:
		msg = "**New publications available online!**\n\n"
		while True:
			if len(new_publications) == 0 or len(msg) + len(new_publications[0]) + 2 >= 1500:
				# the webhook breaks if the message is more than 2k characters
				# just to be safe, we stay a lot below the threshold
				# the +2 is for the newlines
				break
			msg += new_publications.pop(0) + '\n\n'
		data = {
			"content": msg,
			"username": "New Papers Bot"
		}
		response = requests.post(webhook_url, json=data)
		if response.status_code == 204:
			print(f"Message sent for new publications")
		else:
			raise ValueError(f"Failed to send message for new publications (code {response.status_code}): {response.json()}")
			
	new_incomplete = [incomplete_publications[k] for k in incomplete_publications if k not in old_incomplete_publications]
	incomplete_str = [f"Owner: {pub[0]}\nPublication: _{pub[1]}_\nMissing fields: " + ', '.join(pub[2]) for pub in new_incomplete]
	while len(incomplete_str) > 0:
		msg = "**New incomplete publications found:**\n\n"
		while True:
			if len(incomplete_str) == 0 or len(msg) + len(incomplete_str[0]) + 2 >= 1500:
				# the webhook breaks if the message is more than 2k characters
				# just to be safe, we stay a lot below the threshold
				# the +2 is for the newlines
				break
			msg += incomplete_str.pop(0) + '\n\n'
		data = {
			"content": msg,
			"username": "New Papers Bot"
		}
		response = requests.post(webhook_url, json=data)
		if response.status_code == 204:
			print(f"Message sent for incomplete publications")
		else:
			raise ValueError(f"Failed to send message for incomplete publications (code {response.status_code}): {response.json()}")
