import sys, getopt, os
############################################################################################
def supermatrix(arguments, documentDirectory, corpusDirectory, inclusionList):

    optlist, args = getopt.getopt(arguments, 'd:c:i:', ['docDirectory=', 'corpusDirectory=', 'inclusionList'])
    for arg, val in optlist:
        if arg in ('-d', '--docdirectory'):
            documentDirectory = val
        if arg in ('-c', '--corpusDirectory'):
            corpusDirectory = val
        if arg in ('-i', '--inclusionList'):
            inclusionList = val
            
    return documentDirectory, corpusDirectory, inclusionList

############################################################################################
def corpCreateFromCorpFile(arguments, corpusFilename, outputDirectory, splitRule, freqOrder, alphaOrder):
    optlist, args = getopt.getopt(arguments, 'C:c:s:fa', ['corpusFilename=', 'outputDirectory=', 'splitRule=', 'freqOrder', 'alphaOrder'])
    for arg, val in optlist:
        if arg in ('-C', '--corpusfilename'):
            corpusFilename = val
        if arg in ('-c', '--outputdirectory'):
            outputDirectory = val
        if arg in ('-s', '--splitrule'):
            splitRule = val
        if arg in ('-f', '--freqorder'):
            freqOrder = 1
        if arg in ('-a', '--alphaorder'):
            alphaOrder = 1
            
    return corpusFilename, outputDirectory, splitRule, freqOrder, alphaOrder

############################################################################################
def corpCreateFromDocDirectory(arguments, documentDirectory, corpusDirectory, freqOrder, alphaOrder):

    optlist, args = getopt.getopt(arguments, 'd:c:fa', ['docDirectory=', 'corpusDirectory=', 'freqOrder', 'alphaOrder'])
    for arg, val in optlist:
        if arg in ('-d', '--docdirectory'):
            documentDirectory = val
        if arg in ('-c', '--corpusDirectory'):
            corpusDirectory = val
        if arg in ('-f', '--freqorder'):
            freqOrder = 1
        if arg in ('-a', '--alphaorder'):
            alphaOrder = 1
            
    return documentDirectory, corpusDirectory, freqOrder, alphaOrder

############################################################################################
def corpModify(arguments, corpusDirectory, outputDirectory, translateFile, freqOrder, alphaOrder):
    optlist, args = getopt.getopt(arguments, 'c:o:t:f:a:', ['corpusDirectory=', 'outputDirectory=', 'translateFile=', 'freqOrder=', 'alphaOrder='])
    for arg, val in optlist:
        if arg in ('-c', '--corpusDirectory'):
            corpusDirectory = val
        if arg in ('-o', '--outputDirectory'):
            outputDirectory = val
        if arg in ('-t', '--translateFile'):
            translateFile = val
        if arg in ('-f', '--freqOrder'):
            freqOrder = int(val)
        if arg in ('-a', '--alphaOrder'):
            alphaOrder = int(val)
            
    return corpusDirectory, outputDirectory, translateFile, freqOrder, alphaOrder

############################################################################################
def corpGetSubDocuments(arguments, corpusDirectory, outputFilename, typeThreshold, tokenThreshold, numDocumentsThreshold, includeListFilename, excludeListFilename):
    optlist, args = getopt.getopt(arguments, 'c:o:t:T:n:i:e:', ['corpusDirectory=', 'outputFilename=', 'typeThreshold=', 'tokenThreshold=', 'numDocuments=', 'includeList=', 'excludeList='])
    for arg, val in optlist:
        if arg in ('-c', '--corpusDirectory'):
            corpusDirectory = val
        if arg in ('-o', '--outputFilename'):
            outputFilename = val
        if arg in ('-t', '--typeThreshold'):
            typeThreshold = int(val)
        if arg in ('-T', '--tokenThreshold'):
            tokenThreshold = int(val)
        if arg in ('-n', '--numDocuments'):
            numDocumentsThreshold = int(val)
        if arg in ('-i', '--includeList'):
            includeListFilename = val
        if arg in ('-e', '--excludeList'):
            excludeListFilename = val
            
    return corpusDirectory, outputFilename, typeThreshold, tokenThreshold, numDocumentsThreshold, includeListFilename, excludeListFilename
    
