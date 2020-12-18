#! /usr/bin/env python

__all__ = [
    'spliting_text', 'check_end_sentence',
    'topic_matcher', 'get_topics', 'join_sentence'
    ]

from typing import List
from collections import defaultdict
from _mappings import title_prefix, stopwords, contractions

def spliting_text(text: str) -> List[List[str]]:
    '''
    Spliting text in to a list of sentences.
    Each sentence is represented by a list of words.
    >>> spliting_text('Good morning, Mr. Smith. Welcome to https://www.fetchrewards.com/. How are we doing, today?')
    [['Good', 'morning,', 'Mr.', 'Smith.'], ['Welcome', 'to', 'https://www.fetchrewards.com/.'], ['How', 'are', 'we', 'doing,', 'today?']]
    >>> spliting_text("Mr. John Johnson Jr. was born in the U.S.A but earned his Ph.D. in Israel before joining Nike Inc. as an engineer. He also worked at craigslist.org as a business analyst.")
    [['Mr.', 'John', 'Johnson', 'Jr.', 'was', 'born', 'in', 'the', 'U.S.A', 'but', 'earned', 'his', 'Ph.D.', 'in', 'Israel', 'before', 'joining', 'Nike', 'Inc.', 'as', 'an', 'engineer.'], ['He', 'also', 'worked', 'at', 'craigslist.org', 'as', 'a', 'business', 'analyst.']]
    '''
    if not isinstance(text, str):
        raise TypeError("The text needs to be a string!")

    text = text.replace("\n", " ")
    if len(text) == 0:
        return [[]]
    
    sentences = [[]]
    words = text.split(" ")
    num_words = len(words)
    for i in range(num_words):
        word = words[i]
        if len(word) == 0:
            continue

        # Append word to current sentence
        sentences[-1].append(word)
        if i == num_words-1:
            break

        # Check if the sentence has ended
        if check_end_sentence(word, words[i+1]):
            sentences.append([])

    return sentences


def check_end_sentence(word: str, next_word: str) -> bool:
    # Based on punctuation
    if word[-1] in "?!":
        return True

    if word[-1] not in """"'.""":
        return False

    # Check if last char is ' or "
    if word[-1] == """"'""":
        if len(word) > 1 and word[-2] in ".?!":
            return True
        else:
            return False

    # Check if current word (ending with . ) is INDEED end of the sentence.
    # Assuming starting a sentence with a lower case word is not allowed.
    if next_word[0].islower():
        return False

    # title_prefix is a set of words that could lead a uppercase word.
    # There could be more than those listed in _mappings.py.
    # title_prefix = {"Mr.", "Mrs.", "Ms.", "Mx.", "Dr.", "St.", ... }
    return word not in title_prefix


def topic_matcher(a: List[List[str]], b: List[List[str]]) -> dict:
    topics_a = get_topics(a)
    topics_b = get_topics(b)

    common_topics = {}
    for t in topics_a:
        if t in topics_b:
            common_topics[t] = min(topics_a[t], topics_b[t])

    return common_topics


def get_topics(text: List[List[str]]) -> defaultdict:
    topics = defaultdict(int)
    for sentence in text:
        for word in sentence:
            w = word.lower()
            while w and not w[-1].isalpha():
                w = w[:-1]
                
            if w and (w in stopwords or w in contractions):
                continue
            
            topics[w] += 1

    return topics


def join_sentence(text: List[List[str]]) -> List[str]:
    if len(text[0]) == 0:
        return []

    sentences = []
    for sentence in text:
        sentences.append(" ".join(sentence))

    return sentences
