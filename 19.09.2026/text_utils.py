def load_data():
    return [3, 17, 8, 25, 6, 12, 25, 9, 14]
def filter_above(values, threshold=10):
    z=[]
    for i in values:
        if i >threshold:
            z.append(i)
    return(z)
def mean(values):
    return sum(values)/len(values)