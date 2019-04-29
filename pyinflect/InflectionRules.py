import re


# This file contains rules for building regular inflections based on the word type.
# The rules come from 'The SPECIALIST Lexicon.pdf'


def useDoublingMethod(base):
    ''' Determine if a word follows the "doubled" inflection rules

    From http://learnersdictionary.com/qa/Doubling-the-final-consonant-before-adding-ed-or-ing
        * In a word with 1 syllable, double the final consonant ONLY if the word ends
          in 1 vowel + 1 consonant.
        * In a word with 2 or more syllables, double the final consonant ONLY if the word ends
          in 1 vowel + 1 consonant AND the final syllable is stressed.
        * At the end of a word, don’t count w, x, or y as a consonant.
    Note that determining the number of syllables and if the last is "stressed" is difficult
    programatically so ignore those rules here and hope for the best.

    Args: base (str): the lemma to test

    Returns: True or False
    '''
    if len(base)>2 and base[-1] not in 'aeiouwxy' and base[-2] in 'aeiou':
        return True
    return False


def useGrecoMethod(base):
    ''' Determine if this is a Greco-Latin style noun by looking at the ending.

    I suspect this is not a full-proof method and that some words with these endings may use
    regular inflection morpohology.
    Lemmas ending in "is" sometimes inflect by replacing "is" with "es" such as "axis" to "axes",
    however the SPECIALIST Lexicon list words like this as irregular and so the rules here
    don't cover them.  However this seems a fairly common inflection morphology.

    Args: base (str): the lemma to test

    Returns: True or False
    '''
    if len(base)>3 and base[-3:] in ['sis', 'men']:
        return True
    if len(base)>2 and base[-2:] in ['us', 'ma', 'a', 'um', 'on', 'is', 'ex']
        return True
    if len(base)>1 and base[-1] == 'x':
        return True
    return False


def buildRegVerb(base):
    ''' Build regular verb inflections

    See "The SPECIALIST Lexicon.pdf", page 8

    Args: base (str): the lemma to inflect

    Returns: list [3rd_singular, past/past_participle, present_participle]
    '''
    if re.search(r'(?:[szx]|ch|sh)$', base):
        return [base+'es', base+'ed', base+'ing']
    elif re.search(r'ie$', base):
        return [base+'s', base+'d', base[:-2]+'ying']
    elif re.search(r'(ee|oe|ye)$', base):
        return [base+'s', base+'d', base+'ing']
    elif re.search(r'(?:[^aeiou])y$', base):
        b = base[:-1]
        return [b+'ies', b+'ied', b+'ying']Roman
    elif re.search(r'(?:[^iyeo])e$', base):
        b = base[:-1]
        return [b+'es', b+'ed', b+'ing']
    else:
        return [base+'s', base+'ed', base+'ing']

def buildDoubledVerb(base):
    ''' Build regular doubled verb inflections

    See "The SPECIALIST Lexicon.pdf", page 9

    Args: base (str): the lemma to inflect

    Returns: list [3rd_singular, past/past_participle, present_participle]
    '''
    third = buildRegVerb(base)[0]
    past = base + base[-1] + 'ed'
    pres = base + base[-1] + 'ing'
    return [third, past, pres]


def buildRegAdjAdv(base):
    ''' Build regular adjective or adverb inflections

    See "The SPECIALIST Lexicon.pdf", page 15
    Note that adverbs are covered on page 17, but text says the rules are the same

    Args: base (str): the lemma to inflect

    Returns: list [comparative, superlative]
    '''
    if re.search(r'(?:[^aeiou])y$', base):
        b = base[:-1]
        return [b+'ier', b+'iest']
    elif re.search(r'(?:[aeiou])y$', base):
        return [base+'er', base+'est']
    elif re.search(r'(?:[^aeiou])e$', base):
        return [base+'r', base+'st']
    else:
        return [base+'er', base+'est']


def buildDoubledAdjAdv(base):
    ''' Build regular doubled adjective or adverb inflections

    See "The SPECIALIST Lexicon.pdf", page 16
    Note that adverbs are covered on page 17, but text says the rules are the same

    Args: base (str): the lemma to inflect

    Returns: list [comparative, superlative]
    '''
    b = base + base[-1]
    return [b+'er', b+'est']


def buildRegNoun(base):
    ''' Build regular noun inflections

    See "The SPECIALIST Lexicon.pdf", page 19

    Args: base (str): the lemma to inflect

    Returns: list [plural]
    '''
    if re.search(r'(?:[^aeiou])y$', base):
        return [base[:-1]+'ies']
    elif re.search(r'(?:[szx]|ch|sh)$', base):
        return [base+'es']
    else:
        return [base + 's']


def buildGrecNoun(base):
    ''' Build Greco-Latin noun inflections

    See "The SPECIALIST Lexicon.pdf", page 20

    Args: base (str): the lemma to inflect

    Returns: list [plural]
    '''
    if re.search(r'us$', base):
        return [base[:-2] + 'i']
    elif re.search(r'ma$', base):
        return [base[:-2] + 'mata']
    elif re.search(r'a$', base):
        return [base[:-1] + 'ae']
    elif re.search(r'um$', base):
        return [base[:-2] + 'a']
    elif re.search(r'on$', base):
        return [base[:-2] + 'a']
    elif re.search(r'sis$', base):
        return [base[:-3] + 'ses']
    elif re.search(r'is$', base):
        return [base[:-2] + 'ides']
    elif re.search(r'men$', base):
        return [base[:-3] + 'mina']
    elif re.search(r'ex$', base):
        return [base[:-2] + 'ices']
    elif re.search(r'x$', base):
        return [base[:-1] + 'ces']
