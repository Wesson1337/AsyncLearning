class Test:
    def __init__(self, test):
        self._test = test

    @property
    def test(self):
        return self._test

    @test.setter
    def test(self, value):
        print("i'm test setter")
        self._test = value


x = Test('kek')
x.test = 'hyu'
print(x.test)
