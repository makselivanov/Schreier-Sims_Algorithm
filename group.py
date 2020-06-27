from permutation import Permutation
from itertools import islice


def build_schreier_tree(b: int, gen):
    n = len(next(iter(gen)))

    def dfs(b, gen, orbit, prev):
        for g in gen:
            if g[b] not in orbit:
                orbit[g[b]] = g * orbit[b]
                prev[g[b]] = g
                dfs(g[b], gen, orbit, prev)
    orbit = {b: Permutation(n)}
    prev = {b: Permutation(n)}
    dfs(b, gen, orbit, prev)
    return orbit, prev


def make_gen(gen, orbit):
    n = len(next(iter(gen)))
    new_gen = set()
    for g in gen:
        for a in orbit:
            new_gen.add(~(orbit[g[a]]) * g * orbit[a])
    return new_gen


def shrink_gen(gen):
    n = len(next(iter(gen)))
    new_gen = set()
    base = [{} for i in range(n)]
    for g in gen:
        for x in range(0, n):
            if g[x] != x:
                if g[x] in base[x]:
                    g = (~g) * base[x][g[x]]
                else:
                    base[x][g[x]] = g
                    new_gen.add(g)
                    break
    return new_gen


class StabChain(object):
    def __init__(self, gen, base=None):
        self._ord = None
        self.n = len(next(iter(gen)))
        self.gen = set(gen)
        self.tree_list = []
        self.prev_tree_list = []
        gen = set(gen)
        if base is None:
            base = range(self.n)
        for b in base:
            if b < 0 or b >= self.n or not isinstance(b, int):
                raise ValueError("Error in base")
        base = iter(base)
        self.base = []
        while gen:
            b = next(base)
            self.base.append(b)
            orbit, prev = build_schreier_tree(b, gen)
            self.tree_list.append(orbit)
            self.prev_tree_list.append(prev)
            gen = shrink_gen(make_gen(gen, orbit))

    def get_first_orbit(self):
        return set(map(lambda x: x[0], next(iter(self.tree_list)).items()))

    def ord(self):
        if self._ord is None:
            self._ord = 1
            for tree in self.tree_list:
                self._ord *= len(tree)
        return self._ord

    def factoring(self, perm):
        step = dict()
        for g in self.gen:
            step[g] = 0
        perm = Permutation(perm=perm)
        for i in range(len(self.base)):
            while perm[self.base[i]] != self.base[i]:
                step[(self.prev_tree_list[i][perm[self.base[i]]])] += 1
                perm = ~(self.prev_tree_list[i][perm[self.base[i]]]) * perm
        if perm != Permutation(size=len(perm)):
            return None
        return step



    def get_generators(self, index: int):
        if index < 0 or index > len(self.tree_list):
            raise ValueError("Invalid index")
        for (_, g) in self.tree_list[index]:
            pass # if () # TODO

    def get_stabchain(self, index: int):
        if index < 0 or index > len(self.tree_list):
            raise ValueError("Invalid index")
        pass # TODO