############################################################################################
def corpGetTargetSublist(arguments, corpusDirectory, outputFilename, frequencyThreshold, numTargetsThreshold, docPropThreshold, includeListFilename, excludeListFilename):
    optlist, args = getopt.getopt(arguments, 'c:o:f:n:d:i:e:', ['corpusDirectory=', 'outputFilename=', 'frequencyThreshold=', 'numTargetsThreshold=', 'docPropThreshold=', 'includeList=', 'excludeList='])
    for arg, val in optlist:
        if arg in ('-c', '--corpusDirectory'):
            corpusDirectory = val
        if arg in ('-o', '--outputFilename'):
            outputFilename = val
        if arg in ('-f', '--frequencyThreshold'):
            frequencyThreshold = int(val)
        if arg in ('-n', '--numTargetsThreshold'):
            numTargetsThreshold = int(val)
        if arg in ('-d', '--docPropThreshold'):
            docPropThreshold = float(val)
        if arg in ('-i', '--includeList'):
            includeListFilename = val
        if arg in ('-e', '--excludeList'):
            excludeListFilename = val
            
    return corpusDirectory, outputFilename, frequencyThreshold, numTargetsThreshold, docPropThreshold, includeListFilename, excludeListFilename

############################################################################################
def createTDMatrix(arguments, corpusDirectory, matrixDirectory, targetFilename, documentFilename):
    
    optlist, args = getopt.getopt(arguments, 'c:m:T:D:', ['corpusDirectory=', 'matrixDirectory=', 'targetFile=', 'documentFile=', ])
    for arg, val in optlist:
        if arg in ('-c', '--corpusdirectory'):
            corpusDirectory = val
        if arg in ('-m', '--matrixDirectory'):
            matrixDirectory = val
        if arg in ('-T', '--targetfile'):
            targetFilename = val
        if arg in ('-D', '--documentfile'):
            documentFilename = val        
            
    if not corpusDirectory:
        print
        print "Error: You didn't specify a corpus directory"
        sys.exit(0)

    if not matrixDirectory:
        print
        print "Error: You didn't specify a matrix (output) directory"
        sys.exit(0)
    
    if not targetFilename:
        print
        print "Warning: You did not specify a target list filename; all words in the corpus will be used"
    
    if not documentFilename:
        print
        print "Warning: You did not specify a document list filename; all documents in the corpus will be used"
    
    return corpusDirectory, matrixDirectory, targetFilename, documentFilename
############################################################################################
def createCollapsedTCMatrix(arguments, corpusDirectory, matrixDirectory, targetFilename, documentFilename, windowSize):
    
    optlist, args = getopt.getopt(arguments, 'c:m:T:D:W:d', ['corpusDirectory=', 'matrixDirectory=', 'targetFile=', 'documentFile=', 'windowsize='])
    for arg, val in optlist:
        if arg in ('-c', 'corpusDirectory'):
            corpusDirectory = val
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-T', 'targetFile'):
            targetFilename = val
        if arg in ('-D', 'documentFile'):
            documentFilename = val
        if arg in ('-W', 'windowsize'):
            windowSize = int(val)

    if not corpusDirectory:
        print
        print "Error: You didn't specify a corpus directory"
        sys.exit(0)

    if not matrixDirectory:
        print
        print "Error: You didn't specify a matrix (output) directory"
        sys.exit(0)

    if not targetFilename:
        print "Warning: You did not specify a target list filename; all words in the corpus will be used"

    if not documentFilename:
        print "Warning: You did not specify a document list filename; all documents in the corpus will be used"

    if not windowSize:
        print
        print "Error: You didn't specify a window size"
        sys.exit(0)

    return corpusDirectory, matrixDirectory, targetFilename, documentFilename, windowSize
    
############################################################################################
def createTCMatrix(arguments, corpusDirectory, matrixDirectory, targetFilename, contextFilename, documentFilename, windowSize, distinctDocs):
    
    optlist, args = getopt.getopt(arguments, 'c:m:T:C:D:W:d', ['corpusDirectory=', 'matrixDirectory=', 'targetFile=', 'contextFile=', 'documentFile=', 'windowsize=', 'distinctDocs'])
    for arg, val in optlist:
        if arg in ('-c', 'corpusDirectory'):
            corpusDirectory = val
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-T', 'targetFile'):
            targetFilename = val
        if arg in ('-C', 'contextFile'):
            contextFilename = val
        if arg in ('-D', 'documentFile'):
            documentFilename = val
        if arg in ('-W', 'windowsize'):
            windowSize = int(val)
        if arg in ('-d', 'distinctdocs'):
            distinctDocs = 1

    if not corpusDirectory:
        print
        print "Error: You didn't specify a corpus directory"
        sys.exit(0)

    if not matrixDirectory:
        print
        print "Error: You didn't specify a matrix (output) directory"
        sys.exit(0)

    if not targetFilename:
        print "Warning: You did not specify a target list filename; all words in the corpus will be used"

    if not contextFilename:
        print "Warning: You did not specify a context list filename; all words in the corpus will be used"

    if not documentFilename:
        print "Warning: You did not specify a document list filename; all documents in the corpus will be used"

    if not windowSize:
        print
        print "Error: You didn't specify a window size"
        sys.exit(0)

    return corpusDirectory, matrixDirectory, targetFilename, contextFilename, documentFilename, windowSize, distinctDocs
    
