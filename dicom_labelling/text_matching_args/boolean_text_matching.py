BOOL_DICT = {
    'YES': [r'(?i)y'],
    'NO': [r'(?i)n']
}

MATCH_TABLE = {
    'Yes': {'one': ['YES']},
    'No': {'one': ['NO']}
}


boolean_kwargs = {
    'seq_dict': BOOL_DICT,
    'match_table': MATCH_TABLE,
    'out': 'Bool'
}
