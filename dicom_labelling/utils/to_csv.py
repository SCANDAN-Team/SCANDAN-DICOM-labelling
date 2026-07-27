import pandas as pd
from dicom_labelling import text_matching_args as txm_args
from dicom_labelling import TextMatching
import os
import argparse

to_export = [
    txm_args.sequence_kwargs,
    txm_args.angio_kwargs,
    txm_args.body_kwargs,
    txm_args.contrast_kwargs,
    txm_args.boolean_kwargs,
    txm_args.empty_kwargs,
    txm_args.kernel_kwargs,
]


def create_df_seq_dict(seq_dict):
    return pd.DataFrame([(k, i) for k, v in seq_dict.items() for i in v],
                        columns=['Key', 'Expression'])


def create_df_match_table(match_table, seq_dict):
    full_table = {i: TextMatching.convert_bool_table(pat=seq_dict, **row)
                  for i, row in match_table.items()}
    res = {}
    for key in full_table:
        tmp = {i: k for k, v in full_table[key].items()
               if k != 'cond'
               for i in v}
        tmp['cond'] = full_table[key]['cond']
        res[key] = tmp
    return pd.DataFrame(res).T.reset_index().rename(columns={'index': 'Label'})


def create_csv(path, match_table, seq_dict, out):
    df_seq_dict = create_df_seq_dict(seq_dict)
    df_match_table = create_df_match_table(match_table, seq_dict)
    os.makedirs(path, exist_ok=True)
    df_seq_dict.to_csv(os.path.join(path, f'{out}_seq_dict.csv'), index=False)
    df_match_table.to_csv(os.path.join(path, f'{out}_match_table.csv'),
                          index=False)


def to_csv():
    argp = argparse.ArgumentParser('From csv')
    argp.add_argument("dir", type=str, default='csv',
                      help="The folder directory")
    args = argp.parse_args()
    for i in to_export:
        create_csv(args.dir, **i)

