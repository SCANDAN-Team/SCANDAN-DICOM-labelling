# bolus = ys
# perfusion
# cbf = cerbral blood flow
# asl = arterial spin labeling
CON_DICT = {
    'CONTRAST': [r'(?i)contrast', r'(?i)gd', r'(?i)gad'],
}

MATCH_TABLE = {
    'Contrast': {'one': ['CONTRAST']},
}


contrast_kwargs = {
    'seq_dict': CON_DICT,
    'match_table': MATCH_TABLE,
    'out': 'Contrast'
}
