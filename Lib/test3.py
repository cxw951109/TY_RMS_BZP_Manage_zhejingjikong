arr = [1, 23,3 ,434,54,545,65,54,54,45,23,54,23]
arr_1 = set(arr)
from collections import Counter
def counter(arr):
    return Counter(arr).most_common(len(arr_1)) if Counter(arr).most_common(len(arr_1)) else None


for x in counter(arr):
    print('{}出现的次数为{}'.format(x[0], x[1]))
