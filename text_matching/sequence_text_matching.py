# start word
STW = r'(\s|\+|^|\_|\-|\(|\)|\:)'
# end word
ENW = r'(\s|\+|$|\_|\-|\(|\)|\:)'


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
    'SWI': [fr'(?i){gw("swi")}', fr'(?i){gw("swan")}', 'SWI', 'SWAN',
            '(?i)Susceptibility'],
    'SWI?': [r'(?i)swi', r'(?i)swan'],
    'SWI_mIP': [r'mIP', r'MINIP', r'^MIP$'],
    'SWI_mIP?': [r'(?i)mIP', r'(?i)MINIP'],
    'DWI_ADC': [fr'(?i){gw(fr"d?a{ENW}?dc")}', fr'(?i)d?average{ENW}?dc',
                r'ADC'],
    'DWI_FA': [fr'(?i)FA{ENW}', r'(?i)fractional ansio'],
    'DWI_DTI?': [fr'(?i){gw("DTI")}', r'DTI', r'EPI'],
    'DWI_DTI??': [r'(?i)dti'],
    'DWI': [r'TRACEW', r'(?i)dwi', r'DW', r'(?i)diff', r'(?i)b(\s)?1000',
            r'(?i)b0'],
    'SWI_Mag': [r'Mag'],
    'SWI_Mag?': [fr'(?i){gw("mag")}'],
    'SWI_Pha': [fr'{gw("Pha")}', r'(?i)FILT_PHA'],
    'SWI_Pha?': [r'(?i)pha'],
    'GRE': [r'(?i)gre', r'(?i)hemo', r'(?i)blood', r'(?i)haem',
            r'gradient echo'],
    # 'GRE?'r: ['(?i)GRE', '(?i)hemo'],
    'FLAIR': [r'(?i)flair', fr'(?i)da(rk)?{ENW}?fl'],
    # 'FLAIR?': [r'(?i)fl'],
    'PD': [r'PD', r'IR-SPGR_IROff_2_v4', fr'(?i){gw("pd")}'],
    'LOC': [fr'(?i){gw("LOC")}', fr'{gw("SUR")}', r'(?i)survey',
            r'(?i)locali(z|s)er', r'(?i)scout',
            r'(?i)patient protocol', r'(?i)topogram', r'(?i)calib',
            fr'(?i){gw("cal")}'],
    # 'LOC?': [r'(?i)loc'],
    'MRA': [fr'(?i){gw("TOF")}', r'MRA'],
    'PWI': [r'DSC-EPI', r'Negative Enhancement Integra(l|\?)'],
    # 'PAT2': ['(?i)pat2'],
    'DSE': [r'(?i)dse'],
    'FAT SAT': [r'FS(\s|$)', r'(?i)fat sat'],
    'STIR': [r'(?i)stir'],
    'MeanDiff': [r'(e|d|iso)MEAN']
}


MATCH_TABLE = {
    'T1W': {'one': ['T1'],
            'two': ['T1?', 'GRE', 'FAT SAT', 'FLAIR_UKN', 'FLAIR'],
            'zero': ['MRA']},
    'T2W': {'one': ['T2'], 'two': []},
    'PDT2': {'cond': 'and', 'one': ['PD', 'T2'], 'two': ['PD?']},
    'T2starW_': {'cond': 'or', 'one': ['T2*'], 'two': ['T2', 'GRE'],
                 'zero': ['T2*T1']},
    'T2starW': {'cond': 'and', 'one': ['T2', 'GRE'], 'zero': ['T2*T1']},
    'T2starT1': {'one': ['T2*T1'], 'two': ['T2', 'T2*', 'GRE']},
    'FLAIR': {'one': ['FLAIR'], 'two': ['T2', 'FLAIR?', 'FAT SAT'],
              'zero': []},
    'T1WUKN': {'one': ['T1?'], 'two': [], 'zero': ['DSE', 'T1']},
    'LOCALISER': {'one': ['LOC'], 'two': ['*'], 'zero': []},
    'DWI': {'one': ['DWI'],
            'two': ['T2']},
    'DWI_DTI': {'one': ['DWI_DTI?',],
                'two': ['DWI_DTI??', 'DWI', 'T2']},
    'DWI_ADC': {'one': ['DWI_ADC', ],
                'two': ['DWI_ADC?', 'DWI', 'T2', 'DWI_DTI?', 'DWI_DTI??']},
    'DWI_FA': {'one': ['DWI_FA'],
               'two': ['DWI', 'T2', 'DWI_DTI?', 'DWI_DTI??']},
    'SWI': {'one': ['SWI'],
            'two': ['SWI?', 'T2']},
    'SWI_mIP': {'one': ['SWI_mIP'],
                'two': ['SWI?', 'SWI', 'SWI_mIP?', 'T2']},
    'SWI_mIP_': {'cond': 'and', 'one': ['SWI_mIP?', 'SWI'],
                 'two': ['SWI?', 'SWI', 'SWI_mIP?', 'T2']},
    'SWI_Mag': {'one': ['SWI_Mag'],
                'two': ['SWI?', 'SWI', 'SWI_Mag?', 'T2']},
    'SWI_Pha': {'one': ['SWI_Pha'],
                'two': ['SWI?', 'SWI', 'SWI_Pha?', 'T2']},
    'MRA': {'one': ['MRA'], 'two': ['T1']},
    'PDW': {'one': ['PD'], 'two': ['PD?', 'T1']}
}


sequence_kwargs = {
    'seq_dict': SEQ_DICT,
    'match_table': MATCH_TABLE,
    'out': 'Sequence'
}
