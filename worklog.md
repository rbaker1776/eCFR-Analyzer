# Work Log

Howdy!
This file documents my work on the eFCR analyzer.
I will include timestamps, a brief summary of tasks completed, and some reasoning at each stage.
I hope to provide transparency into how I approached the project, including any challenges or ideas I had along the way.

---

## April 9 @ 4:45 PM

**Actions**

- Read project description
    - Need to analyze the Electronic Code of Federal Regulations for various metrics
        - Word count per agency (suggested)
        - Historical changes (suggested)
        - Some tree visualization of the documents may be nice
        - Would like a way to see how certain regulations evolved over time
    - Produce a front end visualization for the content
        - Implement a query system (query for what?)
        - Click around (click on what? perhaps I will have a better idea once I better understand the eFCR)
- Initialized git repo
- Read thru eFCR API documentation to understand services provided
    - https://www.ecfr.gov/developers/documentation/api/v1#/
- Leaving for training @ 5:55PM

**Thoughts**

- Want to balance simplicity with comprehensiveness--need to avoid my tendency to overengineer features that aren't relevant
- Probably will go with a Flask app to build quick and clean (not quick and dirty!)
- eFCR looks like a bit of a mess

** TODO **

- Probe data for features, trends, etc.
- Should be simple enough to find word counts per agency, will tackle that challenge first

## April 9 @ 10:00 PM

- Scanned the eCFR website more completely to get a better understanding of the data
- Leaving @ 10:40 PM to sleep

## April 10 @ 4:30 AM

**Actions**

- Implemented 'Agency' class to encapsulate data related to agencies
    - ecfr/agency.py
    - Not strictly needed at the moment, could just use dict. But seems good for possible extensions
    - I think this should me more a 'struct' than a 'class', so to speak... should basically be plain old data. Functionality will be within the client script
- Implemented some basic API calls to analyze the data in Python
    - ecfr/client.py
    - Counting agencies as well as their children... 
- Seems like I will use the cfr_references field for each agency to find the word count and other interesting features
