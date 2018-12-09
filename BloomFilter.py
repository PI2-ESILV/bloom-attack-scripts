# Python 3 program to build Bloom Filter
# Install mmh3 and bitarray 3rd party module first
# pip install mmh3
# pip install bitarray


import math
import mmh3
from bitarray import bitarray


class BloomFilter(object):

    UPDATE_NONE = 0
    UPDATE_ALL = 1
    UPDATE_P2PUBKEY_ONLY = 2
    UPDATE_MASK = 3

    def __init__(self, items_count, fp_prob, nTweak, nFlags):
        self.fp_prob = fp_prob

        # Size of bit array to use
        self.size = self.get_size(items_count, fp_prob)

        # number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items_count)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

        self.nTweak = nTweak
        self.nFlags = nFlags

    def add(self, item):

        digests = []
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)

            self.bit_array[digest] = True

    def check(self, item):

        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
                return False
        return True

    @classmethod
    def get_size(self, n, p):

        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):

        k = (m / n) * math.log(2)
        return int(k)

    __struct = struct.Struct(b'<IIB')

    def serialize(self):
        return struct.pack("I", len(self.bit_array)) + self.bit_array \
               + self.__struct.pack(self.hash_count, self.nTweak, self.nFlags)