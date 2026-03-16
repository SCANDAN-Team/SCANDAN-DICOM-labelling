# SCANDAN-DICOM-labelling

Regular expression used during the SCANDAN project to label MRI scans based on DICOM tag. 
DOI: https://doi.org/10.1101/2025.10.21.25338469  

If you use these for your research, please cite:  
Camilleri, Michael PJ, et al. "A large dataset of brain imaging linked to health systems data: the curation and access to a whole system national cohort from NHS Scotland." medRxiv (2025): 2025-10.


## Specifics
- DICOM tags were stripped of their tag "(XXXX,XXXX)" after extraction for easier reading and reference within the code. 
- We used multiple tags for some information (like body parts) as there was empty columns, and some information was not reliable. A consensus approach was adopted to merge the different results when they disagreed, although the exact threshold is specific to the data you have.
- Rules were improved with later project. Please look below for the version explanation.
- CT Kernel rules were not provided for SCANDAN as they were not tested, due to render errors within the DICOM viewer used. 

## Version
- This version is the one used for the results of the SCANDAN paper and the one used to generate the labelling currently available on the Brain Health Data. 
- The latest version can be found in branch `latest` and has been improved on in-house research dataset. Improvement include better differentiation of DWI/SWI, and fixes for regex catching too wide.





