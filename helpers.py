import os
from sys import platform

import constants

def format_sentences(text):
    words = text.split()
    i = 0
    sentence = ''
    sentences = []
    while True:
        if i < len(words):
            if len(sentence) < constants.MAX_WIDTH:
                sentence += words[i] + ' '
                i += 1
            else:
                sentences.append(sentence[0:-1])
                sentence = ''
        else:
            sentences.append(sentence[0:-1])
            break
    return '\n'.join(sentences)

def format_path(p):
    path = ''
    # Attempt to make this portable by performing the right kind of path expansion
    if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
        if '~' in p:
            path = os.path.expanduser(p)
        elif '$HOME' in p:
            rest_path = p.strip('$HOME')
            path = '{}{}'.format(os.environ['HOME'], rest_path)
        else:
            path = os.path.abspath(p)
    elif platform == "win32":
        path = os.path.expandvars(repr(p))

    return path
