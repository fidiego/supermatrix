#! /usr/bin/python
import sys, getopt, os
from operator import itemgetter
##################################################################################################################
matrixDirectory = sys.argv[1]
biggest = 1
numNeighbors = 20
##################################################################################################################
##################################################################################################################
def Pairs(matrixDirectory, numNeighbors, biggest):
    ##############################################################################################################
    def Process_Word(matrixDirectory, token, numNeighbors, biggest):
        try:
            token_filehandle = open(matrixDirectory+'/'+token+'.txt')
            
            pmi = []
            pmiSim = []
            coalsSim = []
            beagleSim = []
            docSim = []
            lsaSim = []
            topicsSim = []
            for line in token_filehandle:
                data = (line.strip().strip('\n').strip()).split()
                pmi.append((data[1],float(data[2])))
                pmiSim.append((data[1],float(data[3])))
                coalsSim.append((data[1],float(data[4])))
                beagleSim.append((data[1],float(data[5])))
                docSim.append((data[1],float(data[6])))
                lsaSim.append((data[1],float(data[7])))
                topicsSim.append((data[1],float(data[8])))
            token_filehandle.close()
    
            sPMI = sorted(pmi,key=itemgetter(1),reverse=biggest)
            sPMISim = sorted(pmiSim,key=itemgetter(1),reverse=biggest)
            sCoalsSim = sorted(coalsSim,key=itemgetter(1),reverse=biggest)
            sBeagSim = sorted(beagleSim,key=itemgetter(1),reverse=biggest)
            sDocSim = sorted(docSim,key=itemgetter(1),reverse=biggest)
            sLSASim = sorted(lsaSim,key=itemgetter(1),reverse=biggest)
            sTopicsSim = sorted(topicsSim,key=itemgetter(1),reverse=biggest)
    
            print "***********************************************************************************************************************************************************************************************"
            print "|------------------------|------------------------|-------------------------|-------------------------|-------------------------|--------------------------|--------------------------|"
            print "|      POINTWISE MI      |     PPMI Similarity    |  PPMI + PCA Similarity  |    BEAGLE-C Similarity  |    DocFreq Similarity   |     LSA Similarity       |   LDA Topics Similarity  |"
            print "|------------------------|------------------------|-------------------------|-------------------------|-------------------------|-----------------------------------------------------|"
            for i in range(numNeighbors):
                print "|%12s   %1.5f  |%12s   %1.5f  |%12s    %1.5f  |%12s    %1.5f  |%12s    %1.5f  |%12s    %1.5f  |%12s    %1.5f  |" % (sPMI[i][0], sPMI[i][1], sPMISim[i][0], sPMISim[i][1], sCoalsSim[i][0], sCoalsSim[i][1], sBeagSim[i][0], sBeagSim[i][1], sDocSim[i][0], sDocSim[i][1], sLSASim[i][0], sLSASim[i][1], sTopicsSim[i][0], sTopicsSim[i][1])
            print "***********************************************************************************************************************************************************************************************"
        
        except:
            print "***********************************************************************************************************************************************************************************************"
            print "%s is not in this matrix" % token
            print "***********************************************************************************************************************************************************************************************"
            
    ##############################################################################################################
    def Process_Command(word, numNeighbors, biggest):
        if (word[1] == 'h'):
            print """
            Commands:
                -q      QUIT
                -h      HELP
                -n      CHANGE THE NUMBER OF WORDS DISPLAYED
                -b      TOGGLE LARGEST TO SMALLEST
            """
        elif (word[1] == 'b'):
            if biggest == 1:
                biggest = 0
                print "Now displaying in ascending order"
            else: 
                biggest = 1
                print "Now displaying in descending order"
        elif (word[1] == 'n'):
            param = int((word.split())[1])
            if (param < 1):
                print "Error. Option -n must be positive number."
            else:
                numNeighbors = param
                print "Number of neighbors set to %s" % param
        else:
            print "That is not a valid '-' command. Please type -h for more information."
        return numNeighbors, biggest

    ##############################################################################################################
    print "********************************************************************************************************************"
    print "Welcome to Neighbors. You are using matrix %s" % matrixDirectory
    print "     Type a word to start."
    print "     Type -q to quit"
    print "********************************************************************************************************************"
    token = raw_input()
    while not (token == '-q'):
        if (token[0] == '-'):
            numNeighbors, biggest = Process_Command(token, numNeighbors, biggest)
        else:
            Process_Word(matrixDirectory, token, numNeighbors, biggest)
        token = raw_input()
    sys.exit(1)

##################################################################################################################
##################################################################################################################
Pairs(matrixDirectory, numNeighbors, biggest)
