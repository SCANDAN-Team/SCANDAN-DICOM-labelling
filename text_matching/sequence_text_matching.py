# start word
STW = r'(\s|^|\_|\-|\(|\))'
# end word
ENW = r'(\s|$|\_|\-|\(|\))'


# get word as regex
def gw(s):
    return fr'{STW}{s}{ENW}'


SEQ_DICT = {
    'T1': [r'(?i)t1', r'SmartBrain', r'(?i)spgr',
           r'3DIR PREP', r'(?i)mprage'],
    'T1?': [r'(?i)SmartBrain'],
    'T2': [r'(?i)(?<!pa)t2', r'\*se2d1'],
    'T2*': [r'(?i)T2\*'],
    'T2*T1': [r'3-pl T2\* FGRE'],
    'T2ci3d': [r'(?i)ci3d', r'(?i)iac'],
    'SWI': [r'SWI', r'SWAN'],
    'SWI?': [r'(?i)swi', r'(?i)swan'],
    'SWI_mIP': [r'mIP', r'MINIP'],
    'SWI_mIP?': [r'(?i)mIP', r'(?i)MINIP'],
    'DWI_ADC': [fr'(?i){gw("ADC")}', r'ADC', r'(?i)dadc', r'(?i)Average_DC'],
    'DWI_ADC?': [r'(?i)ADC'],
    'DWI_FA': [fr'(?i){gw("FA")}'],
    'DWI_DTI?': [fr'(?i){gw("DTI")}', r'DTI', r'EPI'],
    'DWI_DTI??': [r'(?i)dti'],
    'DWI': [r'TRACEW', r'(?i)dwi', r'DW', r'(?i)diff'],
    'SWI_Mag': [r'Mag'],
    'SWI_Mag?': [r'(?i)mag'],
    'SWI_Pha': [r'Pha'],
    'SWI_Pha?': [r'(?i)pha'],
    'GRE': [r'(?i)gre', r'(?i)hemo', r'(?i)blood', r'(?i)haem',
            r'gradient echo'],
    # 'GRE?'r: ['(?i)GRE', '(?i)hemo'],
    'FLAIR': [r'(?i)flair', r'(?i)da(rk|)(-|_)fl'],
    # 'FLAIR?': [r'(?i)fl'],
    'PD': [r'PD', r'IR-SPGR_IROff_2_v4'],
    'PD?': [r'(?i)pd'],
    'LOC': [fr'(?i){gw("LOC")}', fr'{gw("SUR")}', r'(?i)survey',
            r'(?i)localizer', r'(?i)localiser', r'(?i)scout',
            r'(?i)patient protocol', r'(?i)topogram'],
    # 'LOC?': [r'(?i)loc'],
    'MRA': [r'TOF', r'MRA'],
    'PWI': [r'DSC-EPI', r'Negative Enhancement Integra(l|\?)'],
    # 'PAT2': ['(?i)pat2'],
    'DSE': [r'(?i)dse'],
    'FAT SAT': [r'FS(\s|$)', r'(?i)fat sat'],
    'STIR': [r'(?i)stir']
}


MATCH_TABLE = {
    'T1': {'one': ['T1'],
           'two': ['T1?', 'GRE', 'FAT SAT', 'FLAIR_UKN', 'FLAIR'],
           'zero': ['DSE']},
    'T2': {'one': ['T2'], 'two': [], 'zero': ['FLAIR', 'GRE', 'T2*', 'T2ci3d',
                                              'T2*T1']},
    'T2iac': {'one': ['T2ci3d'], 'two': ['T2']},
    'T2*_': {'cond': 'or', 'one': ['T2*'], 'two': ['T2', 'GRE'],
             'zero': ['T2*T1']},
    'T2*': {'cond': 'and', 'one': ['T2', 'GRE'], 'zero': ['T2*T1']},
    'T2*T1': {'one': ['T2*T1'], 'two': ['T2', 'T2*', 'GRE']},
    'FLAIR': {'one': ['FLAIR'], 'two': ['T2', 'FLAIR?'], 'zero': []},
    'T1w_UKN': {'one': ['T1?'], 'two': [], 'zero': ['DSE', 'T1']},
    'FLAIR_UKN': {'one': ['FLAIR?'], 'two': ['T2'], 'zero': ['FLAIR']},
    'LOCALISER': {'one': ['LOC'], 'two': ['*'], 'zero': []},
    'DWI': {'one': ['DWI', 'DWI_ADC', 'DWI_FA', 'DWI_DTI?'],
            'two': ['DWI_ADC?', 'DWI_DTI??']},
    'SWI': {'one': ['SWI', 'SWI_mIP', 'SWI_Mag', 'SWI_Pha'],
            'two': ['SWI?', 'SWI_mIP?', 'SWI_Mag?', 'SWI_Pha?']},
    'MRA': {'one': ['MRA']},
    'PD': {'one': ['PD'], 'two': ['PD?']}
    # 'LOCALISER_UKN': {'one': ['LOC?'], 'two': ['*'], 'zero': ['LOC']}
    # 'UKN': {'one': [], 'zero': [], 'two': [i for i in SEQ_DICT.keys()
    #                           if '?' in i or i not in ['T1?', 'FLAIR?']]}
}

sequence_kwargs = {
    'seq_dict': SEQ_DICT,
    'match_table': MATCH_TABLE,
    'out': 'Sequence'
}
