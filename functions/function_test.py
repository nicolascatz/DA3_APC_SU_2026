def mean(X):
   
    return sum(X) / len(X)

def median(X):
    
    sorted_X = sorted(X)
    n = len(sorted_X)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_X[mid - 1] + sorted_X[mid]) / 2
    else:
        return sorted_X[mid]