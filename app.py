from models import Model, IntegerField


class TestModel(Model):
    __tablename__ = 'test_model'

    t1 = IntegerField()
    t2 = IntegerField()
    t3 = IntegerField()
    t4 = IntegerField()


class NewTestModel(Model):
    __tablename__ = 'new_test_model'
    t1 = IntegerField()


if __name__ == '__main__':

    condition = (NewTestModel.t1 == TestModel.t2) & ((((TestModel.t1 <= TestModel.t2) | (TestModel.t1 > TestModel.t2)) & ((TestModel.t1 != TestModel.t2) | (TestModel.t1 >= TestModel.t2))) | TestModel.t1.contains(TestModel.t2) | TestModel.t1.is_not_null())
    print condition.to_str()

    condition = (NewTestModel.t1 >= 0) | (NewTestModel.t1 == 1)
    print condition.to_str()

    print TestModel.filter(TestModel.t1 != TestModel.t2).left_join(NewTestModel, on=NewTestModel.t1.is_not_null()).join(NewTestModel, on=NewTestModel.t1.is_null()).order_by(TestModel.t1).order_by(TestModel.t1).sql()
    print TestModel._fields
    tm = TestModel(t1=2, t3=4)
    tm2 = TestModel(t1=3)
    print tm.t1
    print tm2.t1
    print tm.__dict__
    print TestModel.t1
    print tm.t2
    print tm.save().sql()

