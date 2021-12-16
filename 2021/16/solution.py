from sys import argv
from typing import IO
from math import prod
from colorama import Style


class BitDispenser:
    def __init__(self, bit_line: str):
        self.data = bit_line

    def take(self, n):
        out = self.data[:n]
        self.data = self.data[n:]
        return out

    def take_int(self, n):
        return int(self.take(n), base=2)

    def take_bool(self):
        return self.take(1) == '1'

    @property
    def has_data_left(self):
        return any(b == '1' for b in self.data)


class Packet:
    def __init__(self, bit_stream: BitDispenser):
        self.version = bit_stream.take_int(3)
        self.id = bit_stream.take_int(3)

        self.subpackets = []

        if self.id == 4:  # literal value packet
            buffer = ''
            more = True
            while more:
                more = bit_stream.take_bool()
                buffer += bit_stream.take(4)
            self.literal_value = int(buffer, base=2)

        elif bit_stream.take_bool():  # number of subpackets
            n_packets = bit_stream.take_int(11)
            self.subpackets = [Packet(bit_stream) for _ in range(n_packets)]

        else:  # length of subpackets
            packets_length = bit_stream.take_int(15)
            packets_block = BitDispenser(bit_stream.take(packets_length))
            while packets_block.has_data_left:
                self.subpackets += [Packet(packets_block)]

    @property
    def version_sums(self):
        return self.version + sum(p.version_sums for p in self.subpackets)

    @property
    def value(self):
        if self.id == 0:
            return sum(p.value for p in self.subpackets)
        elif self.id == 1:
            return prod(p.value for p in self.subpackets)
        elif self.id == 2:
            return min(p.value for p in self.subpackets)
        elif self.id == 3:
            return max(p.value for p in self.subpackets)
        elif self.id == 4:
            return self.literal_value
        elif self.id == 5:
            return 1 if self.subpackets[0].value > self.subpackets[1].value else 0
        elif self.id == 6:
            return 1 if self.subpackets[0].value < self.subpackets[1].value else 0
        else:
            return 1 if self.subpackets[0].value == self.subpackets[1].value else 0


data_hex = open(argv[1]).readline().strip()
data_bin = bin(int(data_hex, base=16))[2:].zfill(len(data_hex)*4)

root = Packet(BitDispenser(data_bin))

print(f'version sum: {Style.BRIGHT}{root.version_sums}{Style.RESET_ALL}')

print(f'total value: {Style.BRIGHT}{root.value}{Style.RESET_ALL}')
