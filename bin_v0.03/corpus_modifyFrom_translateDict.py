##############################################################################
# define and set program parameters
corpusDirectory = 0           # -d: the path of the directory containing the documents.
outputDirectory = 0           # -o: the name of the directory that will be created
translateFile = 0             # -t: the name of the file containing the string translation definitions
freqOrder = 1                 # -f: output the words in frequency (high to low) order
alphaOrder = 0                # -a: output the owrds in alphabetical order
##############################################################################
# import python libraries
import sys, getopt
import sm_libs.scriptParams as params
import sm_libs.corpora as corpora
##############################################################################

# process command line arguments
corpusDirectory, outputDirectory, translateFile, freqOrder, alphaOrder = params.corpModify(arguments, corpusDirectory, translateFile, freqOrder, alphaOrder)

# create and initialize a corpus object
theCorpus = corpora.corpus()
theCorpus.initializeModifiedCorpus(corpusDirectory, outputDirectory, freqOrder, alphaOrder)
theCorpus.importDocumentNames()

# get counts of word types and tokens from separate documents, and print merged corpus file
theCorpus.modifyCorpus(translateFile)

# output the various information files
theCorpus.outputCorpusInfo()
theCorpus.outputTargetInfo()
theCorpus.outputDocumentInfo()