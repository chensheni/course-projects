'''
This code is provided solely for the personal and private use of students
taking the CSC401H/2511H course at the University of Toronto. Copying for
purposes other than this use is expressly prohibited. All forms of
distribution of this code, including but not limited to public repositories on
GitHub, GitLab, Bitbucket, or any other online platform, whether as given or
with any changes, are expressly prohibited.

Authors: Sean Robertson, Jingcheng Niu, Zining Zhu, and Mohamed Abdall
Updated by: Raeid Saqur <raeidsaqur@cs.toronto.edu>

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 University of Toronto
'''

'''Calculate BLEU score for one reference and one hypothesis

You do not need to import anything more than what is here
'''

from math import exp  # exp(x) gives e^x
from typing import List, Sequence, Iterable


def grouper(seq:Sequence[str], n:int) -> List:
    '''Extract all n-grams from a sequence

    An n-gram is a contiguous sub-sequence within `seq` of length `n`. This
    function extracts them (in order) from `seq`.

    Parameters
    ----------
    seq : sequence
        A sequence of words or token ids representing a transcription.
    n : int
        The size of sub-sequence to extract.

    Returns
    -------
    ngrams : list
    '''
    grams_cnt = len(seq) - (n-1)
    ngrams    = [seq[i: i+n] for i in range(grams_cnt)]

    return ngrams


def n_gram_precision(reference:Sequence[str], candidate:Sequence[str], n:int) -> float:
    '''Calculate the precision for a given order of n-gram

    Parameters
    ----------
    reference : sequence
        The reference transcription. A sequence of words or token ids.
    candidate : sequence
        The candidate transcription. A sequence of words or token ids
        (whichever is used by `reference`)
    n : int
        The order of n-gram precision to calculate

    Returns
    -------
    p_n : float
        The n-gram precision. In the case that the candidate has length 0,
        `p_n` is 0.
    '''
    ref_grams = grouper(reference, n)
    can_grams = grouper(candidate, n)

    p_n = 0
    if len(candidate) != 0 and len(candidate) > n:
        concurrence = sum([1 for gram in can_grams if gram in ref_grams])
        p_n = float(concurrence) / float(len(can_grams))
    
    return p_n


def brevity_penalty(reference:Sequence[str], candidate:Sequence[str]) -> float:
    '''Calculate the brevity penalty between a reference and candidate

    Parameters
    ----------
    reference : sequence
        The reference transcription. A sequence of words or token ids.
    candidate : sequence
        The candidate transcription. A sequence of words or token ids
        (whichever is used by `reference`)

    Returns
    -------
    BP : float
        The brevity penalty. In the case that the candidate transcription is
        of 0 length, `BP` is 0.
    '''
    if len(candidate) == 0:
        return 0

    brevity = float(len(reference)) / float(len(candidate))

    if brevity < 1:
        return 1
    else:
        return float(exp(1 - brevity))


def BLEU_score(reference:Sequence[str], candidate:Sequence[str], n) -> float:
    '''Calculate the BLEU score

    Parameters
    ----------
    reference : sequence
        The reference transcription. A sequence of words or token ids.
    candidate : sequence
        The candidate transcription. A sequence of words or token ids
        (whichever is used by `reference`)
    n : int
        The maximum order of n-gram precision to use in the calculations,
        inclusive. For example, ``n = 2`` implies both unigram and bigram
        precision will be accounted for, but not trigram.

    Returns
    -------
    bleu : float
        The BLEU score
    '''
    BP = brevity_penalty(reference, candidate)
    grams_list = [i + 1 for i in range(n)]
    pn_product = 1.0

    for gram in grams_list:
        pn = n_gram_precision(reference, candidate, gram)
        pn_product *= pn

    bleu = float(BP * pow(pn_product, 1/len(grams_list)))
    return bleu
