from difflib import SequenceMatcher
from typing import List
from _mappings import contractions


class sequence_referee(SequenceMatcher):
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
            if "'" in word and word in contractions:
                equiv_phrase = contractions[word][0]
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
                extra_len = match - 1
                self._len_matches += extra_len
                self._la += extra_len

        else:
            match = self.check_contraction_matches(block_b, block_a)
            if match > 0:
                extra_len = match - 1
                self._len_matches += extra_len
                self._lb += extra_len

        if match == 0:
            extra_len_a = self.check_contraction_unmatched(block_a)
            self._la += extra_len_a
            
            extra_len_b = self.check_contraction_unmatched(block_b)
            self._lb += extra_len_b

    
    def check_contraction_unmatched(self, block: List[str]):
        for word in block:
            if "'" in word and word in contractions:
                equiv_phrase = contractions[word][0]
                return len(equiv_phrase.split(" ")) - 1
                
        return 0
 

    def check_contraction_matches(self, short_block: List[str], long_block: List[str]) -> int:
        for word in short_block:
            if "'" not in word or word not in contractions:
                continue
          
            for phrase in contractions[word]:
                expanded = phrase.split(" ")
                if all(e in long_block for e in expanded):
                    return len(expanded)
        
        return 0





