## Introduction

- This script helps you perform a quick keyword gap analysis
- It's been designed to work with the keyword export from [SEMRush's domain organic research report](https://www.semrush.com/analytics/organic/positions/?sortField=&sortDirection=desc&db=uk&q=ebay.com&searchType=domain)
- This script essentially performs 2 actions: a) it merges multiple keyword export Excel files together, and b) it filters the merged files down to ensure only the 'useful' rows are kept
- It gets rid of all keywords where less than 3 competitors have visibility, maximising the chance that the resulting keyword list is relevant (if only 1-2 competitors rank for a particular keyword, it's often because that keyword is brand specific or exclusive)
- The output is a ready-to-pivot list of relevant keywords with the best opportunity, so you can compare client visibility with competitors and find the gaps (for each keyword it shows which competitors are currently ranking, their rank, their estimated traffic and more)

## Instructions

- Choose at least 3 of your client's top competitors (less than 3 means there's a strong chance of irrelevant and branded keywords)
- Go to [SEMRush's domain organic research report](https://www.semrush.com/analytics/organic/positions/?sortField=&sortDirection=desc&db=uk&q=ebay.com&searchType=domain) and download keyword lists for your client and each of your chosen competitors (they must be the same xlsx format and filename as you downloaded them from SEMRush - if not this will stop the tool from working)
- Upload your exported files to the tool and click the start button
