import sys
import codecs

from Tkinter import Tk
from tkFileDialog import askopenfilename
import ttk

def fromcin(prompt=None):
    while True:
        try: line = raw_input(prompt)
        except EOFError: break
        for w in line.split(): yield w

def printResult(x,classAry,classValueMap,class_pNameAry,classMap):
    for value1 in classAry:
        if( x == 1 ) : sys.stdout.write(classValueMap[value1]+",")
        classValueMap[value1] = ""
        for value2 in class_pNameAry[value1]:
            if( x == 1 ) : sys.stdout.write(classMap[value1][value2]+",")
            classMap[value1][value2] = ""

    if( x == 1 ) : sys.stdout.write("\n")

def printHead(x,classAry,classValueMap,class_pNameAry,classMap):
    for value1 in classAry:
        if( x == 0 ) :sys.stdout.write(value1+",")
        for value2 in class_pNameAry[value1]:
            if( x == 0 ) : sys.stdout.write(value2+",")
    if( x == 0 ) : sys.stdout.write("\n")
    printResult(x,classAry,classValueMap,class_pNameAry,classMap)


def Ignore(str):
    #if( str == "LNCEL"): return True
    #if( str == "mcc"): return True

    return False

def process(file):

    sys.stdout = open(file+".csv", 'w')

    className = ""
    classValu = ""
    distName  = ""

    classMap = {};
    classValueMap = {}

    classAry = []
    class_pNameAry = {}

    for x in range(0, 2):
        className = ""
        classValu = ""
        distName  = ""

        with codecs.open(file, encoding='utf-8', mode='r') as ins:
            for line in ins:
                pos = line.find("<managedObject");
                if( pos > 0 ):
                    pos1 = line.find("distName=\"",pos);
                    if( pos1 > 0 ):
                        pos1 += len("distName=\"")
                        pos2 = line.find("/",pos1);
                        if(pos2==-1):pos2=pos1;
                        pos2 = line.find("/",pos2+1);
                        if(pos2==-1):pos2=pos1;
                        if( distName != "" and distName != line[pos1:pos2] ):
                            className = ""
                            printResult(x,classAry,classValueMap,class_pNameAry,classMap)

                        distName = line[pos1:pos2]
                        classValu = line[pos2+1:line.find("\"",pos2)]

                    pos = line.find("class=\"",pos);
                    if( pos > 0 ):
                        pos += len("class=\"")

                        if( Ignore(line[pos:line.find("\"",pos)]) ):
                            className = line[pos:line.find("\"",pos)]
                            continue

                        if( className == line[pos:line.find("\"",pos)] ):
                            printResult(x,classAry,classValueMap,class_pNameAry,classMap)

                        className = line[pos:line.find("\"",pos)]
                        if( (className in classMap) == False ):
                            classMap[className] = {}
                            classAry.append(className)
                            class_pNameAry[className] = []
                        classValueMap[className] = classValu

                if( Ignore(className) ): continue

                pos = line.find("<p");
                if( pos > 0 ):
                    pos = line.find("name=\"",pos);
                    if( pos > 0 ):
                        pos += len("name=\"")
                        pName = line[pos:line.find("\"",pos)]
                        if( Ignore(pName) ): continue
                        if( (pName in classMap[className]) == False ) :
                            classMap[className][pName] = ""
                            class_pNameAry[className].append(pName)

                        pos += len(pName)
                        pos = line.find(">",pos);
                        if( pos > 0 ):
                            val = line[pos+1:line.find("<",pos)]
                            classMap[className][pName] = val

        printHead(x,classAry,classValueMap,class_pNameAry,classMap)


if( len(sys.argv) > 1 ):
    process(sys.argv[1])
else:
    Tk().withdraw()
    filename = askopenfilename()
    process(filename)
