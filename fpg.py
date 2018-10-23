class treeNode:
    def __init__(self,nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.children = {}   
        self.nodeLink = None 
    
    def inc(self, numOccur):
        self.count += numOccur
     
    def disp(self, ind = 1):
        print "  " * ind, self.name, "  ",self.count
        for child in self.children.values():
            child.disp(ind + 1)

def datatrans():
    f = open('data.ntrans_0.1.tlen_5.nitems_0.01', 'r')

    input=f.read()
    list=input.split()
    #print(list)

    data=[list[i:i+3] for i in range(0,len(list),3)] #list fragment
    #print(data)

    data2=[]
    for i in range(0,len(list)/3):
        j=3*i+2
        data2.append(list[j])
    #print(data2)

    data3=[]
    data4=[]
    for i in range(1,len(list)/3):
       data3.append(data2[i-1])
       if(int(list[i*3])-int(list[(i-1)*3])==1):
         data4.append(data3)
         data3=[]
    data3.append(data2[i])
    data4.append(data3)
    #print(data4)
    return data4
    
def createTree(dataSet, minSup=1):  #creat fp-tree
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in headerTable.keys():    #remove item < minSup
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:   #if [] return none
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None)     #Tree root
    for tranSet, count in dataSet.items(): 
        localD = {} 
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0] 
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)] #sort
            updateTree(orderedItems, retTree, headerTable, count) 
    return retTree, headerTable

def updateTree(items, inTree, headerTable,count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)   #if item exists count++
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree) #if item doesnt exist
        if headerTable[items[0]][1]==None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)    
          
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode   

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0)+1
    return retDict

def findPrefixPath(basePat,treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []     
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)    
        
def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),key = lambda p:p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myConTree,myHead = createTree(condPattBases, minSup)
        
        if myHead != None:
            print 'conditional tree for :', newFreqSet
            myConTree.disp()
            
            mineTree(myConTree, myHead, minSup, newFreqSet, freqItemList)

def fpGrowth(dataSet, minSup=input("Input minSup:")): #minSupset
    initSet = createInitSet(dataSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems

if __name__=="__main__":
    dataSet = datatrans()
    freqItems = fpGrowth(dataSet)
    print freqItems
