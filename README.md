#White Truffle API Scraper

#Their interface is so lovely, why scrape?
White Truffle has More Info than they show, including employers' self selected pay ranges ;p

# Example Use:

	from jobscraper import WTScraper

	wt = WTScraper("brian@whatever.com", "myp4ssword4white_truffle" [, other search_params you might want])
	# wait a second for it to go get companies 

	# The jobs that the companies list has aren't very descriptive.
	# Let's update those from the other API endpoints.
	wt.update_companies_jobs_lists()