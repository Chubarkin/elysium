from query.condition import ConditionMixin


class Test(ConditionMixin):
    def __init__(self, name):
        self._name = name

    def to_str(self):
        return self._name


if __name__ == '__main__':
    t1 = Test('test.t1')
    t2 = Test('test.t2')
    t3 = Test('test.t3')
    t4 = Test('test.t4')

    condition = (t1 == t2) & ((((t1 <= t2) | (t1 > t2)) & ((t1 != t2) | (t1 >= t2))) | t1.contains(t2) | t1.is_not_null())
    print condition.to_str()
