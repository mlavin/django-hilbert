"""
django-hilbert is one of many Django apps which is a loose collection of utility functions.
It is a mixture of Python code and Javascript that I find myself writing over and 
over. Primarily it focuses around utilities for AJAX and testing.
"""

__version_info__ = {
    'major': 0,
    'minor': 3,
    'micro': 0,
    'releaselevel': 'final'
}

def get_version():
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s' % __version_info__)
    return ''.join(vers)

__version__ = get_version()
