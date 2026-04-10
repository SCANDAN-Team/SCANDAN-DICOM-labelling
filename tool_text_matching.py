import pandas as pd
import numpy as np


class TextMatching():
    def __init__(self, in_path, out_path, key, col, out, match_table, seq_dict,
                 sep=','):
        self._col = col
        self._key = key
        self._sep = sep
        self._out = out
        self._in_path = in_path
        self._out_path = out_path
        self._seq = seq_dict
        self._match_table = match_table

    @classmethod
    def match_pat(cls, desc, pat):
        res = {}
        isna = desc.isna()
        desc = desc.fillna('')
        for i, v in pat.items():
            idx = np.logical_or.reduce(
                [desc.str.contains(j, regex=True) for j in v])
            res[i] = idx
        res['nan'] = isna
        return res

    @classmethod
    def convert_bool_table(cls, pat, one=None, two=None, zero=None, cond='or'):
        one_s = set(one) if one is not None else set()
        zero_s = set(zero) if zero is not None else set()
        nan_s = set(['nan'])
        two_s = set(two) if two is not None else set()
        all_s = set(pat) - (one_s | two_s | nan_s | zero_s)
        tmp = set('*')
        if '*' in one_s:
            one_s |= all_s
        elif '*' in two_s:
            two_s |= all_s
        else:
            zero_s |= all_s
        one_s -= tmp
        zero_s -= tmp
        two_s -= tmp
        return {0: zero_s | nan_s, 1: one_s, 2: two_s, 'cond': cond}

    @classmethod
    def get_cross_keys(cls, matched, table):
        idx = {}
        for key, vals in table.items():
            key = key.rstrip('_')
            false = [matched[j] for j in vals[0] if j in matched]
            true = [matched[j] for j in vals[1] if j in matched]
            if vals['cond'] == 'or':
                one_reduce = np.logical_or.reduce(true)
            else:
                one_reduce = np.logical_and.reduce(true)
            tmp = np.logical_and(
                one_reduce,
                ~np.logical_or.reduce(false))
            if key in idx:
                idx[key] = np.logical_or(tmp, idx[key])
            else:
                idx[key] = tmp
        idx['Nan'] = matched['nan']
        idx['Unknown'] = ~np.logical_or.reduce(list(matched.values()))
        idx['Other'] = ~np.logical_or.reduce([v for k, v in idx.items()])
        return idx

    @classmethod
    def get_sequence(cls, n, idx):
        out = np.full(n, '', dtype=object)
        # out = np.full(n, '',
        #    dtype=f'S{len(max(list(idx.keys()), key=len))+3}')
        for key, val in list(idx.items())[::-1]:
            out[val] = key
        return out

    @classmethod
    def match_fn(cls, series, sequences, match_table):
        seq_match = cls.match_pat(series, sequences)
        full_table = {i: cls.convert_bool_table(pat=sequences, **row)
                      for i, row in match_table.items()}
        lst_idx = cls.get_cross_keys(seq_match, full_table)
        out = cls.get_sequence(len(series), lst_idx)
        debug = pd.DataFrame(seq_match).apply(
            lambda x: '+'.join([str(i) for i in x[x].index]),
            axis=1).rename('debug')
        return out, debug

    def __classify__(self):
        data = pd.read_csv(self._in_path, sep=self._sep)
        res, debug = self.match_fn(data[self._col], self._seq,
                                   self._match_table)
        return pd.concat([data[self._key], data[self._col],
                          pd.Series(res, name=self._out), debug], axis=1)

    def __transform_fn__(self):
        sequence = self.__classify__()
        sequence.to_csv(self._out_path, index=False)


series_desc_kwargs = {
    'key': 'SeriesInstanceUID',
    'col': 'SeriesDescription',
    'out': 'SERDesc'
}

performed_proc_kwargs = {
    'key': 'SeriesInstanceUID',
    'col': 'PerformedProcedureStepDescription',
    'out': 'PerfProc'
}


body_part_kwargs = {
    'key': 'SeriesInstanceUID',
    'col': 'BodyPartExamined',
    'out': 'Body'
}


protocol_name_kwargs = {
    'key': 'SeriesInstanceUID',
    'col': 'ProtocolName',
    'out': 'Protocol'
}


study_desc_kwargs = {
    'key': 'StudyInstanceUID',
    'col': 'StudyDescription',
    'out': 'STDesc'
}


angio_flag_kwargs = {
    'key': 'SeriesInstanceUID',
    'col': 'AngioFlag',
    'out': 'AngioFlag'
}


contrast_route_kwargs = {
    'key': 'SeriesInstanceUID',
    'col': 'ContrastBolusRoute',
    'out': 'Route'
}


contrast_agent_kwargs = {
    'key': 'SeriesInstanceUID',
    'col': 'ContrastBolusAgent',
    'out': 'Agent'
}


convo_kernel_kwargs = {
    'key': 'SeriesInstanceUID',
    'col': 'ConvolutionKernel',
    'out': 'Kernel'
}
