# -*- coding: utf-8 -*-
import select
import sys
import os
import random
import threading
import time

timelimits = {'beginner': 30, 'easy': 15, 'normal':10, 'fast':5, 'ultra': 3}
numberofquestions = {'short': 10, 'normal': 15, 'long': 25}
hLevels = [
# Level Type (Add,Sub,Mult,Divide), Number range
{ 'Addition': range(10) }, 
{ 'Subtraction': range(11) },
{ 'Addition': range(1,26) }, 
{ 'Subtraction': range(-10,11) },
{ 'Addition': range(-25,26), 'Subtraction': range(-15,16) },
{ 'Multiplication': range(10) },
{ 'Multiplication': range(2,15),'Addition': range(-25,26), 'Subtraction': range(-15,16) },
{ 'Division': range(11) },
]

random.seed(time.time())

class Problem(object):
    """ Base class for all Problem Creation Classes """
    def __init__(self,dataSet): 
        self.problems = []
        self.lDataSet = len(dataSet)
        self.dataSet = dataSet
    def CreateProblem(self):
        print "Feature not implemented <%s>" % self
    def StoreProblem(self,values,equation,result=None,time=None):
        self.problems.append([values,equation,result,time])
    def UpdateProblemResults(self,result,completedtime):
        (values,equation,oldresult,oldtime) = self.problems.pop()
        self.StoreProblem(values,equation,result,time)

class Addition(Problem):
    def __init__(self,dataSet): 
        super(Addition,self).__init__(dataSet)
    def CreateProblem(self):
        "Returns equation for addition"
        i1, i2 = [ getrandom(self.lDataSet) for j in range(2) ]
        n1, n2 = [ self.dataSet[i] for i in (i1,i2) ]
        ans = n1 + n2
        self.StoreProblem( [n1,n2,ans],"%d + %d = %d" % (n1,n2,ans))
        return "%d + %d" % (n1,n2), ans

def swap(n1,n2):
    tmp = n2
    n2 = n1
    n1 = tmp
    return n1,n2

class Subtraction(Problem):
    def __init__(self,dataSet): 
        super(Subtraction,self).__init__(dataSet)
    def CreateProblem(self):
        "Returns equation for subtraction"
        i1, i2 = [ getrandom(self.lDataSet) for j in range(2) ]
        ans, n2 = [ self.dataSet[i] for i in (i1,i2) ]
        if ans > n2: n1,n2 = swap(ans,n2)
        n1 = ans + n2
        self.StoreProblem( [n1,n2,ans],"%d - %d = %d" % (n1,n2,ans))
        return "%d - %d" % (n1,n2), ans

class Multiplication(Problem):
    def __init__(self,dataSet):
        super(Multiplication,self).__init__(dataSet)
    def CreateProblem(self):
        "Returns equation for multiplication"
        i1, i2 = [ getrandom(self.lDataSet) for j in range(2) ]
        n1, n2 = [ self.dataSet[i] for i in (i1,i2) ]
        ans = n1 * n2
        self.StoreProblem( [n1,n2,ans],"%d * %d = %d" % (n1,n2,ans))
        return "%d * %d" % (n1,n2), ans

class Division(Problem):
    def __init__(self,dataSet):
        super(Division,self).__init__(dataSet)
    def CreateProblem(self):
        "Returns equation for division"
        i1, i2 = [ getrandom(self.lDataSet) for j in range(2) ]
        ans, n2 = [ self.dataSet[i] for i in (i1,i2) ]
        if ans > n2: n1,n2 = swap(ans,n2)
        n1 = ans * n2
        if ans > n2: n1,n2 = swap(n1,n2)
        self.StoreProblem( [n1,n2,ans],"%d / %d = %d" % (n1,n2,ans))
        return "%d / %d" % (n1,n2), ans

hSetup = { 
    'Addition': Addition, 
    'Subtraction': Subtraction,
    'Multiplication': Multiplication,
    'Division': Division,
}

answerstrings = ["Correct!!","Perfect!!","Yes!!","Great Job!!"]
lanswerstrings = len(answerstrings)

def getrandom(value): return random.randint(0,value-1)

# choose a level
def ChooseLevel( level = None ):
    global hLevels
    numLevels = len(hLevels)
    if level == None: level = getrandom(numLevels)
    if level < 0 or level >= numLevels: level = (level+numLevels*abs(level/numLevels))%numLevels
    return (level, hLevels[level])

