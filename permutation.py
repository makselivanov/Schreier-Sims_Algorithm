import copy


class Permutation(object):
    def __init__(self, size=None, perm=None):
        if size is not None and (not isinstance(size, int) or size <= 0):
            raise Exception("Incorrect Size")
        if size is not None and perm is not None and size != len(perm):
            raise Exception("Incorrect Arguments")
        if size is not None and perm is None:
            perm = [i for i in range(size)]
        if perm is not None:
            n = len(perm)
            test_perm = set(perm)
            for i in range(n):
                if i not in test_perm:
                    raise Exception("Incorrect Permutation")
                test_perm.remove(i)
            self._perm = copy.deepcopy(tuple(perm))
            return
        raise Exception("Arguments is Empty")

    def __len__(self):
        return len(self._perm)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True

    def __getitem__(self, item: int):
        return self._perm[item]

    def __call__(self, item: int):
        return self[item]

    def __mul__(self, other):
        if len(self) != len(other):
            raise Exception("Different Length in Permutation's Multiplication")
        return Permutation(perm=[self[other[i]] for i in range(len(self))])

    def __invert__(self):
        perm = [None] * len(self)
        for i in range(len(self)):
            perm[self[i]] = i
        return Permutation(perm=perm)

    def __str__(self):
        return "(" + ", ".join(map(lambda x: str(x[0]) + ": " + str(x[1]), enumerate(self._perm))) + ")"

    def __repr__(self):
        return "(" + ", ".join(map(lambda x: str(x[0]) + ": " + str(x[1]), enumerate(self._perm))) + ")"

    def __pow__(self, power: int):
        if power < 0:
            perm = ~Permutation(size=len(self))
            base = ~Permutation(perm=self._perm)
            power *= -1
        else:
            perm = Permutation(size=len(self))
            base = Permutation(perm=self._perm)
        for i in range(power):
            perm *= base
        return perm

    def ord(self):
        step = 1
        perm = Permutation(perm=self._perm)
        while perm != Permutation(size=len(self)):
            step += 1
            perm *= self
        return step

    def __hash__(self):
        return hash(self._perm)
