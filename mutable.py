class HashMap(object):

    def __init__(self, size=5):
        self.__curr__ = 0
        self.len = size
        self.data = []
        self.keynumber = 0
        for i in range(size):
            self.data.append([])

    # 1. add
    def add(self, key):
        if self.is_member(key):
            return self
        index = key % self.len
        self.data[index].append(key)
        self.keynumber += 1
        return self

    # 2. remove
    def remove(self, key):
        index = key % self.len
        self.keynumber -= 1
        for value in self.data[index]:
            if value == key:
                self.data[index].remove(value)
        return self

    # 3. size
    def size(self):
        return self.len

    # 4. key_number
    def key_number(self):
        return self.keynumber

    # 5. is_member
    def is_member(self, key):
        for layer1 in self.data:
            for layer2 in layer1:
                if key == layer2:
                    return True
        return False

    # 6. conversion
    def from_list(self, list_A):
        for i in list_A:
            self.add(i)
        return self

    def to_list(self):
        list_A = []
        for i in range(self.len):
            for v in self.data[i]:
                list_A.append(v)
        return list(set(list_A))

    # 7. filter: return a list
    def filter(self, func):
        res = []
        for i in range(self.len):
            for v in self.data[i]:
                if func(v):
                    res.append(v)
        return res

    # 8.map(func): return a list
    def map(self, func):
        res = []
        for i in range(self.len):
            for v in self.data[i]:
                res.append(func(v))
        return res

    # 9.reduce: return accumulator
    def reduce(self, func, initial):
        accumulator = initial
        for i in range(self.len):
            for v in self.data[i]:
                accumulator = func(accumulator, v)
        return accumulator

    # 10.monoid_add
    def monoid_add(self, another_hash):
        if another_hash.keynumber == 0:
            return self

        for i in range(another_hash.len):
            for v in another_hash.data[i]:
                if not self.is_member(v):
                    self.add(v)
        self.keynumber += another_hash.keynumber
        return self

    # 11.iteration and __next__
    def __iter__(self):
        return self

    def __next__(self):
        if self.keynumber > 0:
            if self.__curr__ < self.keynumber:
                cur = self.__curr__
                for i in range(self.len):
                    if cur >= len(self.data[i]):
                        cur -= len(self.data[i])
                        continue
                    else:
                        tmp = self.data[i][cur]
                        self.__curr__ += 1
                        return tmp
            else:
                self.__curr__ = 0
                raise StopIteration
        else:
            raise StopIteration
