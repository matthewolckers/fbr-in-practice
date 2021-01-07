# Friend-Based Ranking in Practice

Code and data for [Friend-Based Ranking in Practice](https://www.aeaweb.org/conference/2021/preliminary/2338), a presentation by [Francis Bloch](https://www.sites.google.com/site/francisbloch1/) and [Matthew Olckers](https://www.matthewolckers.com/) at [American Economic Association's Annual Meeting](https://www.aeaweb.org/conference/about) on January 4, 2021.

Code is written in Python makes use of Jupyter Notebooks. Rather than saving the original notebook in this folder, we use [JupyText](https://github.com/mwouts/jupytext) to save either a markdown file or Python script. We also save the output of the notebooks in the subfolder `notebooks/output` as pdf print-outs.

Figures are produced in R using ggplot2.

The analysis is completed in the following steps.


## Step 1: Download the data

The data is sourced from Alatas et al (2012) and Alatas et al (2016). Before running any of the code, this data must be downloaded and saved in specific folders. The data is downloaded as `.zip` files and then must be extracted to the `\data` folder.

### Alatas et al (2012)

Download from [DOI:10.3886/E112522V1](http://doi.org/10.3886/E112522V1) and save in the folder `data\112522-V1`.

Data citation:

Alatas, Vivi, Banerjee, Abhijit, Hanna, Rema, Olken, Benjamin A., and Tobias, Julia. Replication data for: Targeting the Poor: Evidence from a Field Experiment in Indonesia. Nashville, TN: American Economic Association [publisher], 2012. Ann Arbor, MI: Inter-university Consortium for Political and Social Research [distributor], 2019-10-11. [https://doi.org/10.3886/E112522V1](https://doi.org/10.3886/E112522V1)

Article citation:

Alatas, Vivi, Abhijit Banerjee, Rema Hanna, Benjamin A Olken, and Julia Tobias. “Targeting the Poor: Evidence from a Field Experiment in Indonesia.” American Economic Review 102, no. 4 (June 2012): 1206–40. [https://doi.org/10.1257/aer.102.4.1206](https://doi.org/10.1257/aer.102.4.1206)


### Alatas et al (2016)


Download from [DOI:10.3886/E119802V1](https://doi.org/10.3886/E119802V1) the source and save in the folder `data\119802-V1`. This zip file contains a second compressed folder `Network Data.zip`, which you will also need to extract.

Data citation:

Alatas, Vivi, Banerjee, Abhijit, Chandrasekhar, Arun, Hanna, Rema, and Olken, Benjamin. Data and Code for: Network Structure and the Aggregation of Information: Theory and Evidence from Indonesia. Nashville, TN: American Economic Association [publisher], 2020. Ann Arbor, MI: Inter-university Consortium for Political and Social Research [distributor], 2020-06-08. https://doi.org/10.3886/E119802V1

Article citation:

Alatas, Vivi, Abhijit Banerjee, Arun G. Chandrasekhar, Rema Hanna, and Benjamin A. Olken. “Network Structure and the Aggregation of Information: Theory and Evidence from Indonesia.” American Economic Review 106, no. 7 (July 1, 2016): 1663–1704. https://doi.org/10.1257/aer.20140705.


## Step 2: Run the programs

`ExtractNetworks.md` + `ExtractData.md`

Extract the network, household and hamlet data collected by [Alatas et al (2020)](http://doi.org/10.3886/E119802V1) during a field experiment in Indonesia.


`Analysis.md`

Run the analysis to compare friend-based ranking with community-based targeting. HodgeRank codes are imported from `Hodge.py`.

`Figures.R`

Use data exported from the analysis to produce figures for the publication.

`HodgeRank.md`

Test HodgeRank on simple examples.

---

## Bonus

You can play with the data online using Binder.


[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/matthewolckers/fbr-in-practice/HEAD)