############################################################################################
def reduceTDMatrixLDA(arguments, matrixDirectory, outputDirectory, alphaList, betaList, numTopicsList, numIterations, randomSeed, numChains, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, trackHistories, numRowAssignmentOutputs ):

    optlist, args = getopt.getopt(arguments, 'm:o:A:B:T:N:S:C:i:e:I:E:hx:', ['matrixDirectory=', 'outputDirectory=', 'alpha=', 'beta=', 'numTopics=', 'numIterations=', 'randomSeed=', 'numChains=', 'rowInclude=', 'rowExclude=', 'columnInclude=', 'columnExclude=', 'trackHistories', 'rowOutputs=' ])
    
    for arg, val in optlist:
        if arg == '-m':
            matrixDirectory = val
        if arg == '-o':
            outputDirectory = val            
        if arg == '-A':
            alphaList = []
            alphaList.append(float(val))
        if arg == '-B':
            betaList = []
            betaList.append(float(val))
        if arg == '-T':
            numTopicsList = []
            numTopicsList.append(int(val))
        if arg == '-N':
            numIterations = int(val)    
        if arg == '-S':
            randomSeed = int(val)
        if arg == '-C':
            numChains = int(val)
        if arg == '-i':
            rowInclusionFilename = val
        if arg == '-e':
            rowExclusionFilename = val
        if arg == '-I':
            columnInclusionFilename = val
        if arg == '-E':
            columnExclusionFilename = val
        if arg == '-h':
            trackHistories = 1
        if arg == '-x':
            numRowAssignmentOutputs = int(val)
    if randomSeed == 0:
        randomSeed =os.urandom(n)
    
    return matrixDirectory, outputDirectory, alphaList, betaList, numTopicsList, numIterations, randomSeed, numChains, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, trackHistories, numRowAssignmentOutputs

############################################################################################
def reduceTDMatrixSVD(arguments, matrixDirectory, outputDirectory, normalizationMethod, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename):
    
    optlist, args = getopt.getopt(arguments, 'm:o:N:i:e:I:E:', ['matrixDirectory=', 'outputDirectory=', 'normMethod=', 'rowInclude=', 'rowExclude=', 'colInclude=', 'colExclude='])
    
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputDirectory'):
            outputDirectory = val
        if arg in ('-i', 'rowInclude'):
            rowInclusionFilename = val
        if arg in ('-e', 'rowInclude'):
            rowExclusionFilename = val
        if arg in ('-I', 'colInclude'):
            columnInclusionFilename = val
        if arg in ('-E', 'colExclude'):
            columnExclusionFilename = val
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
            
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)

    if outputDirectory == 0:
        print "Error: You did not specify an output directory"
        sys.exit(1)

    return matrixDirectory, outputDirectory, normalizationMethod, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename

###########################################################################################
def reduceTCMatrixSVD(arguments, matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod):

    optlist, args = getopt.getopt(arguments, 'm:o:i:e:I:E:D:S:C:W:N:', ['matrixDirectory=', 'outputDirectory=', 'rowInclude=', 'rowExclude=', 'colInclude=', 'colExclude=', 'normMethod='])
    
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputDirectory'):
            outputDirectory = val
        if arg in ('-i', 'rowInclude'):
            rowInclusionFilename = val
        if arg in ('-e', 'rowInclude'):
            rowExclusionFilename = val
        if arg in ('-I', 'colInclude'):
            columnInclusionFilename = val
        if arg in ('-E', 'colExclude'):
            columnExclusionFilename = val
        if arg in ('-D', 'direction'):
            directionType = int(val)
        if arg in ('-S', 'windowSize'):
            windowSize = int(val)
        if arg in ('-C', 'collapseWindow'):
            collapseWindow = int(val)
        if arg in ('-W', 'windowWeighting'):
            windowWeighting = int(val)
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
            
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)

    if outputDirectory == 0:
        print "Error: You did not specify an output directory"
        sys.exit(1)

    return matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod
    
