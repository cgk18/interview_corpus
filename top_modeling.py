'''
Chris Kim
Updated Nov 23, 2024
'''

'''
New idea:

instead of breaking up the interview per speaker, break into chunks at which the interviewer speaks. 

Use word embedding to group these into the interviewer guide
''' 

import re
from collections import defaultdict


from nltk.tokenize import sent_tokenize