def sortkeys( mydict ):
    keys = mydict.keys()
    keys.sort()
    return keys

def CreateLevelData(problemCount,level,data):
    def CreateObject(data):
        """ Create Objects necessary for building problems """
        global hSetup
        levelObject = {}
        for key in sortkeys(data):
            numberRange = data[key]
            levelObject[key] = hSetup[key]( numberRange )
        return levelObject
    def CreateData(levelObject):
        """ Set references to problem objects for use during level """
        keysValues = levelObject.items()
        lkeysValues = len(keysValues)
        levelData = []
        for i in range(problemCount):
            choice = getrandom(lkeysValues)
            oProblem = keysValues[choice][1]
            levelData.append( oProblem )
        return levelData
    levelObject = CreateObject(data)
    return CreateData(levelObject)

def UnitTests():
    # range testing
    results = []
    print "Starting range testing",
    try: 
        results = map( lambda a: ChooseLevel(a), [None] + range(-len(hLevels),2*len(hLevels)) )
        print "Passed"
    except:
        print "Failed"
    # testing creation of all programs
    print "Starting test of level creation"
    try:
        for (level,data) in results:
            print "Test %s - %s" % (level,data),
            try:
                levelData = CreateLevelData(level,data)
                print "Passed"
                print levelData
            except:
                print "Failed"
        print "Passed"
    except:
        print "Failed"

def usage(prgname):
    print "usage: %s level-number [number-of-questions] [time-limit]" % prgname
    print "\tlevel-number: integer representing the level of choice"
    print "\tnumber-of-questions: %s" % ','.join( [ i for i in numberofquestions.keys() ] )
    print "\ttime-limit: %s" % ','.join( [ i for i in timelimits.keys() ] )
    count = 1
    for item in hLevels:
        print "\tLevel %s. " % count, ','.join( [ "%s numbers %d-%d" % (k,v[0],v[-1]) for k,v in item.items() ] )
        count += 1
    sys.exit(1)

if __name__ == "__main__":
    (results, count, correctanswers) = ([],1,0)
    timelimit = 5 
    cProblems = 25

    # choose level, 
    if len(sys.argv) < 2:
       usage(sys.argv[0])

    try:
        cLevel = int(sys.argv[1])-1
        if len(sys.argv) > 2: cProblems = numberofquestions[sys.argv[2].lower()]
        if len(sys.argv) > 3: timelimit = timelimits[sys.argv[3].lower()]
    except:
        usage(sys.argv[0]) 

    # print "---- Start unit test ----"
    # UnitTests()
    # print "---- End unit test ----"

    # pick level to test
    (level,data) = ChooseLevel(cLevel)
    # print level, data
    levelData = CreateLevelData(cProblems,level,data)
    # print levelData
    print "You have %s questions, answer each question in less than %s seconds" % (cProblems,timelimit)
    print "Get ready ...",
    sys.stdout.flush()
    time.sleep(1)
    print "Set ...",
    sys.stdout.flush()
    time.sleep(1)
    print "Go!"
    problemstart = time.time()
    for problem in levelData:
        (equation,answer) = problem.CreateProblem()
        print "%d. %s ? " % (count,equation),
        sys.stdout.flush()
        starttime = time.time()
        rfd = select.select([sys.stdin],[],[],timelimit)[0]
        delta = time.time() - starttime
        inputAnswer = "A little faster next time! %d" % answer
        for fd in rfd:
            # get answer from input
            d = os.read(fd.fileno(), 16384)
            try:
                userAnswer = int(d)
                problem.UpdateProblemResults(userAnswer,delta)
                if answer == int(userAnswer): 
                    inputAnswer = answerstrings[getrandom(lanswerstrings)]
                    correctanswers+=1
                else: 
                    inputAnswer = "Close!  It's actually %d" % answer
            except ValueError:
                inputAnswer = "Oops!  I didn't recognize that number"
                incorrectanswers+=1
        print inputAnswer
        count+=1
    problemdelta = time.time() - problemstart
    print ""
    print "Great job!  You answered %s out of %s questions correctly." % (correctanswers,cProblems)
    print "That's %.1f %% correct.  It took you %.0f seconds to answer all the questions." % (100*correctanswers/cProblems,problemdelta)
    if 100*correctanswers/(cProblems+1.0) > 80 and (cProblems*timelimit+1.0)/problemdelta > 1:
        print "You should think about trying the next level, or the same level at a quicker pace"
    print ""