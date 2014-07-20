import requests
import json
import re

"""
Example Use:

from jobscraper import LeakyTruffle

wt = LeakyTruffle("brian@whatever.com", "myp4ssword4white_truffle" [, other search_params you might want])
# wait a second for it to go get companies 

# The jobs that the companies list has aren't very descriptive.
# Let's update those from the other API endpoints.
wt.update_companies_jobs_lists()

"""

# Should be in str_utils file.
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class LeakyTruffle(object):

	def __init__(self, email, password, skills=[], locations=[], specializations=[], remote=False, persistent=False, json_file_name=None, keyword=""):
		self.email = email
		self.password = password
		self.session = self.get_authenticated_session(self.email, self.password)
		self.companies = {}
		self.skills = skills
		# Locations are lat/long pairs, see the default.
		self.locations = locations
		self.specializations = specializations
		self.remote = remote

		self.keyword = keyword

		# For serialization and persisting data.
		# Can't be non-persistent if you give a file name.
		self._persistent = persistent if not json_file_name else True
		self.json_file_name = json_file_name


		if not self._persistent and not self.json_file_name:
			self.companies = self.get_list_of_companies()
			self.companies_by_names = {c["name"]: c for k, c in self.companies.items()}

		if self._persistent:
			self.json_file_name = json_file_name or ".preserved_companies.json"
			try:
				self._load()
			except :
				self.companies = self.get_list_of_companies()
				self.companies_by_names = {c["name"]: c for k, c in self.companies.items()}
				self._save()


	def _save(self):
		if self._persistent:
			json_file = file(self.json_file_name, "w")
			json_file.write(json.dumps(self.companies))
			json_file.close()

	def _load(self):
		if self._persistent:
			json_file = open(self.json_file_name)
			self.companies = json.loads(json_file.read())
			self.companies_by_names = {c["name"]: c for k, c in self.companies.items()}
			self.set_jobs_pay_skills()

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
			"keyword": self.keyword,
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

	def update_companies_jobs_lists(self, only_new=False):
		to_update = self.recently_added if only_new else self.companies
		for cid, company in to_update.items():
			joblist = {}
			try:
				joblist = self.get_joblist_for_company(cid)
			except:
				pass
			self.companies[cid]["positions"] = joblist
			self.companies_by_names[company["name"]]["positions"] = joblist

		self.set_jobs_pay_skills()
		self._save()


	def get_list_of_companies(self):
		"""
		Default NYC because Brian is writing this.
		"""
		search_params = {"keyword":"","skills":[],"locations":[{"latitude":40.67,"longitude":-73.94}],"specializations":[],"remote":int(self.remote)}
		search_params.update(self.search_params)

		headers = {'Accept-Encoding': ' gzip,deflate,sdch',
		'Accept-Language': ' en-US,en;q=0.8',
		'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
		'Content-Type': ' application/json;charset=UTF-8',
		'Accept': ' application/json, text/plain, */*',
		'Referer': ' https://www.whitetruffle.com/c/explore',}

		employer_list = self.session.post("https://www.whitetruffle.com/c/search_explore", data=json.dumps(search_params), headers=headers).json()
		return employer_list


	def add_companies_from_new_search(self):
		"""
		To not get same results change some of the params between __init__ and using this..
		"""
		new_companies = {k:v for k,v in self.get_list_of_companies().items() if k not in self.companies}
		self.companies.update(new_companies)
		self.recently_added = {k: self.companies[k] for k in new_companies}
		self.companies_by_names.update({c["name"]: c for k, c in self.recently_added.items()})
		self.update_companies_jobs_lists(only_new=True)


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


	def set_jobs_pay_skills(self):
		res = {}
		for cid, company in self.companies.items():
			res[company["name"]] = [
				{p["title"]: {
						"pay_range": (p["min_salary"], p["max_salary"]),
						"equity_range": (p["min_equity"], p["max_equity"]),
						"skills": p["skills"],
					}
				} for p in company["positions"]["jobs"] ]

		self.jobs_pay_skills = res

	def load_company_objects():
		for c in self.companies.values():
			Company(c)


class Company(object):

	all_companies = []

	@classmethod
	def search_by(cls, *args, **tests):
		def run_tests(pos, tests=tests):
			value = getattr(pos, attr)
			return all([passing(value) if callable(passing) else value == passing for attr, passing in tests.items()])

		return [pos for pos in cls.all_positions if run_tests(pos)]

	def __init__(self, raw):
		Company.all_companies.append(self)
		self.name = raw.get("name", name)
		self.location = raw.get("location", location)
		self.positions = [Position(pos, raw) for pos in raw["positions"]["job"]]
		for pos in self.positions:
			setattr(convert(pos.title), pos)

class Position(object):

	all_positions = []

	@classmethod
	def search_by(cls, *args, **tests):
		def run_tests(pos, tests=tests):
			value = getattr(pos, attr)
			return all([passing(value) if callable(passing) else value == passing for attr, passing in tests.items()])

		return [pos for pos in cls.all_positions if run_tests(pos)]


	def __init__(self, company, job_raw={}, raw={}):
		Position.all_positions.append(self)
		self.company = company
		self.title = job_raw.get("title", "")

		# Compensation
		self.min_salary = job_raw.get("min_salary", None)
		self.max_salary = job_raw.get("max_salary", None)
		self.min_equity = job_raw.get("min_equity", None)
		self.max_equity = job_raw.get("max_equity", None)

		# Other

		# Set-like stuff
		self.skills = set(job_raw.get("skills", []))
		self.specializations = set(job_raw.get("specializations", []))
		self.tags = set(job_raw.get("tags", []))
		
		# Update company stuff, dunno why they store this in the positions info and not company or job.
		self.company.about = self.company.about or raw.get("about", "")
		self.company.hours = self.company.hours or raw.get("hours", "")
		self.company.mission_statement = self.company.mission_statement or raw.get("mission_statement", "")
		self.company.workflow = self.company.workflow or raw.get("workflow", "")
		self.company.website_url = self.company.website_url or raw.get("website_url", "")
		self.company.employees_enum = self.company.employees_enum or raw.get("employees_enum", "")
		
		# Set-like stuff with selected or not.
		self.company.perks = self.company.perks or set([p['public_name'] for p in raw.get("perks", "") if p["selected"]])
		self.company.benefits = self.company.benefits or set([p['public_name'] for p in raw.get("benefits", "") if p["selected"]])
		