###########################################################################################
def reduceTCMatrixICA(arguments, matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod):

    optlist, args = getopt.getopt(arguments, 'm:o:i:e:I:E:D:S:C:W:N:', ['matrixDirectory=', 'outputDirectory=', 'rowInclude=', 'rowExclude=', 'colInclude=', 'colExclude=', 'normMethod='])
    
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputDirectory'):
            outputDirectory = val
        if arg in ('-i', 'rowInclude'):
            rowInclusionFilename = val
        if arg in ('-e', 'rowInclude'):
            rowExclusionFilename = val
        if arg in ('-I', 'colInclude'):
            columnInclusionFilename = val
        if arg in ('-E', 'colExclude'):
            columnExclusionFilename = val
        if arg in ('-D', 'direction'):
            directionType = int(val)
        if arg in ('-S', 'windowSize'):
            windowSize = int(val)
        if arg in ('-C', 'collapseWindow'):
            collapseWindow = int(val)
        if arg in ('-W', 'windowWeighting'):
            windowWeighting = int(val)
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
            
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)

    if outputDirectory == 0:
        print "Error: You did not specify an output directory"
        sys.exit(1)

    return matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod

###########################################################################################
def reduceTDMatrixRVA(arguments, matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, normalizationMethod, randomVectorLength, randomMean, randomSD, randomSeed):

    optlist, args = getopt.getopt(arguments, 'm:o:i:e:I:E:N:L:M:S:R:', ['matrixDirectory=', 'outputDirectory=', 'rowInclude=', 'rowExclude=', 'colInclude=', 'colExclude=', 'normMethod=', 'vectorSize=', 'randomMean=', 'randomSD=', 'randomSeed='])
    
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputDirectory'):
            outputDirectory = val
        if arg in ('-i', 'rowInclude'):
            rowInclusionFilename = val
        if arg in ('-e', 'rowInclude'):
            rowExclusionFilename = val
        if arg in ('-I', 'colInclude'):
            columnInclusionFilename = val
        if arg in ('-E', 'colExclude'):
            columnExclusionFilename = val
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-L', 'vectorSize'):
            randomVectorLength = int(val)
        if arg in ('-M', 'randomMean'):
            randomMean = int(val)
        if arg in ('-S', 'randomSD'):
            randomSD = int(val)
        if arg in ('-R', 'randomSeed'):
            randomSeed = int(val)
            
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)

    if outputDirectory == 0:
        print "Error: You did not specify an output directory"
        sys.exit(1)

    if randomVectorLength == 0:
        print "Warning, you did not specify a random vector length. Using n = 100)."
        randomVectorLength = 100
    
    if randomSD == 0:
        print "Warning: you did not specify a random vector SD. Using 1/Length)."
        randomSD = float(1)/randomVectorLength
        
    return matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, normalizationMethod, randomVectorLength, randomMean, randomSD, randomSeed

###########################################################################################
def reduceTCMatrixRVA(arguments, matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, normalizationMethod, randomVectorLength, randomMean, randomSD, windowSize, randomSeed):

    optlist, args = getopt.getopt(arguments, 'm:o:i:e:I:E:N:L:M:S:W:R:', ['matrixDirectory=', 'outputDirectory=', 'rowInclude=', 'rowExclude=', 'colInclude=', 'colExclude=', 'normMethod=', 'vectorSize=', 'randomMean=', 'randomSD=', 'windowSize=', 'randomSeed='])
    
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputDirectory'):
            outputDirectory = val
        if arg in ('-i', 'rowInclude'):
            rowInclusionFilename = val
        if arg in ('-e', 'rowInclude'):
            rowExclusionFilename = val
        if arg in ('-I', 'colInclude'):
            columnInclusionFilename = val
        if arg in ('-E', 'colExclude'):
            columnExclusionFilename = val
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-L', 'vectorSize'):
            randomVectorLength = int(val)
        if arg in ('-M', 'randomMean'):
            randomMean = int(val)
        if arg in ('-S', 'randomSD'):
            randomSD = int(val)
        if arg in ('-W', 'windowSize'):
            windowSize = int(val)
        if arg in ('-R', 'randomSeed'):
            randomSeed = int(val)
            
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)

    if outputDirectory == 0:
        print "Error: You did not specify an output directory"
        sys.exit(1)

    if randomVectorLength == 0:
        print "Warning, you did not specify a random vector length. Using n = 100)."
        randomVectorLength = 100
    
    if randomSD == 0:
        print "Warning: you did not specify a random vector SD. Using 1/Length)."
        randomSD = float(1)/randomVectorLength
        
    return matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, normalizationMethod, randomVectorLength, randomMean, randomSD, windowSize, randomSeed

