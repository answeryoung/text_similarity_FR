#! /usr/bin/env python

from difflib import SequenceMatcher
from typing import List
from _mappings import contractions


class sequence_referee(SequenceMatcher):
    r"""
    sequence_referee is a class extended from SequenceMatcher.
    The derived class has a method score(), which behaves similarly
    than ratio() of the base class.

    For the purpose matching sequences of words, dealing with contractions
    become the added feature of this class. As we wish to expand all 
    contractions to the expanded form and the mapping is one-to-many,
    we first look locate a contraction in one sequence then check if any
    of the expanded form exist in the other sequence.
    """

    def score(self) -> float:
        codes = self.get_opcodes()

        self._len_matches = 0
        self._la, self._lb = len(self.a), len(self.b)

        for c in codes:
            if c[0] == 'equal':
                # matching_block_size = c[2] - c[1] if no contractions
                self.increment_len_matches(self.a[c[1]:c[2]])

            else:
                self.check_contractions(self.a[c[1]:c[2]], self.b[c[3]:c[4]])                

        return self._len_matches / (self._la * self._lb)**0.5


    def increment_len_matches(self, words: List[str]) -> None:
        matching_block_size = len(words)
        for word in words:
            if "'" in word and word.lower() in contractions:
                equiv_phrase = contractions[word.lower()][0]
                extra_len = len(equiv_phrase.split(" ")) - 1
                matching_block_size += extra_len
                self._la += extra_len
                self._lb += extra_len

        self._len_matches += matching_block_size
        

    def check_contractions(self, block_a: List[str], block_b: List[str]) -> None:
        match = 0
        if len(block_b) >= len(block_a):
            match = self.check_contraction_matches(block_a, block_b)
            if match > 0:
                self._len_matches += match
                self._la += match - 1

        else:
            match = self.check_contraction_matches(block_b, block_a)
            if match > 0:
                self._len_matches += match
                self._lb += match - 1

        if match == 0:
            extra_len_a = self.check_contraction_unmatched(block_a)
            self._la += extra_len_a
            
            extra_len_b = self.check_contraction_unmatched(block_b)
            self._lb += extra_len_b

    
    def check_contraction_unmatched(self, block: List[str]) -> int:
        extra_len = 0
        for word in block:
            if "'" in word and word.lower() in contractions:
                equiv_phrase = contractions[word.lower()][0]
                extra_len += len(equiv_phrase.split(" ")) - 1
                
        return extra_len
 

    def check_contraction_matches(self, short_block: List[str], long_block: List[str]) -> int:
        long_block_lower = [word.lower() for word in long_block]
        for word in short_block:
            if "'" not in word or word.lower() not in contractions:
                continue
          
            for phrase in contractions[word.lower()]:
                expanded = phrase.split(" ")
                if all(e in long_block_lower for e in expanded):
                    return len(expanded)
        
        return 0
