from dicom_labelling import metadata_kwargs as met_args
from dicom_labelling import text_matching_args as txm_args
from dicom_labelling import TextMatching, mix_args
from difflib import unified_diff

def main_classify(mt_path, out_path):
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
        **mix_args(met_args.series_desc_kwargs,
                 txm_args.sequence_kwargs))
    seq_series_desc_class.__transform_fn__()


# A typical file csv need to contain only 2 columns
# the key columns, provided in the first dictionary. E.g. SeriesInstanceUID
# the columns to parse. E.g. SeriesDescription
# it can contains more, it doesn't matter, it will ignore the rest
def test_main_csv():
    # the path to the csv which contains the columns you want to use
    ser_mt_MR = './tests/example/ex1.csv'
    # path to the output file (name)
    out_sequence_label = './tests/example/out1.csv'
    main_classify(ser_mt_MR, out_sequence_label)
    with open('./tests/example/out_test.csv', "r") as f:
        expected_lines = f.readlines()
    with open(out_sequence_label, "r") as f:
        actual_lines = f.readlines()
    diff = list(unified_diff(expected_lines, actual_lines))
    assert diff == [], "Unexpected file contents:\n" + "".join(diff)