###########################################################################################
def calcTDMatrixSims(arguments, matrixDirectory, targetIncludeFile, targetExcludeFile, documentIncludeFile, documentExcludeFile, normalizationMethod, similarityMetric):

    optlist, args = getopt.getopt(arguments, 'm:i:e:I:E:N:M:', ['matrixDirectory=', 'targetInclude=', 'targetExclude=', 'contextInclude=', 'contextExclude=', 'normMethod=', 'simMetric='])
    
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-i', 'targetInclude'):
            targetIncludeFile = val
        if arg in ('-e', 'targetExclude'):
            targetExcludeFile = val
        if arg in ('-I', 'docInclude'):
            documentIncludeFile = val
        if arg in ('-E', 'docExclude'):
            documentExcludeFile = val        
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-M', 'simMetric'):
            similarityMetric = int(val)

    if matrixDirectory == 0:
        print "Error: You did not specify an matrix directory"
        sys.exit(1)

    if similarityMetric == 0:
        print "Error: You did not specify a similarity metric"
        sys.exit(1)

    return matrixDirectory, targetIncludeFile, targetExcludeFile, documentIncludeFile, documentExcludeFile, normalizationMethod, similarityMetric

###########################################################################################
def calcTCMatrixSims(arguments, matrixDirectory, targetIncludeFile, targetExcludeFile, contextIncludeFile, contextExcludeFile, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod, similarityMetric):
    
    optlist, args = getopt.getopt(arguments, 'm:i:e:I:E:D:S:C:W:N:M:', ['matrixDirectory=', 'targetInclude=', 'targetExclude=', 'contextInclude=', 'contextExclude=', 'normMethod=', 'direction=', 'windowSize=', 'collapseWindow=', 'windowWeighting=', 'simMetric='])
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-i', 'targetInclude'):
            targetIncludeFile = val
        if arg in ('-e', 'targetExclude'):
            targetExcludeFile = val
        if arg in ('-I', 'contextInclude'):
            contextIncludeFile = val
        if arg in ('-E', 'contextExclude'):
            contextExcludeFile = val            
        if arg in ('-D', 'direction'):
            directionType = int(val)
        if arg in ('-S', 'windowSize'):
            windowSize = int(val)
        if arg in ('-C', 'collapseWindow'):
            collapseWindow = int(val)
        if arg in ('-W', 'windowWeighting'):
            windowWeighting = int(val)
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-M', 'simMetric'):
            similarityMetric = int(val)
    
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)
    
    return matrixDirectory, targetIncludeFile, targetExcludeFile, contextIncludeFile, contextExcludeFile, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod, similarityMetric

###########################################################################################
def calcSentiments(arguments, matrixDirectory, outputDirectory, targetFilename, featureFilename, documentFilename, normalizationMethod):
    
    optlist, args = getopt.getopt(arguments, 'm:o:T:F:D:N:', ['matrixDirectory=', 'outputDirectory=', 'targetFile=', 'featureFile=', 'documentFile=', 'normMethod='])
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputDirectory'):
            outputDirectory = val
        if arg in ('-T', 'targetFile'):
            targetFilename = val
        if arg in ('-F', 'featureFile'):
            featureFilename = val
        if arg in ('-D', 'documentFile'):
            documentFilename = val            
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
    
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)
    
    return matrixDirectory, outputDirectory, targetFilename, featureFilename, documentFilename, normalizationMethod

###########################################################################################
def calcTCMatrixDiagFeats(arguments, matrixDirectory, targetIncludeFile, targetExcludeFile, contextIncludeFile, contextExcludeFile, normalizationMethod, categoryFilename, outputDirectory):
    
    optlist, args = getopt.getopt(arguments, 'm:i:e:I:E:N:c:o:', ['matrixDirectory=', 'targetInclude=', 'targetExclude=', 'contextInclude=', 'contextExclude=', 'normMethod=', 'categoryFileName=', 'outputDirectory='])
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-i', 'targetInclude'):
            targetIncludeFile = val
        if arg in ('-e', 'targetExclude'):
            targetExcludeFile = val
        if arg in ('-I', 'contextInclude'):
            contextIncludeFile = val
        if arg in ('-E', 'contextExclude'):
            contextExcludeFile = val            
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-c', 'categoryFileName'):
            categoryFilename = val
        if arg in ('-o', 'outputDirectory'):
            outputDirectory = val
    
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)
    
    return matrixDirectory, targetIncludeFile, targetExcludeFile, contextIncludeFile, contextExcludeFile, normalizationMethod, categoryFilename, outputDirectory

