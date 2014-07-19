#White Truffle API Scraper

#Their interface is so lovely, why scrape?
White Truffle has More Info than they show, including employers' self selected pay ranges.

Add the arg `persistent=True` if you want it to silently save to a .file in the current direcory. You can also assign a file path yourself using the `json_file_name` arg.

# Example Use:

	from jobscraper import WTScraper

	wt = WTScraper("brian@whatever.com", "myp4ssword4white_truffle" [, other search_params you might want])
	# wait a second for it to go get companies 

	# The jobs that the companies list has aren't very descriptive.
	# Let's update those from the other API endpoints.
	wt.update_companies_jobs_lists()

	from pprint import pprint

	pprint(wt["Delectable"]['positions']['jobs'])
	[{u'account_location_id': 6,
	  u'citizenships': [],
	  u'date_posted': u'2013-08-26T20:02:16',
	  u'done_processing': False,
	  u'educations': [],
	  u'employer_id': 12921,
	  u'employers': [],
	  u'id': 1492,
	  u'locations': [u'Peninsula', u'San Francisco', u'Oakland', u'North Bay'],
	  u'max_equity': None,
	  u'max_salary': None,
	  u'min_equity': None,
	  u'min_salary': None,
	  u'ptype': 0,
	  u'relocation': False,
	  u'remote': False,
	  u'skill_required': u'iOS',
	  u'skills': [u'iOS', u'Obj-C'],
	  u'skills2': [{u'position_id': 1492,
	                u'skill': u'iOS',
	                u'specialization': u'Mobile'},
	               {u'position_id': 1492,
	                u'skill': u'Obj-C',
	                u'specialization': u'Mobile'}],
	  u'specializations': [u'Mobile'],
	  u'status': u'ACTIVE',
	  u'status_int': 0,
	  u'tags': [u'Mobile', u'San Francisco, CA, US', u'iOS', u'Obj-C'],
	  u'title': u'iOS Engineer'},
	 {u'account_location_id': 6,
	  u'citizenships': [],
	  u'date_posted': u'2014-07-16T22:48:45',
	  u'done_processing': False,
	  u'educations': [],
	  u'employer_id': 12921,
	  u'employers': [],
	  u'id': 2409,
	  u'locations': [u'North Bay', u'Peninsula', u'Oakland', u'San Francisco'],
	  u'max_equity': None,
	  u'max_salary': None,
	  u'min_equity': None,
	  u'min_salary': None,
	  u'ptype': 0,
	  u'relocation': False,
	  u'remote': False,
	  u'skill_required': u'',
	  u'skills': [u'CSS', u'HTML', u'JavaScript', u'Rails', u'Ruby'],
	  u'skills2': [{u'position_id': 2409,
	                u'skill': u'CSS',
	                u'specialization': u'Frontend'},
	               {u'position_id': 2409,
	                u'skill': u'HTML',
	                u'specialization': u'Frontend'},
	               {u'position_id': 2409,
	                u'skill': u'JavaScript',
	                u'specialization': u'Frontend'},
	               {u'position_id': 2409,
	                u'skill': u'Rails',
	                u'specialization': u'Frontend'},
	               {u'position_id': 2409,
	                u'skill': u'Ruby',
	                u'specialization': u'Frontend'}],
	  u'specializations': [u'Frontend'],
	  u'status': u'ACTIVE',
	  u'status_int': 0,
	  u'tags': [u'Frontend',
	            u'San Francisco, CA, US',
	            u'CSS',
	            u'HTML',
	            u'JavaScript',
	            u'Rails',
	            u'Ruby'],
	  u'title': u'Master of Web'},
	 {u'account_location_id': 6,
	  u'citizenships': [],
	  u'date_posted': u'2014-06-11T19:51:44',
	  u'done_processing': False,
	  u'educations': [],
	  u'employer_id': 12921,
	  u'employers': [],
	  u'id': 4489,
	  u'locations': [u'Relocate', u'Remote'],
	  u'max_equity': 1.0,
	  u'max_salary': None,
	  u'min_equity': 0.5,
	  u'min_salary': None,
	  u'ptype': 0,
	  u'relocation': True,
	  u'remote': True,
	  u'skill_required': u'',
	  u'skills': [u'JavaScript', u'REST', u'Ruby', u'Web Development'],
	  u'skills2': [{u'position_id': 4489,
	                u'skill': u'JavaScript',
	                u'specialization': u'Full-Stack'},
	               {u'position_id': 4489,
	                u'skill': u'REST',
	                u'specialization': u'Full-Stack'},
	               {u'position_id': 4489,
	                u'skill': u'Ruby',
	                u'specialization': u'Full-Stack'},
	               {u'position_id': 4489,
	                u'skill': u'Web Development',
	                u'specialization': u'Full-Stack'}],
	  u'specializations': [u'Full-Stack'],
	  u'status': u'ACTIVE',
	  u'status_int': 0,
	  u'tags': [u'Full-Stack',
	            u'San Francisco, CA, US',
	            u'JavaScript',
	            u'REST',
	            u'Ruby',
	            u'Web Development'],
	  u'title': u'Full Stack Lead Web Developer'},
	 {u'account_location_id': 6,
	  u'citizenships': [],
	  u'date_posted': u'2014-07-13T19:37:00',
	  u'done_processing': False,
	  u'educations': [],
	  u'employer_id': 12921,
	  u'employers': [u'Google',
	                 u'Square',
	                 u'Dropbox',
	                 u'Box',
	                 u'Apple',
	                 u'Facebook'],
	  u'id': 5214,
	  u'locations': [u'Relocate', u'Remote'],
	  u'max_equity': None,
	  u'max_salary': None,
	  u'min_equity': None,
	  u'min_salary': None,
	  u'ptype': 0,
	  u'relocation': True,
	  u'remote': True,
	  u'skill_required': u'',
	  u'skills': [u'JavaScript', u'Rails', u'Ruby'],
	  u'skills2': [{u'position_id': 5214,
	                u'skill': u'JavaScript',
	                u'specialization': u'Full-Stack'},
	               {u'position_id': 5214,
	                u'skill': u'Rails',
	                u'specialization': u'Full-Stack'},
	               {u'position_id': 5214,
	                u'skill': u'Ruby',
	                u'specialization': u'Full-Stack'}],
	  u'specializations': [u'Full-Stack'],
	  u'status': u'ACTIVE',
	  u'status_int': 0,
	  u'tags': [u'Full-Stack',
	            u'San Francisco, CA, US',
	            u'JavaScript',
	            u'Rails',
	            u'Ruby'],
	  u'title': u'Expert in Web Technologies'}]