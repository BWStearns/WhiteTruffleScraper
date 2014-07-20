#Leaky Truffle
##A White Truffle API Scraper

#Their interface is so lovely, why scrape?
While looking for a new job today (anyone in NYC hiring?) I found that White Truffle sends the browser more info than they show, including employers' self selected pay ranges. Clearly this might be nice to have to limit the information asymmetry of negotiations.

Add the arg `persistent=True` if you want it to silently save to a .file in the current direcory. You can also assign a file path yourself using the `json_file_name` arg.

## Todo
+ Make company/jobs objects so you're not in __getitem__/brackets hell.
+ Some kind of search capability.
+ Ideas?

## Example Use:

	from jobscraper import LeakyTruffle

	wt = LeakyTruffle("brian@whatever.com", "myp4ssword4white_truffle" [, other search_params you might want])
	# wait a second for it to go get companies 

	# The jobs that the companies list has aren't very descriptive.
	# Let's update those from the other API endpoints.
	wt.update_companies_jobs_lists()

	wt.jobs_pay_skills["Yo"]
	[
		{u'Android Developer': 
			{
				'equity_range': (110000.0, 140000.0),
			   	'pay_range': (110000.0, 140000.0),
			   	'skills': [u'Android'],
			}
		}
	]