# Work Log

Howdy!
This file documents my work on the eFCR analyzer.
I will include timestamps, a brief summary of tasks completed, and some reasoning at each stage.
I hope to provide transparency into how I approached the project, including any challenges or ideas I had along the way.

---

## April 8 @ 4:45 PM

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

**Thoughts**

- Want to balance simplicity with comprehensiveness--need to avoid my tendency to overengineer features that aren't relevant
- Probably will go with a Flask app to build quick and clean (not quick and dirty!)
- eFCR looks like a bit of a mess

** TODO **

- Probe data for features, trends, etc.
- Should be simple enough to find word counts per agency, will tackle that challenge first
- Leaving for training @ 5:55PM
