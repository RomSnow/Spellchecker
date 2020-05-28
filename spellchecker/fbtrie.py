class Trie:
    """Реализация FBTrie"""

    def __init__(self):
        self.root = {}

    def insert(self, word):
        """Добавление слова"""
        word = word + "\0"
        node = self.root
        for c in word:
            if c not in node:
                node[c] = {}
            node = node[c]

    def traverse(self, d, node, sofar):
        for c, child in node.items():
            if c == "\0":
                yield sofar, d
            else:
                yield from self.traverse(d, child, sofar + c)

    def fuzzy(self, query, k, k_fn=None, prefix=False):
        """Найти все слова расхождения с которыми меньше k"""
        n = len(query)
        tab = [[0] * (n + 1) for _ in range(n + k + 1)]
        for j in range(n + 1):
            tab[0][j] = j

        if not k_fn:
            k_fn = lambda _t: k
        yield from self.fuzzy_(k_fn, tab, self.root, 1, "", query, prefix)

    def fuzzy_(self, k_fn, tab, node, i, sofar, query, prefix=False):
        k = k_fn(i)

        if prefix and i >= len(query) + 1:
            d = tab[i - 1][len(query)]
            if d <= k:
                yield sofar, d
                yield from self.traverse(d, node, sofar)
            return

        if i >= len(tab):
            return

        for c, child in node.items():
            d = tab[i - 1][len(query)]
            if c == "\0":
                if d <= k:
                    yield sofar, d
                continue

            new = sofar + c
            tab[i][0] = i
            for j in range(1, len(tab[i])):
                sub_cost = 1 if c != query[j - 1] else 0
                sub = tab[i - 1][j - 1] + sub_cost
                insert = tab[i - 1][j] + 1
                delete = tab[i][j - 1] + 1
                tab[i][j] = min(sub, insert, delete)

            smallest = min(tab[i])
            if smallest <= k:
                yield from self.fuzzy_(k_fn, tab, child,
                                       i + 1, new, query, prefix)