###########################################################################################
def calcTCMatrixCollapsedSims(arguments, matrixDirectory, targetIncludeFile, targetExcludeFile, normalizationMethod, similarityMetric):
    
    optlist, args = getopt.getopt(arguments, 'm:i:e:N:M:', ['matrixDirectory=', 'targetInclude=', 'targetExclude=', 'normMethod=', 'simMetric='])
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-i', 'targetInclude'):
            targetIncludeFile = val
        if arg in ('-e', 'targetExclude'):
            targetExcludeFile = val
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-M', 'simMetric'):
            similarityMetric = int(val)
    
    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)
    
    return matrixDirectory, targetIncludeFile, targetExcludeFile, normalizationMethod, similarityMetric
###########################################################################################
def calcSVDSims(arguments, svdDirectory, numDimensions, rowInclusionList, rowExclusionList, normalizationMethod, similarityMetric):

    optlist, args = getopt.getopt(arguments, 's:n:i:e:N:M:', ['svdDirectory=', 'numDimensions=', 'rowInclude=', 'rowExclude=', 'normMethod=', 'simMetric='])
    
    for arg, val in optlist:
        if arg in ('-s', 'svdDirectory'):
            svdDirectory = val
        if arg in ('-n', 'numDimensions'):            
            numDimensions = int(val)
        if arg in ('-i', 'rowInclude'):
            rowInclusionList = val
        if arg in ('-e', 'rowExclude'):
            rowExclusionList = val          
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-M', 'simMetric'):
            similarityMetric = int(val)

    if svdDirectory == 0:
        print "Error: You did not specify an svd model directory"
        sys.exit(1)

    if similarityMetric == 0:
        print "Error: You did not specify a similarity metric"
        sys.exit(1)

    return svdDirectory, numDimensions, rowInclusionList, rowExclusionList, normalizationMethod, similarityMetric

###########################################################################################
def calcLDASims(arguments, chainDirectory, normalizationMethod, similarityMetric, rowInclusionFile, rowExclusionFile):

    optlist, args = getopt.getopt(arguments, 'c:N:M:i:e:', ['chainDirectory=', 'normMethod=', 'simMetric=', 'targetLabels=', 'rowInclude=', 'rowExclude='])
    
    for arg, val in optlist:
        if arg in ('-c', 'chainDirectory'):
            chainDirectory = val
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-M', 'simMetric'):
            similarityMetric = int(val)
        if arg in ('-i', 'rowInclude'):
            rowInclusionFile = val
        if arg in ('-e', 'rowExclude'):
            rowExclusionFile = val

    if chainDirectory == 0:
        print "Error: You did not specify an lda chain directory"
        sys.exit(1)

    if similarityMetric == 0:
        print "Error: You did not specify a similarity metric"
        sys.exit(1)

    return chainDirectory, normalizationMethod, similarityMetric, rowInclusionFile, rowExclusionFile

###########################################################################################
def calcRVASims(arguments, rvaDirectory, rowInclusionFilename, rowExclusionFilename, normalizationMethod, similarityMetric):

    optlist, args = getopt.getopt(arguments, 'r:i:e:N:M:', ['rvaDirectory=', 'rowInclude=', 'rowExclude=', 'normMethod=', 'simMetric=', 'rowExclude='])
    
    for arg, val in optlist:
        if arg in ('-r', 'rvaDirectory'):
            rvaDirectory = val
        if arg in ('-i', 'rowInclude'):
            rowInclusionFilename = val
        if arg in ('-e', 'rowExclude'):
            rowExclusionFilename = val
        if arg in ('-N', 'normMethod'):
            normalizationMethod = int(val)
        if arg in ('-M', 'simMetric'):
            similarityMetric = int(val)

    if similarityMetric == 0:
        print "Error: You did not specify a similarity metric"
        sys.exit(1)

    return rvaDirectory, rowInclusionFilename, rowExclusionFilename, normalizationMethod, similarityMetric
###########################################################################################
def outputSimNeighbors(arguments, similarityFile, targetListIndexFile, numNeighbors):

    optlist, args = getopt.getopt(arguments, 's:t:n:a:o:', ['similarityFile=', 'targetFile=', 'numNeighbors='])
    for arg, val in optlist:
        if arg in ('-s', 'similarityFile'):
            similarityFile = val
        if arg in ('-t', 'targetFile'):
            targetListIndexFile = val
        if arg in ('-n', 'numNeighbors'):
            numNeighbors = int(val)

    if similarityFile == 0:
        print "Error: You did not specify a similarity file"
        sys.exit(1)

    if targetListIndexFile == 0:
        print "Error: You did not specify a target index file"
        sys.exit(1)

    return similarityFile, targetListIndexFile, numNeighbors

