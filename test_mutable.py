import unittest
from hypothesis import given
import hypothesis.strategies as st
from mutable import *


class TestHashmapMethods(unittest.TestCase):

    def test_init(self):
        hashmap = HashMap()
        self.assertEqual(hashmap.length, 7)

    def test_hash(self):
        hashmap = HashMap()
        hash_value = hashmap.hash(47)
        self.assertEqual(hash_value, 5)

    # 1. add
    def test_add(self):
        hashmap = HashMap()
        self.assertEqual(hashmap.hashmap_to_list(), [])
        hashmap.add(36, 240)
        self.assertEqual(hashmap.get(36), 240)


    # 2. remove
    def test_remove(self):
        hashmap = HashMap()
        dict1 = {1: 1, 3: 3, 5: 5}
        hashmap.hashmap_from_dict(dict1)
        # hashmap.add(1, 2)
        # self.assertEqual(hashmap.get(1), 2)

        hashmap.remove(1)
        dict2 = {3: 3, 5: 5}
        self.assertEqual(hashmap.hashmap_to_dict(), dict2)
        # with pytest.raises(Exception):
        #     hashmap.remove(6)

    def test_get(self):
        hashmap = HashMap()
        hashmap.add(1, 2)
        self.assertEqual(hashmap.get(1), 2)

    # 3. get_size
    def test_get_size(self):
        hashmap = HashMap()
        self.assertEqual(hashmap.get_size(), 0)
        dict = {1: 1, 2: 2, 3: 3}
        hashmap.hashmap_from_dict(dict)
        self.assertEqual(hashmap.get_size(), 3)
        hashmap.add(2, 10)
        self.assertEqual(hashmap.get_size(), 3)

    # 4. conversion
    def test_hashmap_from_dict(self):
        hashmap = HashMap()
        dict = {1: 1, 2: 2, 3: 3}
        hashmap.hashmap_from_dict(dict)
        self.assertEqual(hashmap.get_size(), 3)
        dict1 = {5: 10, 22: 4, 7: 55}
        hashmap.hashmap_from_dict(dict1)
        self.assertEqual(hashmap.get_size(), 6)

    # 4. conversion
    def test_hashmap_from_list(self):
        hashmap = HashMap()
        test_data = [1, 2, 3, 4, 5]
        hashmap.hashmap_from_list(test_data)
        self.assertEqual(hashmap.get_size(), 5)

    # 4. conversion
    def test_hashmap_to_dict(self):
        hashmap = HashMap()
        hashmap.add(1, 2)
        hashmap.add(2, 3)
        hashmap.add(4, 5)
        self.assertEqual(hashmap.hashmap_to_dict(), {1: 2, 2: 3, 4: 5})

    # 4. conversion
    def test_hashmap_to_list(self):
        hashmap = HashMap()
        dict = {1: 2, 2: 3, 3: 4, 7: 9}
        hashmap.hashmap_from_dict(dict)
        self.assertEqual(hashmap.hashmap_to_list(), [9, 2, 3, 4])

    # 5. find: return the even value list
    def test_find_even(self):
        hashmap = HashMap()
        hashmap.hashmap_from_list([75.51, 2, 60.0, 7.0])
        self.assertEqual(hashmap.find_even(), [2, 60.0])

    # 6. filter: return the values' list except even value
    def test_filter_even(self):
        hashmap = HashMap()
        hashmap.hashmap_from_list([75.51, 2, 4.0, 7.0])
        self.assertEqual(hashmap.filter_even(), [75.51, 7.0])

    # 7.map(func): test square
    def test_map(self):
        dict1 = {1: 5, 4: 10}
        hashmap = HashMap()
        hashmap.hashmap_from_dict(dict1)
        self.assertEqual(hashmap.map(lambda x: x * x), [25, 100])

    # 8.reduce:test multiplicative
    def test_reduce(self):
        hashmap = HashMap()
        self.assertEqual(hashmap.reduce(lambda a, b: a * b, 1), 1)
        dict1 = {2: 10, 4: 18}
        hashmap.hashmap_from_dict(dict1)
        self.assertEqual(hashmap.reduce(lambda a, b: a * b, 1), 180)

    # 9.iteration
    def test_iter(self):
        x = {1, 2, 3, 4}
        hashmap = HashMap()
        hashmap.hashmap_from_list(x)
        temp = {}
        for e in hashmap:
            temp[e.key] = e.value
        self.assertEqual(hashmap.hashmap_to_dict(), temp)
        i = iter(hashmap)
        self.assertEqual(next(i).value, 1)

    # Add property-based tests for from_list and to_list, all monoid properties (Associativity, Identity element)
    @given(x=st.lists(st.integers()), y=st.lists(st.integers()), z=st.lists(st.integers()))
    def test_monoid_associativity(self, x, y, z):
        hashmap = HashMap()
        hash_x = HashMap()
        hash_y = HashMap()
        hash_z = HashMap()

        hash_x.hashmap_from_list(x)
        hash_y.hashmap_from_list(y)
        hash_z.hashmap_from_list(z)

        xy = hashmap.mconcat(hash_x, hash_y)
        xy_z = hashmap.mconcat(xy, hash_z)
        yz = hashmap.mconcat(hash_y, hash_z)
        yz_x = hashmap.mconcat(hash_x, yz)

        self.assertEqual(xy_z, yz_x)

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, a):
        hash1 = HashMap()
        hash2 = HashMap()
        hash1.hashmap_from_list(a)
        # a+b = b+a
        self.assertEqual(hash1.mconcat(hash2.mempty(), hash1), hash1)
        self.assertEqual(hash1.mconcat(hash1, hash2.mempty()), hash1)

    @given(a=st.lists(st.integers()))
    def test_hashmap_from_list_to_list_equality(self, a):
        hashmap = HashMap()
        hashmap.hashmap_from_list(a)
        b = hashmap.hashmap_to_list()
        self.assertEqual(len(b), len(a))


if __name__ == '__main__':
    unittest.main()