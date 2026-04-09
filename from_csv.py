import pandas as pd
import os

csv_dir = 'csv'


def make_seq_dict(path):
    df = pd.read_csv(path)
    return df.groupby('Key')['Expression'].aggregate(
        lambda x: list(x)).to_dict()


def make_match_table(path):
    alias = {0: 'zero', 1: 'one', 2: 'two'}
    df = pd.read_csv(path, index_col='Label')
    res = {}
    for i in df.iloc:
        res[i.name] = {}
        res[i.name]['cond'] = i['cond']
        res[i.name]['one'] = []
        res[i.name]['two'] = []
        res[i.name]['zero'] = []
        for j in i.items():
            if j[0] == 'cond':
                continue
            res[i.name][alias[j[1]]].append(j[0])
    return res


def load_directory_csv(path):
    ls = os.listdir(path)
    res = {}
    for i in ls:
        if i.endswith('.csv'):
            out, f_type = i.split('_', 1)
            f_type = f_type[:-4]
            if f_type == 'seq_dict':
                tmp = make_seq_dict(os.path.join(path, i))
            else:
                tmp = make_match_table(os.path.join(path, i))
            if out not in res:
                res[out] = {}
            res[out][f_type] = tmp
    return res


if __name__ == '__main__':
    load_directory_csv(csv_dir)
