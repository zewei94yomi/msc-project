def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    
    cls.__str__ = __str__
    return cls


@auto_str
class Foo(object):
    def __init__(self, value_1, value_2):
        self.attribute_1 = value_1
        self.attribute_2 = value_2
        
        
if __name__ == '__main__':
    test = Foo(1, 2)
    print(test)
