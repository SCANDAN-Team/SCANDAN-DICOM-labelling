from text_matching import text_matching as txm
import text_matching as txm_args

from tool_text_matching import TextMatching


def main_classify(out_path, mt_path):
    # txm.mix_args is simply a union of dict
    # there's 2 type of dictionary
    # the first is the for the columns to use. It contains the key to use as
    #  identifier for the columns (e.g. the SOPID, SeriesInstanceUID, ...),
    #  the name of the columns, and the name to give to the output.
    #  You can find them in ./text_matching/text_matching
    # the second is for the feature to generate. They are taken from
    #  the different files stored in ./text_matching. They contains the
    #  dictionary of regexp, the match table to use to create the rules,
    #  and the name of the output
    # That is because the same rules can be applied to different features.
    #  For example the body rules can be applied to the series description,
    #  the study description, or the body part examined.
    seq_series_desc_class = TextMatching(
        in_path=mt_path,
        out_path=out_path,
        **txm.mix_args(txm.series_desc_kwargs,
                       txm_args.sequence_kwargs))
    seq_series_desc_class.__transform_fn__()


# A typical file csv need to contain only 2 columns
# the key columns, provided in the first dictionary. E.g. SeriesInstanceUID
# the columns to parse. E.g. SeriesDescription
# it can contains more, it doesn't matter, it will ignore the rest
def main():
    # the path to the csv which contains the columns you want to use
    ser_mt_MR = 'path'
    # path to the output file (name)
    out_sequence_label = 'path'
    main_classify(ser_mt_MR, out_sequence_label)


if __name__ == '__main__':
    main()
