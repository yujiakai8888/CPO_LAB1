import unittest
from hypothesis import given
import hypothesis.strategies as st
from immutable import HashMap


class TestMutableHashMap(unittest.TestCase):
    def setUp(self):
        self.hashMap = HashMap()


class TestMutableHashMapMethods(TestMutableHashMap):
    def test_init(self):
        self.assertEqual(self.hashMap.len, 5)
        self.assertIsInstance(self.hashMap.data, list)
        self.assertEqual(self.hashMap.data[0], [])
        self.assertEqual(self.hashMap.data[1], [])
        self.assertEqual(self.hashMap.data[2], [])
        self.assertEqual(self.hashMap.data[3], [])
        self.assertEqual(self.hashMap.data[4], [])

    # 1. add
    def test_add(self):
        new = HashMap()
        for i in range(5):
            new = new.add(i)
        self.assertEqual(new.data[0], [0])
        self.assertEqual(new.data[1], [1])
        self.assertEqual(new.data[2], [2])
        self.assertEqual(new.data[3], [3])
        self.assertEqual(new.data[4], [4])

    # 2. remove
    def test_remove(self):
        new = HashMap()
        new = new.add(0)
        self.assertEqual(new.data[0], [0])
        new = new.remove(0)
        self.assertEqual(new.data[0], [])

    # 3. size
    def test_size(self):
        self.assertEqual(self.hashMap.size(), 5)

    # 4. key_number
    def test_key_num(self):
        self.assertEqual(self.hashMap.key_number(), 0)

    # 5. is_member
    def test_is_member(self):
        new = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        new = new.from_list(list_a)
        self.assertEqual(new.is_member(11), True)
        self.assertEqual(new.is_member(9), False)

    # 6. conversion
    def test_from_list(self):
        list_a = [0, 1, 2, 3, 4, 11]
        self.hashMap.from_list(list_a)
        self.assertEqual(self.hashMap.data[0], [0])
        self.assertEqual(self.hashMap.data[1], [1, 11])
        self.assertEqual(self.hashMap.data[2], [2])
        self.assertEqual(self.hashMap.data[3], [3])
        self.assertEqual(self.hashMap.data[4], [4])

    # 7. filter
    def test_filter(self):
        new = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        new.from_list(list_a)

        def filterOdd(value):
            if value % 2 == 0:
                return True
            else:
                return False

        res = new.filter(filterOdd)
        self.assertEqual(res, [0, 2, 4])

    # 8.map(func)
    def test_map(self):
        new = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        new.from_list(list_a)

        def mapPlusOne(value):
            return value + 1

        res = new.map(mapPlusOne)
        self.assertEqual(res, [1, 2, 12, 3, 4, 5])

    # 9.reduce
    def test_reduce(self):
        new = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        new.from_list(list_a)

        def reduceSum(accumulator, curr):
            return accumulator + curr

        res = new.reduce(reduceSum, 0)
        self.assertEqual(res, 21)

    # The property - based tests

    @given(st.lists(st.integers(5)))
    def test_from_list_to_list_equality(self, a):
        hash1 = HashMap()
        hash1 = hash1.from_list(a)
        b = hash1.to_list()
        a = set(a)
        b = set(b)
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        a = list(set(a))
        hash1 = HashMap()
        hash1 = hash1.from_list(a)
        self.assertEqual(hash1.key_number(), len(a))

    # 10.monoid_add
    def test_monoid_add(self):
        hash1 = HashMap()
        hash2 = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        list_b = [5, 6, 7]
        hash1 = hash1.from_list(list_a)
        hash2 = hash2.from_list(list_b)
        tmp1 = hash1
        tmp2 = hash2
        # list1 = hash1 add hash2
        list1 = tmp1.monoid_add(hash2).to_list()
        # list2 = hash2 add hash1
        list2 = tmp2.monoid_add(hash1).to_list()
        self.assertEqual(list1, list2)

    # 11.iteration and __next__
    def test_iter(self):
        x = [1, 2, 3]
        hash1 = HashMap()
        hash1 = hash1.from_list(x)
        tmp = []
        for e in hash1:
            tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(hash1.to_list(), tmp)
        i = iter(HashMap())
        self.assertRaises(StopIteration, lambda: next(i))


if __name__ == "__main__":
    unittest.main()
