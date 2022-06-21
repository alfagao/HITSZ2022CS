import numpy as np

def tst1():
    a = [1, 2, 3]
    print(2*a)
    a = np.array(a)
    print(2*a)

def tst2():
    a = [1, 2, 3, 4, 5, 6, 7, 8]
    print(a[3:])
    print(a[:-3])


if __name__ == '__main__':
    tst2()
