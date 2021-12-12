def call(function, *args):
    if function is not None:
        function(*args)
        
def example(test):
    print(test)
    
def example_none():
    print("example_none")
    
def example_many(t1, t2):
    print(f'{t1} {t2}')
    
call(example, "test")
call(example_none)
call(example_many, "test1", "test2")