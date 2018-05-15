class Test(object):
    def __eq__(self, other):
        print '1'
        print self
        return True

    def __and__(self, other):
        print '2'
        print self
        return True

    def __or__(self, other):
        print '3'
        print self
        return True


if __name__ == '__main__':
    t1 = Test()
    t2 = Test()
    t3 = Test()
    t4 = Test()

    t1 == t2 | t3 == t4 & t3 == t1
    print
