"""GenSkew: Genomic nucleotide skew application"""

__version__ = '0.1'

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

from .lib import GenSkew
__all__ = 'lib'