###########################################################################################
def outputSimNDensities(arguments, similarityFile, targetListIndexFile, numNeighbors):

    optlist, args = getopt.getopt(arguments, 's:t:n:', ['similarityFile=', 'targetFile=', 'numNeighbors='])
    for arg, val in optlist:
        if arg in ('-s', 'similarityFile'):
            similarityFile = val
        if arg in ('-t', 'targetFile'):
            targetListIndexFile = val
        if arg in ('-n', 'numNeighbors'):
            numNeighbors = int(val)

    if similarityFile == 0:
        print "Error: You did not specify a similarity file"
        sys.exit(1)

    if targetListIndexFile == 0:
        print "Error: You did not specify a target index file"
        sys.exit(1)

    return similarityFile, targetListIndexFile, numNeighbors

###########################################################################################
def outputTargetSimPairs(arguments, pairFile, similarityFile, targetListIndexFile):

    optlist, args = getopt.getopt(arguments, 'p:s:t:', ['pairFile=', 'similarityFile=', 'targetFile='])
    for arg, val in optlist:
        if arg in ('-p', 'pairFile'):
            pairFile = val
        if arg in ('-s', 'similarityFile'):
            similarityFile = val
        if arg in ('-t', 'targetFile'):
            targetListIndexFile = val

    if pairFile == 0:
        print "Error: You did not specify a file containing a list of word pairs"
        sys.exit(1)

    if similarityFile == 0:
        print "Error: You did not specify a similarity file"
        sys.exit(1)

    if targetListIndexFile == 0:
        print "Error: You did not specify a target index file"
        sys.exit(1)

    return pairFile, similarityFile, targetListIndexFile

############################################################################################
def outputTCMatrixRepetitions(arguments, matrixDirectory, outputFile, targetInclusionFile, targetExclusionFile, windowSize):

    optlist, args = getopt.getopt(arguments, 'm:o:i:e:w:', ['matrixDirectory=', 'outputFile=', 'targetInclusionFile=', 'targetExclusionFile=', 'windowSize='])
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputFile'):
            outputFile = val
        if arg in ('-i', 'targetInclusionFile'):
            targetInclusionFile = val
        if arg in ('-e', 'targetExclusionFile'):
            targetExclusionFile = val
        if arg in ('-w', 'windowSize'):
            windowSize = int(val)

    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)
    
    if targetInclusionFile == 0:
        print "Warning: You did not specify a list of targets to include; will calculate repetitions for all targets in the corpus (minus any words in an exclusion file)"
        
    return matrixDirectory, outputFile, targetInclusionFile, targetExclusionFile, windowSize

###########################################################################################
def outputSquareAssociations(arguments, matrixDirectory, targetInclusionFile, targetExclusionFile, directionType, windowSize, windowWeighting, normalizationMethod, outputFilename):

    optlist, args = getopt.getopt(arguments, 'm:o:i:e:D:S:W:N:', ['matrixDirectory=', 'outputFile=', 'targetInclusionFile=', 'targetExclusionFile=', 'directionType=', 'windowSize=', 'windowWeighting=', 'normalizationMethod=',])
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputFile'):
            outputFilename = val
        if arg in ('-i', 'targetInclusionFile'):
            targetInclusionFile = val
        if arg in ('-e', 'targetExclusionFile'):
            targetExclusionFile = val
        if arg in ('-D', 'directionType'):
            directionType = int(val)
        if arg in ('-S', 'windowSize'):
            windowSize = int(val)
        if arg in ('-W', 'windowWeighting'):
            windowWeighting = int(val)
        if arg in ('-N', 'normalizationMethod'):
            normalizationMethod = int(val)

    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)
    
    if targetInclusionFile == 0:
        print "Warning: You did not specify a list of targets to include; will calculate repetitions for all targets in the corpus (minus any words in an exclusion file)"

    return matrixDirectory, targetInclusionFile, targetExclusionFile, directionType, windowSize, windowWeighting, normalizationMethod, outputFilename
    
    
