def get_start_to_end(i):
    return f'^{i}$'


# maybe use
# maybe no
def gste(i):
    return get_start_to_end(i)
    # return i


# SIEMENS
# Format is
# Kg?XYz
# K is the kernel family
# g is the optional kernel subgroup, from newer model
# XY are the kernel numbers
# z is the kernel subgroup
#
# Alternate format can be
# ['KgXYz', 'N']
# Where KgXYz is the same as above
# and N is.... unknown? Potentially related to beam hardening correction
# with from 1=fine noise and 7=brain (again, maybe)
#
# To simplify, we match KgXYz because regexp are cool
#
#
# Note:
# H08s / B08s  Single-photon emission computed tomography
# Hc is supposed to be crisp enhancement for bone only
#
SIEMENS_KERNEL_FAMILY = 'HBQUCSIJT'
skf = f'[{SIEMENS_KERNEL_FAMILY}]'  # aliasing
# I and J are iterative reconstruction. UHR (Ultra High Resolution)
# H/I = HEAD
# B/J = BODY
# C = Child Head
# S = Special Application
# Q = Quantitative
# U = Ultra High resolution
SIEMENS_KERNEL_SUBGROUP = 'rfIvcp'
skg = f'[{SIEMENS_KERNEL_SUBGROUP}]'
# r = Regular
# f = fine noise optimisation
# I = lung optimised
# v = vascular optimised
# c = crisp edge enhancement
# p = pediatric optimisation
SIEMENS_KERNEL_NUMBER = r'\d{2}'
skn = SIEMENS_KERNEL_NUMBER  # aliasing
# XY format
# X[01234] = SMOOTH
# X[56789] = SHARP
# Y=special kernel, but usually means increment in sharpness
# Y[2] = no iterative beam hardening correction (PFO). Faster reconstruction
# Y[1] = finer grain noise than for same X
# Y=9 may means PET-kernel (somatom)
SIEMENS_KERNEL_SCAN_MODE = 'sfuh'
# s = standard
# f = fast
# u = with φ-FFS (Flying-focal-spot), with UHR  comb, high sampling
# h = high-resolution modes
skcm = f'[{SIEMENS_KERNEL_SCAN_MODE}]'


def build_siemens_kernel(family=None, group=None, number=None, mode=None,
                         group_optional=True):
    if family is None:
        family = skf
    if group is None:
        group = skg
    if number is None:
        number = skn
    if mode is None:
        mode = skcm
    if group_optional:
        go = '?'
    else:
        go = ''
    return fr'{family}{group}{go}{number}{mode}'


# aliasing
def bsk(*args, **kwargs):
    return build_siemens_kernel(*args, **kwargs)


# GE
# "easier" but also not that much details
# Format is much easier, a list of defined words,
# For some reason, SOFT# is also in our data
# SMOOTH, SOFT, STANDARD, STD+, DETAIL, BONE, BONEPLUS, CHST, EDGE, SHARP,
# LUNG, ULTRA, HD LUNG, STANDARD2, DETAIL2, BONE2, BONEPLUS2, EDGE2,
# STANDARDPLUS2, DETAILPLUS2, HD ULTA, HD SOFT
GE_WORDS = ['SMOOTH', 'SOFT#?', 'STANDARD', 'STD+', 'DETAIL', 'BONE',
            'BONEPLUS', 'CHST', 'EDGE', 'SHARP', 'LUNG', 'ULTRA', 'HD LUNG',
            'STANDARD2', 'DETAIL2', 'BONE2', 'BONEPLUS2', 'EDGE2',
            'STANDARDPLUS2', 'DETAILPLUS2', 'HD ULTA', 'HD SOFT']
gew = [gste(i) for i in GE_WORDS]


# Toshiba / Canon
# Format is
# F(|L)CXY
# FC is filter convolution
# FL is ?...
# XY are 2 numbers
#
# FC 01-09: Abdomen with BHC
# FC 11-19: Abdomen without BHC
# For X in [0,1]
# FC X1-X5: body filter, smooth towards sharp
# FC X6-X9: soft tissue filter, smooth towards sharp
#
# FC20-FC26, FC41-FC44, FC62-FC68: head
# FC21: soft
# FC23: soft
# FC26: soft
# FC43: angio?
# FC62: soft?
# FC63: soft?
# FC64: soft?
# FC67: soft?
#
# FC30: bone
# FC35: bone
# FC81: bone
def build_toshiba_kernel(cl='[CL]', x=None, y=None):
    if x is None:
        x = r'\d'
    if y is None:
        y = r'\d'
    return f'F{cl}{x}{y}'


def btk(*args, **kwargs):
    return build_toshiba_kernel(*args, **kwargs)


