class Node(object):
    def __init__(self, key=None, value=None, next=None):
        self.key = key
        self.value = value
        self.next = next


class HashMap(object):
    init = object()

    def __init__(self, dict=None, length=7):
        if dict is not None:
            self.hashmap_from_dict(self, dict)

        self.keyList = []
        self.data = [self.init for i in range(length)]
        self.length = length
        self.index = 0

    def hash(self, key):
        hash_value = key % self.length  # mod
        return hash_value

    # 1. add
    def add(self, key, value):
        hash_value = self.hash(key)
        addNode = Node(key, value)

        if self.data[hash_value] == self.init:
            self.data[hash_value] = addNode
            self.keyList.append(key)
        else:
            head = self.data[hash_value]
            # loop to find the empty Node
            while head.next != None:
                # key == ?
                if head.key == key:
                    head.value = value
                    return
                head = head.next
            # Judge whether it already exists
            if head.key == key:
                head.value = value
                return
            # Now find the empty Node
            head.next = addNode
            self.keyList.append(key)
        return

    # 2. remove
    def remove(self, key):
        hash_value = self.hash(key)
        if self.data[hash_value] is self.init:
            return False
        elif self.data[hash_value].key is key:
            self.data[hash_value] = self.data[hash_value].next
            self.keyList.remove(key)
            return True
        p = self.data[hash_value]
        q = self.data[hash_value].next
        while q.next is not None:
            if q.key == key:
                p.next = q.next
                self.keyList.remove(key)
                return True
            p = q
            q = q.next
        if q.key == key:
            p.next = None
            self.keyList.remove(key)
            return True
        # # all the elements have been checked
        # raise Exception("WE DONT HAVE THIS key")
        # return


    # get value
    def get(self, key):
        dict = self.hashmap_to_dict()
        value = dict[key]
        return value

    # 3. size
    def get_size(self):
        size = len(self.keyList)
        return size

    # 4. conversion
    def hashmap_from_dict(self, dict):
        for key, value in dict.items():
            self.add(key, value)


    def hashmap_from_list(self, list):
        for key, value in enumerate(list):
            self.add(key, value)

    def hashmap_to_dict(self):
        Dict = {}
        # whether the hashmap is empty
        if len(self.keyList) == 0:
            return Dict
        # convert one by one set
        for i in range(self.length):
            if self.data[i] != self.init:
                head = self.data[i]
                while head != None:
                    Dict[head.key] = head.value
                    head = head.next
        return Dict

    # hashmap_to_list may lose the key info
    def hashmap_to_list(self):

        dict = self.hashmap_to_dict()
        list = []
        for key, value in dict.items():
            list.append(value)
        return list

    # 5.find: return the even value list
    def find_even(self):
        dict = self.hashmap_to_dict()
        findlist = []
        for key, value in dict.items():
            if value % 2 == 0:
                findlist.append(value)
        return findlist

    # 6. filter: return the values' list except even value
    def filter_even(self):
        list = self.hashmap_to_list()
        filterlist = []
        for value in list:
            if value % 2 != 0:
                filterlist.append(value)
        return filterlist

    # 7.map(func)
    def map(self, func):

        list = self.hashmap_to_list()
        listOut = []
        for value in list:
            value = func(value)
            listOut.append(value)
        return listOut

    # 8.reduce
    def reduce(self, func, init_state):
        a = init_state
        for key in self.keyList:
            value = self.get(key)
            a = func(a, value)
        return a

    # mempty and mconcat
    def mempty(self):
        return None

    def mconcat(self, a, b):
        # judge input
        if a is None:
            return b
        if b is None:
            return a
        for key in b.keyList:
            value = b.get(key)
            a.add(key, value)
        return a

    # 9.iteration
    def __iter__(self):
        iter_list = []
        for key in self.keyList:
            iter_list.append(Node(key, self.get(key)))
        return iter(iter_list)