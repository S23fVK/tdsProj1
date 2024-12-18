# tdsProj1
- Github API was used to gather data data and analyze popular github users in Seattle and their respective repositories.
## Findings:
### 1. Top 5 Languages:
  - JavaScript (7723 users)
  - Python (5475 users)
  - Ruby (2397 users)
  - HTML (2109 users)
  - TypeScript (1924 users)
### 2. Account creation dates:
  - The majority of users created their accounts in 2012, followed by 2011, 2010, 2013, and 2014.
### 3. Projects and Wiki relation
  - Majority of users (42598 users) have both projects and wiki in their github page.
  - Correlation between projects and wikis: 0.3109
  - The positive value of correlation is because when a repository has projects enabled, it was more likely to have a wiki enabled as well. Conversely, repositories without projects enabled were less likely to have a wiki. But a correlation of 0.311 is relatively low, i.e. the relationship between enabling projects and wikis is weak. There is a slight trend that repos with projects also have wikis, but this is not a strong or consistent association.

# Seattle GitHub User and Repository Analysis
This program retrieves data about Seattle Github users (with more than 200 followers) using Github API and makes csv files of their repo details, making it easier to analyse trends in the data.

# Recommendations:
- Learning JavaScript or Python is recommended as that is the most commonly used programming language in Seattle.
- Having a Readme file which explains the contents of the repo will be very beneficial to viewers.
 
# Note: 
Github API token has been replaced with \<inserted github token here> due to security concerns.
