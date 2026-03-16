ANGIO_DICT = {
    'ANGIO': [r'(?i)angio'],
}

MATCH_TABLE = {
    'Angio': {'one': ['ANGIO']},
}


angio_kwargs = {
    'seq_dict': ANGIO_DICT,
    'match_table': MATCH_TABLE,
    'out': 'Angio'
}
