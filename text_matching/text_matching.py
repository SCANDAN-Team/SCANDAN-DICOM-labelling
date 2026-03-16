def mix_args(dict_key, dict_txt):
    res = dict_key | dict_txt
    res['out'] += '_' + dict_key['out']
    return res


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


# convo_kernel_kwargs = {
#     'key': 'SeriesInstanceUID',
#     'col': 'ConvolutionKernel',
#     'out': 'Kernel'
# }
