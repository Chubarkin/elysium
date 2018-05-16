from models import Model, Field


class TestModel(Model):
    __tablename__ = 'test_model'

    t1 = Field()
    t2 = Field()
    t3 = Field()
    t4 = Field()


if __name__ == '__main__':

    condition = (TestModel.t1 == TestModel.t2) & ((((TestModel.t1 <= TestModel.t2) | (TestModel.t1 > TestModel.t2)) & ((TestModel.t1 != TestModel.t2) | (TestModel.t1 >= TestModel.t2))) | TestModel.t1.contains(TestModel.t2) | TestModel.t1.is_not_null())
    print condition.to_str()
