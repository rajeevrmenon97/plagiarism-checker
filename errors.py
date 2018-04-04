class PlagDetectorError(Exception): pass

class OutOfRangeError(PlagDetectorError): pass

class NoValidArgumentError(PlagDetectorError): pass

class NoValidNameError(PlagDetectorError):

    def __init__(self, wrongName, availableNamesList):
        self.wrongName = str(wrongName)
        self.availableNames = str(availableNamesList)

    def __str__(self):
        print ("The used name " + self.wrongName + " is not defined.\n" \
             + "Following name ids are legal to use:\n" + self.availableNames)

class NoValidNormalizerNameError(NoValidNameError): pass
class NoValidAlgorithmNameError(NoValidNameError): pass

class NoIdentifierSetError(PlagDetectorError): pass
