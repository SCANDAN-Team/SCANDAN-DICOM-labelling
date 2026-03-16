# CAROTIDS head no brain
# add foot/feet, hand, others


BODY_DICT = {
    'HEAD':  [r'(?i)head', r'(?i)brain', r'(?i)cerebr', r'(?i)skull',
              r'(?i)cran(i|e)'],
    'NECK': [r'(?i)neck'],
    # 'SINUSES': [r'(?i)sinus'],
    'CHEST': [r'(?i)chest', r'(?i)thorax'],
    'ABDOMEN': [r'(?i)abdo'],
    'NOSE': [r'(?i)nose'],
    'SPINE': [r'(?i)spine'],
    'IAM': [r'(?i)iam', r'(?i)iac'],
    'PELVIS': [r'(?i)pelv'],
    'CAROTID': [r'(?i)carotid'],
    'HEART': [r'(?i)heart'],
    'OTHER_HEAD': [r'(?i)mandible', r'(?i)orbit', r'(?i)tongue', r'(?i)mouth',
                   r'(?i)sinus'],
}

MATCH_TABLE = {
    'HEAD': {'one': ['HEAD'], 'zero': ['*']},
    'NECK': {'one': ['NECK']},
    'SPINE': {'one': ['SPINE']},
    'ABDOMEN': {'one': ['ABDOMEN']},
    'CHEST': {'one': ['CHEST']},
    # 'SINUSES': {'one': ['SINUSES']},
    'OTHER_HEAD': {'one': ['OTHER_HEAD']},
    'HEAD&NECK': {'cond': 'and', 'one': ['HEAD', 'NECK']},
    'HEAD&?': {'one': ['HEAD'], 'two': ['*'], 'zero': ['Neck']},
}

body_kwargs = {
    'seq_dict': BODY_DICT,
    'match_table': MATCH_TABLE,
    'out': 'Body'
}
