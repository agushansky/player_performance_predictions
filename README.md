# AFC Richmond Analytics

This project aims to predict targeted player metrics in soccer,
with consideration to historical player performance, team play style, and league.
To this end, the documents in this folder include Python code to scrape raw player data,
clean data, and machine learning algorithms to model relationships and make predictions.

Python, Jupyter Notebooks, and Tableau are needed to run. Should the user desire to run the code to pull and manipulate data, steps are provided below; however, this is not necessary, as Tabluea Public is sufficient for viewing.

DESCRIPTION OF DOCUMENTS and HOW TO EXECUTE
1. DOC - this folder contains two files: `team078report.pdf` and `team078poster.pdf`. 
	`team078report.pdf` contains a report detailing project processes and findings.
	`team078poster.pdf` shows a 1-page summary of the project.

2. CODE - this folder contains four folders: `data-collection`, `data`, `analysis`, and `tableau`.
	- `data-collection` contains six Jupyter workbooks in Python to scrape and clean raw data. 
        - Usage order: `scrape.ipynb` first to pull data, then the two `Merging_...` files to clean the downloaded data.
	- `data` holds stored data extracts as .csv, sorted into four folders based on the stage of the analysis process. As such, user does not need to run the `data-collection` files to pull data as it is provided here.
	- `analysis` contains four jupyter workbooks for data analysis.
        - Usage order: `k-means.ipynb` >> `data_prep.ipynb` >>
          - `group-lasso-no-league-play-styles.ipynb` for comparison model without team play style and league effects
          - `group-lasso-2.ipynb` for final model
	- `tableau` contains two files to visualize data outputs for value-add interpretation.  To run visualization on local Tableau, download both files in folder and run `combined_dashboard.twbx`

3. File `Tableau_viz.ppt` - this file contains the hyperlink to the Tableau Public website location where the visualization is published
