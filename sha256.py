class sha256:
    def __init__(self):
        self.iniHash = {
            "a": 0x6a09e667,
            "b": 0xbb67ae85,
            "c": 0x3c6ef372,
            "d": 0xa54ff53a,
            "e": 0x510e527f,
            "f": 0x9b05688c,
            "g": 0x1f83d9ab,
            "h": 0x5be0cd19}

        self.iniCons = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    def strTosBin(self, text: str) -> str:
        return ''.join(map(lambda x: bin(ord(x))[2:].zfill(8), text))

    def splitAndPadd(self, sBin: str) -> list:
        chunks = []
        result = []
        while len(sBin) > 448:
            chunks.append(sBin[0:448])
            sBin = sBin[0:448]
        else:
            if sBin:
                chunks.append(sBin)

        for ch in chunks:
            k = 448 - (len(ch) + 1)
            l = len(ch)

            ch = ch + '1' + ('0' * k) + (bin(l)[2:].zfill(64))
            result.append(ch)
        return result

    def rotl(self, n: int, x: int, w: int = 32) -> int:
        return (x << n) | (x >> w - n)

    def rotr(self, n: int, x: int, w: int = 32) -> int:
        return (x >> n) | (x << w - n)

    def maj(self, x: int, y: int, z: int) -> int:
        return (x & y) ^ (x & z) ^ (y & z)

    def ch(self, x: int, y: int, z: int) -> int:
        return (x & y) ^ (~x & z)

    def Sig0(self, x: int) -> int:
        return self.rotr(2, x) ^ self.rotr(13, x) ^ self.rotr(22, x)

    def Sig1(self, x: int) -> int:
        return self.rotr(6, x) ^ self.rotr(11, x) ^ self.rotr(25, x)

    def sig0(self, x: int) -> int:
        return (self.rotr(7, x) ^ self.rotr(18, x)) ^ (x >> 3)

    def sig1(self, x: int) -> int:
        return (self.rotr(17, x) ^ self.rotr(19, x)) ^ (x >> 10)

    @staticmethod
    def modAdd(x: list, w: int = 2**32) -> int:
        return sum(x) % w

    def getHash(self, message):
        M = self.splitAndPadd(self.strTosBin(message))
        a = self.modAdd

        ini = self.iniHash.copy()

        # MAIN LOOP
        for m in M:
            # splitting into 32b words
            W = [int(m[i:i + 32], 2) for i in range(0, len(m), 32)]

            # getting 64 words
            for i in range(64 - 16):
                W.append(a([self.sig1(W[-2]), W[-7], self.sig0(W[-15]), W[-16]]))

            for i in range(64):
                # setting up Temp's
                T1 = a([self.Sig1(ini['e']),
                        self.ch(ini['e'], ini['f'], ini['g']),
                        ini['h'],
                        self.iniCons[i],
                        W[i]])

                T2 = a([self.Sig0(ini['a']),
                        self.maj(ini['a'], ini['b'], ini['c'])])

                # moving one down
                ini['h'] = ini['g']
                ini['g'] = ini['f']
                ini['f'] = ini['e']
                ini['e'] = a([ini['d'], T1])
                ini['d'] = ini['c']
                ini['c'] = ini['b']
                ini['b'] = ini['a']
                ini['a'] = a([T1, T2])

        # adding up initial to end result
        for i in ini:
            ini[i] = a([ini[i], self.iniHash[i]])

        digest = ''.join([hex(i)[2:] for i in ini.values()])
        return digest
