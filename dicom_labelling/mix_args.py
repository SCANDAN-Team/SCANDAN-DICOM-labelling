def mix_args(dict_key, dict_txt):
    res = dict_key | dict_txt
    res['out'] += '_' + dict_key['out']
    return res

