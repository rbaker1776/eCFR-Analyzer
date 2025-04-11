# Ryan Baker - eCFR Developer Log

This document contains feedback and other requested information about the project. It is also intended to provide insight into my problem solving process and the reason for some decisions I made.

## Feedback on the Project

This project pushed me out of my comfort zone in a good way.
While I’m comfortable with data wrangling and visualization, I hadn’t previously needed to design a database specifically for caching API results.
In hindsight, the basic architecture is straightforward-as many things are once they’re built-but it took some thinking to get there.

The project guidelines were open-ended, but I suspect that was intentional.
That flexibility encouraged exploration and problem-solving. Along the way, I hit several "medium-sized" roadblocks that required me to draw on a broad mix of skills (and certainly left me wishing for a broader mix still)-from data structures and algorithms to web architecture to networking fundamentals.

## How I would continue the Project

* **In one day**: Fix my poor sorting implementation, find a better hosting solution, refactor my front end to be less stringy, and implement regular API calls to stay up to date.
* **In one week**: Upgrade my database implementation, especially for amendments. I suspect it is more efficient to maintain a relational database for amendments due to the increased redundancy in the amendment data structure.
* **In one month+**: Implement some fuzzy finding algorithms to search these 100 million words for reduandcy and contradiction. Create a forum for suggesting parts to be repealed if they have outlived thier purpose, and have been forgotten about by all but a niche crowd.

## Development Process in Steps

### Rough Data Analysis

I spent a while analyzing the dataset, particularly focusing on the relationship between agencies and their word counts.
The primary level of granularity for word counting is the section. agencies reference sections or higher-level categories, which may contain multiple sections.
There appears to be a one-to-many relationship between an agency and sections — an agency can own many sections, but it’s unclear if a section can belong to multiple agencies. However, this distinction seems to be of little practical concern.

I encountered several quirks in the dataset:

* Structure: After the Title level, the heirarch is optional
* XML Parsing: The flexible (sometimes non existant) heirarchy complicates XML parsing
* Section titles: The format of section titles changes depending on the hierarchy level

### Data Retrieval and Storage

It quickly became clear that I won't be able to simply pull this data on demand because the API calls are far too latent.
As a result, I decided to store the data for local querying.
This approach is well-suited for the application, as the data is read-heavy rather than write-heavy.
We can then implement daily (or so) updates.
There is also not an exhorbitant amount of data that would make this approach impossible.

Initially, I considered using a relational database to represent the hierarchical structure, where each node could either have a pointer to children or contain text (leaf node).
However, I ultimately chose a simpler, more linear approach: storing each page in a table alongside its associated headers.
This, of course, has the benefit of being simpler, but it is also okay because the underlying structure of this data is unlikely to change soon and there is a small enough amount of data that I can afford the redundancy. Additionally, this approach should result in faster queries.

### Finding Word Counts

Once the database was set up, calculating the word counts for each agency was trival — or at least, it would have been if agencies didn’t have optional sub-agencies.
I made the (hopefully reasonable) decision to include the word count of a sub-agency as part of its parent agency’s total.
For the definition of a "word," I counted the text within each \<P\> tag in the XML, treating the content of each paragraph as a unit.
This method excludes footers, headers, and other supplementary text that doesn’t fall within the body of the regulation.

Because of the nature of the linear database queries, it was simple to test my code for correctness by querying individual pages for their word counts and adding the results of sibling pages for parent pages.

The word counts are stored directly in the database for each heirarchy level.
I also decided to fetch the section count for each agency, because sections seem to roughly correspond to regulations.
Basically it seems like a single section often tells me to do a single thing, hence the rough correspondance.
I also retrieved the number of paragraphs mentioning the word "COVID" in any respect to perhaps see which agencies are most closely tied to the events of the past few years.

### Displaying Word Counts

Keep it simple stupid.
I chose to display agency word counts in a table on the website.
I implemented (albeit poorly) sorting by each column.
Right now, sorting triggers a full page re-route, which makes it slower than necessary.
Improving this with client-side sorting would be a quick and meaningful upgrade.
To sort by a given column, just click on that column’s header.


### Implementing Search Feature

It's not fun to sift through hundreds of rows of a table to find some piece of information.
I implemented an instant search feature that performs much faster than the sort currently does. 

### Sub-agencies

One problem it took me too long to realize I had was that after sorting a column, sub-agencies would be thrown away from their parent and had no reliable way of returning.
Hence I decided to hide sub-agencies, and make them optionally visible in a dropdown.
Sorting is applied to each group of sub-agencies separately.

### Finding Amendments

The problem statement encouraged an analysis of historical changes over time. Initially, I considered implementing a diff-style visualization to show how individual sections evolve. However, the eCFR already provides a timeline feature that handles this well.
Hence I was more interested in seeing the volume of amendments over time, as well as how many of them relate to COVID-19.

Fortunately, the eCFR API makes it straightforward to retrieve a list of amendments. With those, I was able to group them by month and visualize amendment activity over time.
I could then sort these values and create a graph of amendments per month.
Interestingly, there is a very large spike in amendments at the end of 2016.
This could potentially be an artifact of the data-the eCFR only guarantees full coverage from January 2017 onward-but it might also reflect a real uptick in regulatory activity related to the political transition at that time.

### Duration

I estimate that this project took around 10 hours of focused work from start to finish.
That includes time spent analyzing and exploring the data before I initialized the Git repository.
I also expect that similar projects will come together more quickly in the future - this one involved a lot of firsts, and the learning curve was front-loaded.