###########################################################################################
def outputTargetPairAssociations(arguments, matrixDirectory, pairFile, outputFilename, directionType, windowSize, windowWeighting, normalizationMethod, outputAsProbabilityDistribution):

    optlist, args = getopt.getopt(arguments, 'm:p:o:D:S:W:N:', ['matrixDirectory=', 'pairFile=', 'outputFile=', 'directionType=', 'windowSize=', 'windowWeighting=', 'normalizationMethod=', 'outputAsProbs='])
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-p', 'pairFile'):
            pairFile = val
        if arg in ('-o', 'outputFile'):
            outputFilename = val
        if arg in ('-D', 'directionType'):
            directionType = int(val)
        if arg in ('-S', 'windowSize'):
            windowSize = int(val)
        if arg in ('-W', 'windowWeighting'):
            windowWeighting = int(val)
        if arg in ('-N', 'normalizationMethod'):
            normalizationMethod = int(val)

    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)
    
    if pairFile == 0:
        print "Error, you did not specify a file containing a list of pairs"
        
    if ((directionType < 1) or (directionType > 3)):
        print "Error, Direction type (-D) must be either 1, 2, or 3"
        sys.exit(1)

    return matrixDirectory, pairFile, outputFilename, directionType, windowSize, windowWeighting, normalizationMethod, outputAsProbabilityDistribution
    
###########################################################################################
def outputWordDiversities(arguments, matrixDirectory, targetInclusionFile, targetExclusionFile, directionType, windowSize, outputFilename):

    optlist, args = getopt.getopt(arguments, 'm:o:i:e:D:S:', ['matrixDirectory=', 'outputFile=', 'targetInclusionFile=', 'targetExclusionFile=', 'directionType=', 'windowSize='])
    for arg, val in optlist:
        if arg in ('-m', 'matrixDirectory'):
            matrixDirectory = val
        if arg in ('-o', 'outputFile'):
            outputFilename = val
        if arg in ('-i', 'targetInclusionFile'):
            targetInclusionFile = val
        if arg in ('-e', 'targetExclusionFile'):
            targetExclusionFile = val
        if arg in ('-D', 'directionType'):
            directionType = int(val)
        if arg in ('-S', 'windowSize'):
            windowSize = int(val)

    if matrixDirectory == 0:
        print "Error: You did not specify a matrix directory"
        sys.exit(1)
    
    if targetInclusionFile == 0:
        print "Warning: You did not specify a list of targets to include; will calculate diversities for all targets in the corpus (minus any words in an exclusion file)"

    return matrixDirectory, targetInclusionFile, targetExclusionFile, directionType, windowSize, outputFilename
###########################################################################################
def outputMatrixData(arguments, corpusDirectory):

    optlist, args = getopt.getopt(arguments, 'c:', ['corpusDirectory='])
    for arg, val in optlist:
        if arg in ('-c', 'corpusDirectory'):
            corpusDirectory = val

    if corpusDirectory == 0:
        print "Error: You did not specify a corpus directory"
        sys.exit(1)

    return corpusDirectory
    
###########################################################################################
def output_targetFreqs(arguments, corpusDirectory, outputFilename, includeListFilename, ExcludeListFilename, sortByFreq, partsPerMillion, logged):
    
    optlist, args = getopt.getopt(arguments, 'c:o:i:e:spl', ['corpus=', 'output=', 'include=', 'exclude=', 'sort', 'ppm', 'log'])
    for arg, val in optlist:
        if arg in ('-c', 'corpus'):
            corpusDirectory = val
        if arg in ('-o', 'output'):
            outputFilename = val
        if arg in ('-i', 'include'):
            includeListFilename = val
        if arg in ('-e', 'exclude'):
            ExcludeListFilename = val
        if arg in ('-s', 'sort'):
            sortByFreq = 1
        if arg in ('-p', 'ppm'):
            partsPerMillion = 1
        if arg in ('-l', 'log'):
            logged = 1
 
    return corpusDirectory, outputFilename, includeListFilename, ExcludeListFilename, sortByFreq, partsPerMillion, logged
    
###########################################################################################
def output_targetDocDiversities(arguments, corpusDirectory, outputFilename, includeListFilename, ExcludeListFilename):
    
    optlist, args = getopt.getopt(arguments, 'c:o:i:e:', ['corpus=', 'output=', 'include=', 'exclude='])
    for arg, val in optlist:
        if arg in ('-c', 'corpus'):
            corpusDirectory = val
        if arg in ('-o', 'output'):
            outputFilename = val
        if arg in ('-i', 'include'):
            includeListFilename = val
        if arg in ('-e', 'exclude'):
            ExcludeListFilename = val
 
    return corpusDirectory, outputFilename, includeListFilename, ExcludeListFilename