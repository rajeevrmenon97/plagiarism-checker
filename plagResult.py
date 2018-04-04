from errors import NoValidArgumentError, OutOfRangeError, NoIdentifierSetError

class plagResult(object):

    def __init__(self, id1 = None , id2 = None):
        self.tiles = []
        self.similarity = 0.0
        self.id1 = id1
        self.id2 = id2
        self.id1StringLength = 0
        self.id2StringLength = 0
        self.algName = ""
        self.normName = ""
        self.suspectedPlagiarism = False

    def setTiles(self, tiles):
        if type(tiles) != type([]):
            raise NoValidArgumentError
        else:
            self.tiles = tiles

    def getTiles(self):
        rf_tiles = self.tiles
        rf_tiles=sorted(rf_tiles, key=lambda x: x[0])
        rf = []
        i = 0
        for tile in rf_tiles:
            if i == 0:
                rf.append(tile)
                i = i + 1
                continue
            if rf[i - 1][0] == tile[0]:
                continue
            else:
                rf.append(tile)
                i = i + 1
        return rf

    def setSimilarity(self, similarity):
        if not (0 <= similarity <= 1):
            raise OutOfRangeError
        else:
            self.similarity = similarity

    def getSimilarity(self):
        return self.similarity

    def setIdentifier(self, id1, id2):
        self.id1 = id1
        self.id2 = id2

    def getIdentifier(self):
        if self.id1 == None or self.id2 == None:
            raise NoIdentifierSetError
        return [self.id1, self.id2]

    def containsIdentifier(self, id):
        return id==self.id1 or id==self.id2

    def setIdStringLength(self, id1StringLength, id2StringLength):
        self.id1StringLength = id1StringLength
        self.id2StringLength = id2StringLength

    def getIdStringLength(self):
        return [self.id1StringLength, self.id2StringLength]

    def setSuspectedPlagiarism(self, value):
        if type(value) != type(True):
            raise NoValidArgumentError
        self.suspectedPlagiarism = value

    def isSuspectPlagiarism(self):
        return self.suspectedPlagiarism

    def setAlgorithmName(self, algName):
        self.algName = algName

    def getAlgorithmName(self):
        return self.algName

    def setNormalizerName(self, normName):
        self.normName = normName

    def getNormalizerName(self):
        return self.normName

    def __eq__(self, other):
        if other == None:
            return False
        elif (set(self.getIdentifier()) == set(other.getIdentifier())
            and self.getSimilarity() == other.getSimilarity()
            and set(self.getTiles()) == set(other.getTiles())
            and set(self.getIdStringLength()) == set(other.getIdStringLength())):
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return ('plagResult:\n'
                + ' Identifier: ' + str(self.getIdentifier()) + '\n'
                + ' Similarity: ' + str(self.getSimilarity()) + '\n'
                + ' Tiles: ' + str(self.getTiles()) + '\n'
                + ' supected Plagiarism: ' + str(self.isSuspectPlagiarism()) + '\n')

    def __repr__(self):
        return "%s %s %s %s" %(str(self.getIdentifier()), str(self.getSimilarity()),
                str(self.getTiles()), str(self.isSuspectPlagiarism()))