# PHILIPS
# Format is
# (X)?Y
# Y: [ABCDEFL]
# X: [UYCSH]
#
# Y
# A: Smooth (smoothing filter for soft tissue)
# B: Standard (standard filter for soft tissue)
# C: Sharp (sharper than B)
# D: Detail (edge enhancing filter for boe images)
# E: ? (sharp, but close to standard) > Internal physics and quality test
# F: Edge enhanced (sharp, high resolution, lung or bone)
# L: Edge enhanced (very sharp, high resolution, lung)
#
# X
# U: Seems to be designed for brain only
# C: Cardiac reconstruction filter
# Y: ? Y-Sharp (YA, YC) and Y-Detail (YB, YD)
# S: specialised brain reconstruction filter, increase HU value observed.
# Slightly enhanced the hyper-dense structures
# H: specialised brain reconstruction filter, increase HU value observed.
# Clearly enhances the hyper-dense structures.
#
#
# A: recommended for large patient
# B and C: recommended for routine abdomen and pelvis
# F and L: recommended for lungs, knee and shoulder
#
# UA: Brain smooth
# UB: Brain standard
# UC: Brain sharp
# SA/SB: Brain soft
# SC/SD: Brain routine
# SE/SF: Brain sharp
# HA/HB: Brain soft
# HC/HD: Brain routine
# HE/HF: Brain sharp
#
# YA: Sharp (bone)
# YB: Very Sharp (bone)
# YC: Sharp (lung, bone, IAC)
# YD: Very Sharp (lung, bone, IAC)
# YE: Very sharp and noisy
# YF: Extremely sharp. In fact the sharpest in the system.
def build_philips_kernel(x=None, y=None):
    if x is None:
        x = '[UYCSH]?'
    if y is None:
        y = '[ABCDEFL]'
    return gste(f'{x}{y}')


def bpk(*args, **kwargs):
    return build_philips_kernel(*args, **kwargs)


KERNEL_DICT = {
    # MANUFACTURER TAG
    'SIEMENS': [
        bsk()
    ],
    'GE': [
        *gew
    ],
    'TOSHIBA': [
        btk()
    ],
    'PHILIPS': [
        bpk()
    ],
    'SMOOTH': [
        bsk(number=r'[0-4]\d'),  # SIEMENS. e.g H20s
        gste('SOFT#?'), gste('DETAIL'), gste('STANDARD'),  # GE
        btk(cl='C', x='[01]', y='[12]'),  # TOSHIBA. FC01, FC02, FC11, FC12.
        btk(cl='C', x='[01]', y='[7]'),  # TOSHIBA. FC07, FC17.
        btk(cl='C', x='2', y='[0-6]'),  # TOSHIBA. FC20-FC26.
        btk(cl='C', x='6', y='[2-8]'),  # TOSHIBA. FC62-FC68.
        bpk(x='[USH]?', y='[AB]'),  # PHILIPS. A,B,UA,UB,SA,SB
        bpk(x='C', y='[AB]'),  # PHILIPS. CA,CB

    ],
    'SHARP': [
        bsk(number=r'[5-9]\d'),  # SIEMENS. e.g H61s
        gste('BONE'),  # GE. Or weirdly Canon in some case?
        gste('BONEPLUS'), gste('EDGE'),  # GE.
        btk(cl='C', x='[01]', y='[45]'),  # TOSHIBA. FC04, FC05, FC14, FC15.
        btk(cl='C', x='[01]', y='[9]'),  # TOSHIBA. FC09, FC19.
        btk(cl='C', x='3', y='[015]'),  # TOSHIBA. FC30, FC31, FC35
        btk(cl='C', x='8', y='[01]'),  # TOSHIBA. FC80, FC81.
        bpk(x='[U]?', y='[C]'),  # PHILIPS. C, UC
        bpk(x='', y='[DFLE]'),  # PHILIPS. D, F, L, E
        bpk(x='C', y='[CD]'),  # PHILIPS. CC,CD
        bpk(x='Y', y='[ABCDEF]'),  # PHILIPS. YA, YB, YC, YD

    ],
    'HEAD': [
        bsk(family='[HJ]'),  # SIEMENS. e.g H40s
        btk(cl='C', x='2', y='[0-6]'),  # TOSHIBA. FC20-FC26
        btk(cl='C', x='4', y='[1-4]'),  # TOSHIBA. FC41-FC44
        btk(cl='C', x='6', y='[2-8]'),  # TOSHIBA. FC62-FC68
        bpk(x='[USH]')  # PHILIPS. UA-UD, SA-SF, HA-HF
    ],
    'BODY': [
        bsk(family='[BI]'),  # SIEMENS. e.g. B30s
        btk(cl='C', x='[01]', y='[1-9]'),  # TOSHIBA. Abdomen. FC01-FC19
        bpk(x='C'),  # PHILIPS. CA-CD

    ],
    'ANGIO': [
        btk(cl='C', x='4', y='3'),  # TOSHIBA. CTA
    ],
    'LOC': [
        bsk(family='T'),  # SIEMENS. e.g. B30s
        btk(cl='L')  # TOSHIBA. FLXX
    ]
}

Manufacturer = ['SIEMENS', 'GE', 'TOSHIBA', 'PHILIPS']

MATCH_TABLE = {
    'BRAIN': {'cond': 'and', 'one': ['SMOOTH', 'HEAD'], 'two': Manufacturer},
    'BONE': {'cond': 'and', 'one': ['SHARP', 'HEAD'], 'two': Manufacturer},
    'SHARP': {'one': ['SHARP'], 'two': ['HEAD', 'BODY', *Manufacturer]},
    'SOFT': {'one': ['SMOOTH'], 'two': Manufacturer},
    'BODY_SOFT': {'cond': 'and', 'one': ['SMOOTH', 'BODY'],
                  'two': Manufacturer},
    'LOCALISER': {'one': ['LOC'], 'two': ['*'], 'zero': []},
}


kernel_kwargs = {'seq_dict': KERNEL_DICT, 'match_table': MATCH_TABLE,
                 'out': 'Kernel'}
