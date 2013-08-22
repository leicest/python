import json
import nltk
import operator as op
import numpy as np
from sys import stdin
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV

class ML:
    """Toolkit for simplifying machine learning tasks"""
    
    X = y = X_ = y_ = y_pred = []
    clf = RandomForestRegressor(n_estimators=5, max_depth=3, random_state=0)
    
    def __init__(self, clf=None):
        self.clf = clf or self.clf
        
    def split(self, size=.2):
        """Generate test data from training data"""
        self.X, self.X_, self.y, self.y_ = train_test_split(self.X, self.y, test_size=size)
        return self
    
    def params(self, train_data, X_=[], y_=[], split=True, size=.2):
        """Set the data for the model and generate test data if required"""
        self.X, self.y = train_data
        self.X, self.y = np.array(self.X), np.array(self.y)
        self.X_, self.y_ = np.array(X_), np.array(y_)
        if not self.y_.size and split:
            self.split(size)
        return self
        
    def p(self, x):
        """Predict the target for some data given"""
        return self.clf.predict(x)[0]

    def run(self, override=None):
        """Train the classifier and run it on test values if given"""
        self.clf.fit(self.X, self.y)
        if self.X_.any():
            self.y_pred = self.clf.predict(self.X_)
        if self.y_.any():
            print score(self.y_, self.y_pred)

    def optimize(self, params, override=None, cv=3):
        """Find optimal parameters for the model using GridSearch"""
        self.clf = override or self.clf
        grid = GridSearchCV(self.clf, params, score_func=score)
        grid.fit(self.X, self.y, cv=cv)
        print grid.best_params_, grid.best_score_


def score(y_true, y_pred):
    """Calculate the score of predicted values againt ground truth"""
    # print zip(y_true, y_pred)
    from sklearn.metrics import precision_score
    return precision_score(y_true, y_pred)

def read(f):
    """Return the training and target data"""
    N, M = map(int, f.readline().split())
    X, y = [], []
    for _ in range(N):
        line = f.readline().split()
        y.append(int(line[1]))
        X.append(map(lambda x: float(x.split(':')[1]), line[2:]))
    X, y = np.array(X), np.array(y)
    T = int(f.readline())
    ans, X_ = [], []
    for _ in range(T):
        line = f.readline().split()
        ans.append(line[0])
        X_.append(map(lambda x: float(x.split(':')[1]), line[1:]))
    X_ = np.array(X_)
    return X, y, X_, ans

if __name__ == '__main__':

    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=10, max_depth= 7, random_state=0)
    params = { 'n_estimators': range(8,16), 'max_depth':range(1,11) }
    
    from sklearn import tree
    clf = tree.DecisionTreeClassifier(random_state=0)
    params = { 'max_depth':range(1,11) }
                
    X, y, X_, ans = read(stdin)
    m = ML(clf).params((X, y), X_=X_ , split=False)

    m.optimize(params)
    # m.run(clf)
    for i in zip(ans, m.y_pred):
        print '%s %+d' % i
    