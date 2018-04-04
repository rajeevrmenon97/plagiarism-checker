from __future__ import print_function
from errors import NoValidArgumentError, OutOfRangeError
from plagResult import plagResult

def run(s1, s2, mML=3, treshold=0.5):
    if mML<1:
        raise OutOfRangeError
    if not (0 <= treshold <= 1):
        raise OutOfRangeError
    if s1 == None or s2 == None:
        raise NoValidArgumentError
    if s1 == '' or s2 == '':

        return plagResult(hash(s1), hash(s2))

    global tiles, matchList
    tiles = []
    matchList = []
    tiles = RKR_GST(s1, s2, mML)

    simResult = calcSimilarity(s1.split(), s2.split(), tiles, treshold)
    similarity = simResult[0]

    if similarity>1: similarity = 1

    result = plagResult()
    result.setIdentifier(hash(s1), hash(s2))
    result.setTiles(tiles)
    result.setSimilarity(similarity)
    result.setSuspectedPlagiarism(simResult[1])

    return result

def RKR_GST(P, T, minimalMatchingLength = 3, initsearchSize = 20):

    PList = P.split()
    TList = T.split()

    s = initsearchSize
    stop = False
    while not stop:
        Lmax = scanpattern(s, PList, TList)
        if Lmax > 2*s:
            s = Lmax
        else:
            markstrings(s, PList, TList)
            if s > 2*minimalMatchingLength:
                s = s / 2
            elif s > minimalMatchingLength:
                s = minimalMatchingLength
            else:
                stop = True
    return list(tiles)

def scanpattern(s, P, T):
    longestMaxMatch = 0
    queue = []
    hashtable = GSTHashtable()
    t = 0
    noNextTile = False

    while t<len(T):
        if isMarked(T[t]):
            t = t+1
            continue

        dist = distToNextTile(t, T)
        if dist == None:
            dist = len(T)-t
            noNextTile = True

        if dist < s:
            if noNextTile: t = len(T)
            else:
                t = jumpToNextUnmarkedTokenAfterTile(t, T)
                if t == None: t = len(T)
        else:

            substring = "".join(T[t:t+s])
            h = createKRHashValue(substring)
            hashtable.add(h, t)
            t = t+1

    noNextTile = False
    p = 0
    while p<len(P):
        if isMarked(P[p]):
            p = p+1
            continue

        dist = distToNextTile(p, P)
        if dist == None:
            dist = len(P)-p
            noNextTile = True

        if dist < s:
            if noNextTile: p = len(P)
            else:
                p = jumpToNextUnmarkedTokenAfterTile(p, P) #TODO:
                if p == None: p = len(P)
        else:
            substring = "".join(P[p:p+s])
            h = createKRHashValue(substring)
            values = hashtable.get(h)
            if values != None:
                for val in values:
                    if "".join(T[val:val+s]) == substring:
                        t = val
                        k = s
                        while (p+k<len(P) and t+k<len(T) and
                               P[p+k] == T[t+k]
                               and isUnmarked(P[p+k]) and isUnmarked(T[t+k])):
                            k = k+1
                        if k > 2*s: return k
                        else:
                            if longestMaxMatch < s: longestMaxMatch = s
                            queue.append((p, t, k))
            p = p+1
    if queue != []:
        matchList.append(queue)
    return longestMaxMatch

def markstrings(s, P, T):
    lengthOfTokenTiled = 0
    while matchList != []:
        queue = matchList.pop(0)
        while queue != []:
            match = queue.pop(0)
            if not isOccluded(match, tiles):
                for j in range(0, match[2]):
                    P[match[0]+j] = markToken(P[match[0]+j])
                    T[match[1]+j] = markToken(T[match[1]+j])
                lengthOfTokenTiled = lengthOfTokenTiled+match[2]
                tiles.append(match)


def createKRHashValue(substring):
    hashValue = 0
    for c in substring:
        hashValue = ((hashValue<<1) + ord(c))
    return hashValue

def isUnmarked(s):
    if len(s) > 0: return s[0] != '*'
    else: return False

def isMarked(s):
    return not isUnmarked(s)

def markToken(s):
    return '*'+s

def isOccluded(match, tiles):
    for m in tiles:
        if (m[0]+m[2] == match[0]+match[2]
            and m[1]+m[2] == match[1]+match[2]):
            return True
    return False

def distToNextTile(pos, stringList):
    if pos == len(stringList): return None

    dist = 0
    while pos+dist+1<len(stringList) and isUnmarked(stringList[pos+dist+1]):
        dist = dist+1

    if pos+dist+1 == len(stringList): return None

    return dist+1

def jumpToNextUnmarkedTokenAfterTile(pos, stringList):
    dist = distToNextTile(pos, stringList)
    if dist == None: return None

    pos = pos+dist
    while pos+1<len(stringList) and not isUnmarked(stringList[pos+1]):
        pos = pos+1

    if pos+1> len(stringList)-1: return None

    return pos+1

def calcSimilarity(s1List, s2List, tiles, treshold):
    similarity = sim(s1List, s2List, tiles)
    suspPlag = similarity >= treshold
    return [similarity, suspPlag]

def sim(A, B, tiles):
    return float(2 * coverage(tiles)) / float(len(A) + len(B))

def coverage(tiles):
    accu = 0
    for tile in tiles:
        accu = accu + tile[2]
    return accu

class GSTHashtable:

    def __init__(self):
        self.dict = {}

    def add(self, key, ob):
        if self.dict.has_key(key):
            values = self.dict.get(key)
            values.append(ob)
            self.dict.setdefault(key, values)
        else:
            self.dict.setdefault(key, [ob])

    def get(self, key):
        if self.dict.has_key(key):
            return self.dict.get(key)
        else:
            return None

    def clear(self):
        self.dict = {}

def plagiarismCheck(text1,text2,index_list):
    resultvalue=run(text1,text2)
    print ('tile content is ',resultvalue.getTiles())
    print (resultvalue.similarity)
    print ('tile similarity content copy authentication ')

    tmp1=text1.split()

    for j in resultvalue.getTiles():
        print ('THIS IS FOR ' , j)
        lenh=j[2]

        for i in range(len(index_list)):
            if j[1]<index_list[i][0]:
                 print ('FROM FILE ',index_list[i][1])
                 break
        for k in range(j[0],j[0]+j[2]):

            print (tmp1[k],end=' ')
        print('\n')
