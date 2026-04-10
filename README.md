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


## Logic
There are multiple components. 
- The rule dictionary (`_seq`):
    - Key: temporary labels (e.g. "HEAD", "PELVIS", "T1", ...)
	- Value: the list of regular expressions which are associated with the key. For example, /(?i)head/ and /(?i)skull/ are two regular expression associated with the key "HEAD". 
    - Each temporary labels should be an independant element uniquely identifiable. For exmaple, "FINGER" and "HAND" should be two different keys.
	- The rule dictionaries are stored in `./text_matching/[name]_text_matching.py`
- The match table (dictionary) (`_match_table`):
	- Key: final labels (e.g. "HEAD&NECK", "HEAD", "LOCALISER", ...)
	- Value: the combination dictionary which contains 4 keys: "one", "two", "zero" and "cond". 
		- "one" (mandatory): indicate the temporary labels which needs to be present to assign the Key as a final label
		- "zero" (optional): indicate the temporary labels which needs to be absent to assign the Key as a final label
		- "two" (optional): indicate which temporary labels will be ignored when evaluating a sample for this final label.
		- "cond" (optional, default "or"): "and" or "or" to be used between the label "one". "and" means every temporary labels in "one" need to be present, "or" means only one
		- "\*" means every other temporary labels not present in "one", "two" and "zero". By default it is assigned within "zero" 
	- The match table are stored in `./text_matching/[name]_text_matching.py`
- The DICOM tag which are parsed. One DICOM tag can be used to extract different information (for example the "Study Description" can contains body part or contrast information) (`_col`). 
- The key columns used to identify samples. This is provided so the output can be traced back to the input (`_key`). 

Let's use the following 3 temporary labels: "HEAD", "NECK" and "SPINE". They would be associated to regular expressions which identify their presence within the text parsed (e.g. /(?i)head/ or /(?i)spine/)
- If we want to find a sample which contains "HEAD" only without "NECK" or "SPINE", we want to create a key: value in the match table as follow:
    - `"head": {"one": ["HEAD"], zero: ["NECK", "SPINE"]}` (note: by default, every label not in "one" or "two" goes to "zero", so we could simply write `"head": {"one": ["HEAD"]}`. 
	- This can be translated to Head:1, Neck:0, Spine:0. And we can then understand 1 and 0 as boolean. "head" is "HEAD" and not "NECK" and not "SPINE".
- If we want to find sample which contains "HEAD" and "NECK" together without anything else, this would be:
    - `"head&neck": {"one": ["HEAD", "NECK"], cond: "and"}`
	- This can be read as "HEAD" and "NECK" and not "*". So not "SPINE".
- If we want to find anything that is not a head:
    - `"no_head": {"one": ["NECK", "SPINE"]}`
	- This can be read as ("NECK" or "SPINE") and not "*". So not "HEAD".
	- The default condition, "or" is applied between the temporary labels in "one". 
- If we want to find any sample containing a head, whether they have other parts or not:
	- `"head&?" : {"one": ["HEAD"], "two": ["NECK", "SPINE"]}`
	- "two" will simply ignore the presence or absence of "NECK" and "SPINE", meaning the rule is now simply "HEAD".

Visualised different:
- The regex are matched against the text. Any positive match yield `TRUE` for the temporary label (1). If no regex are matched, then the temporary labels is `False` (0). 
	- "mri head" yield `TRUE` for /(?i)head/ but `FALSE` for /(?i)neck/ and /(?i)spine/
	- "ct neck" yield `FALSE` for /(?i)head/ and /(?i)spine/, but `TRUE` for /(?i)neck/
- For each line in the match table, the temporary labels in "one" and "zero" are the only one used. 
  - {"one": ["HEAD"], "two": ["SPINE"], "zero": ["NECK"]} means only "NECK" and "HEAD" are used
	  - the rule can be read as 10 ("HEAD": 1, "NECK":0)
	  - "mri_head" is "HEAD":TRUE, "NECK":FALSE, so 10, so it matches the rule
	  - "ct neck" is "HEAD":FALSE, "NECK": TRUE, so 01, so it doesn't match the rule
	  
	  
