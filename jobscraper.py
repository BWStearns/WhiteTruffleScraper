import requests
import json

"""
Example Use:



"""

class WTScraper(object):

	def __init__(self, email, password, skills=[], locations=[], specializations=[], remote=False):
		self.email = email
		self.password = password
		self.session = self.get_authenticated_session(self.email, self.password)
		self.companies = {}
		self.skills = skills
		# Locations are lat/long pairs, see the default.
		self.locations = locations
		self.specializations = specializations
		self.remote = remote
		self.companies = self.get_list_of_companies()
		self.companies_by_names = {c["name"]: c for k, c in self.companies.items()}

	def __getitem__(self, item):
		try:
			return self.companies[item]
		except KeyError:
			return self.companies_by_names[item]


	def __setitem__(self, item, value):
		try:
			self.companies[item] = value
		except KeyError:
			self.companies_by_names[item] = value

	@property
	def search_params(self):
		search_params = {
			"skills": self.skills, 
			"locations": self.locations, 
			"specializations": self.specializations,
			"remote": self.remote,
		}
		return {k:v for k,v in search_params.items() if v}

	@property
	def company_names(self):
	    return [c.get('name', None) for k, c in self.companies.items() if 'name' in c]


	def get_authenticated_session(self, email=None, password=None):
		login = "https://www.whitetruffle.com/login"
		s = requests.Session()
		payload = {"email":email,"password":password}
		li = s.post(login, data=payload)
		if li.ok:
			return s
		else:
			print "Login Failed. Type Better, Fail Harder"

	def update_companies_jobs_lists(self):
		for cid, company in self.companies.items():
			joblist = {}
			try:
				joblist = self.get_joblist_for_company(cid)
			except:
				pass
			self.companies[cid]["positions"] = joblist
			self.companies_by_names[company["name"]]["positions"] = joblist


	def get_list_of_companies(self):
		"""
		Default NYC because Brian is writing this.
		"""
		search_params = {"keyword":"","skills":[],"locations":[{"latitude":40.67,"longitude":-73.94}],"specializations":[],"remote":int(self.remote)}.update(self.search_params)

		headers = {'Accept-Encoding': ' gzip,deflate,sdch',
		'Accept-Language': ' en-US,en;q=0.8',
		'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
		'Content-Type': ' application/json;charset=UTF-8',
		'Accept': ' application/json, text/plain, */*',
		'Referer': ' https://www.whitetruffle.com/c/explore',}

		employer_list = self.session.post("https://www.whitetruffle.com/c/search_explore", data=json.dumps(search_params), headers=headers).json()
		return employer_list


	def get_joblist_for_company(self, company):
		joblist = self.session.get("https://www.whitetruffle.com/api/employer/me/{0}".format(company)).json()
		return joblist


	def get_jobslist_for_many_companies(self, companies):
		job_list = {k:{companies[k['name']]} for k in companies if isinstance(companies, dict) and isinstance(k, dict) and 'name' in k}
		for company in job_list:
			jobs = {}
			try:
				jobs = get_joblist_for_company(company)
			except:
				pass
			company["jobs"] = jobs
		return job_list


