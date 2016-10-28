'''
Created on Oct 24, 2016

I'm trying to implement a decision tree,
since it is an easy but useful classification tool, understanding its basic algorithm is helpful
CART - chooses the best variable to divide up the data in each step
In order to choose the best variable each step, the divided 2 sets should have least mixed situations
To measure how mixed a set is, we use Gini Impurity or Entropy
'''
from math import log

class decision_node:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col                       # column index of the criteria to be tested
        self.value = value                   # the value that the column needs to match to get the TRUE result
        self.results = results               # results for the branch, it will be None except for end nodes
        self.fb = fb                         # child node if it's FALSE
        self.tb = tb                         # child node if it's TRUE


def divide_data(rows, col, value):
    split_function = None
    
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[col] >= value    # Python lambda is a type of function
    else:
        split_function = lambda row: row[col] == value
        
    st1 = [row for row in rows if split_function(row)]
    st2 = [row for row in rows if not split_function(row)]
    
    return st1, st2


# for each set of data, count distinct labels, to help find the best variable
def count_label(rows):
    labels = {}
    for r in rows:
        l = r[-1]
        labels.setdefault(l, 0)
        labels[l] += 1
    return labels


# Variable Choose Measure 1 - Gini Impurity, the probability of putting an item to the wrong set. 
## 0 means the same, higher more mixed
def gini_impurity(rows):
    lbs = count_label(rows)
    total_items = len(rows)
    gi = 0
    for l1, ct1 in lbs.items():
        p1 = float(ct1)/total_items
        for l2, ct2 in lbs.items():
            if l1 == l2: continue
            p2 = float(ct2)/total_items
            gi += p1*p2
            
    return gi
        

# Variable Choose Measure 2 - Entropy, calculate how mixed the set is/how different the outcomes are different from each other
## 0 means the same, higher more mixed
def entropy(rows):
    log2 = lambda x: log(x)/log(2)
    lbs = count_label(rows)
    total_items = len(rows)
    ep = 0.0
    
    for ct in lbs.values():
        p = float(ct)/total_items
        ep -= p*log2(p)
        
    return ep



def main():
    # The last column in each row is the label - what needs to be predicted
    # I'm building a decision tree to tell how to make tasty 8 treasure porridge :)
    ## columns meaning (left to right):
    ## using honey or sugar, temperature, iron pot or pottery pot, 
    ## has black bean nor not, hours for cooking, number of dates, cups of sweet rice, tasty or not
    test_data = [
                 ['honey', 200, 'iron', 'has black bean', 3, 7, 0.5, 'no'],
                 ['sugar', 250, 'pottery', 'has black bean', 5, 7, 0.5, 'no'],
                 ['honey', 300, 'pottery', 'has black bean', 5, 5, 0.5, 'yes'],
                 ['honey', 150, 'pottery', 'has black bean', 5, 5, 0.5, 'no'],
                 ['honey', 300, 'pottery', 'has black bean', 3, 5, 1, 'no'],
                 ['honey', 300, 'pottery', 'no black bean', 3, 7, 0.5, 'yes'],
                 ['sugar', 250, 'iron', 'no nlack bean', 4, 7, 0.5, 'yes'],
                 ['sugar', 300, 'iron', 'no black bean', 5, 7, 1, 'no'],
                 ['sugar', 300, 'pottery', 'no black bean', 5, 5, 1, 'no']
                 ]
    
    print "Gini Impurity: ", gini_impurity(test_data)
    print "Entropy: ", entropy(test_data)
    
    st1, st2 = divide_data(test_data, 0, 'honey')
    print "Entropy for set1: ", entropy(st1)
    print "Entropy for set2: ", entropy(st2)
    
if __name__ == "__main__":
    main()
        
        
    
# TO BE CONTINUED...
