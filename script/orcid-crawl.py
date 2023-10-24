# https://github.com/ORCID/ORCID-Source/tree/main/orcid-api-web

# To get access token: 
# curl -i -L -H 'Accept: application/json' -d 'client_id=[APP ID]' -d 'client_secret=[APP SECRET]' -d 'scope=/read-public' -d 'grant_type=client_credentials' 'https://orcid.org/oauth/token'

# To get APP ID and SECRET: https://info.orcid.org/documentation/features/public-api/

import requests
import json
import yaml
import sys
from datetime import *
import hashlib

with open('users.yaml', 'r') as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print('Read configuration successfully')

access_token = sys.argv[1]
api_url = 'https://pub.orcid.org/v2.1'
headers_dict = {
	'Accept': 'application/vnd.orcid+json',
	'Authorization':'Bearer ' + access_token
}

people = list()
publications = list()

for user in data['users']:
	user_id = user['id']
	print('Processing', user_id)
	response = requests.get(api_url + '/' + user_id + '/person', headers=headers_dict) 
	record = json.loads(response.text)
	name = record['name']['given-names']['value']
	surname = record['name']['family-name']['value']
	bio = record['biography']['content']
	mail = record['emails']['email'][0]['email']
	website = record['researcher-urls']['researcher-url'][0]['url']['value']

	try:
		response = requests.get(api_url + '/' + user_id + '/activities', headers=headers_dict) 
		record = json.loads(response.text)
		role = record['employments']['employment-summary'][0]['role-title']
		org = record['employments']['employment-summary'][0]['organization']['name']
	except:
		# if no employment, this is a student
		role = 'PhD Student'
		org = 'Università Ca\' Foscari Venezia'

	person = (name, surname, user['photo'], mail, website, role, org, bio)
	print(person)
	people += [person]

	mindate = user['from']
	maxdate = date.today() if user['to'] == 'today' else user['to']
	for work in record['works']['group']:		
		year = int(work['work-summary'][0]['publication-date']['year']['value'])
		if work['work-summary'][0]['publication-date']['month'] is not None:
			month = int(work['work-summary'][0]['publication-date']['month']['value'])
		else:
			month = 1
		if work['work-summary'][0]['publication-date']['month'] is not None:
			day = int(work['work-summary'][0]['publication-date']['day']['value'])
		else:
			day = 1
		pubdate = date(year, month, day)
		if pubdate < mindate or pubdate > maxdate:
			continue
		
		workresponse = requests.get(api_url + work['work-summary'][0]['path'], headers=headers_dict) 
		workrecord = json.loads(workresponse.text)

		title = workrecord['title']['title']['value']
		pubtype = workrecord['type']
		where = workrecord['journal-title']['value']
		for extid in workrecord['external-ids']['external-id']:
			#print(extid)
			if extid['external-id-type'] == 'doi':
				doi = extid['external-id-value']
				break
		contribs = list()
		for contributor in workrecord['contributors']['contributor']:
			contribs += [contributor['credit-name']['value']]
		publication = (title, pubdate, pubtype, where, doi, contribs)
		print(publication)
		publications += [publication]

def by_date(e):
	return e[1]
publications = reversed(sorted(publications, key=by_date))

with open('../people.md', 'w') as file:
	file.write("""---
layout: page
title: People
---
""")
	for person in people:
		print("Adding", person[0], person[1], "to the People page")
		file.write("""
<div class="div-person-table">
	<div class="div-person-table">
		<img class="div-person-table-col" src="{{{{ site.baseurl }}}}/images/{picture}"/>
		<div class="div-person-table-multicol">
			<h3>{name} {surname}</h3>
			<h5>{position} @ {location}</h5>
			Email: <a href="mailto:{mail}">{mail}</a><br/>
			Website: <a href="{website}">{website}</a>
		</div>
	</div>	
</div>
{bio}
<br/><br/>

""".format(
	name=person[0], 
	surname=person[1], 
	picture=person[2], 
	mail=person[3], 
	website=person[4], 
	position=person[5], 
	location=person[6], 
	bio=person[7]))

def readable(kind):
	r = kind.lower().replace('_', ' ')
	if r == 'book':
		r = 'book chapter'
	elif r == 'other':
		r = 'article'
	return r

with open('../publications.md', 'w') as file:
	file.write("""---
layout: page
title: Publications
---
""")
	curryear = None
	for publication in publications:
		year = publication[1].year
		if curryear is None:
			curryear = year
			file.write('## {year}\n\n'.format(year=curryear))
		elif year != curryear:
			curryear = year
			file.write('## {year}\n\n'.format(year=curryear))

		print("Adding", publication[0], "to the Publications page")
		file.write('{authors}: _"{title}"_, in {venue} [DOI](https://doi.org/{doi})\n\n'.format(
			authors=', '.join(publication[5]), 
			title=publication[0], 
			venue=publication[3], 
			doi=publication[4]))

		newsname = '{year}-{month}-{day}-paper-{hash}'.format(
			year=year, 
			month=publication[1].month, 
			day=publication[1].day, 
			hash=hashlib.md5(publication[0].encode('utf-8')).hexdigest())
		print("Generating news for ", publication[0], "(", newsname, ")")
		with open('../news/_posts/{fname}.md'.format(fname=newsname), 'w') as news:
			news.write("""---
layout: page
title: '{startingkind} published in "{venue}"'
---

The {kind} "{title}", by {authors}, has just been published in "{venue}"! Available [here](https://doi.org/{doi}).
""".format(
		authors=', '.join(publication[5]), 
		title=publication[0], 
		venue=publication[3], 
		doi=publication[4], 
		kind=readable(publication[2]),
		startingkind=readable(publication[2]).capitalize()))