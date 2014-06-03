##############################################################################
# define and set program parameters
documentDirectory = 0           # -d: the path of the directory containing the documents.
corpusDirectory = 0             # -c: the name of the directory that will be created
freqOrder = 1                   # -f: output the words in frequency (high to low) order
alphaOrder = 0                  # -a: output the owrds in alphabetical order
##############################################################################
# import python libraries
import sys, getopt
import sm_libs.scriptParams as params
import sm_libs.corpora as corpora
##############################################################################

# process command line arguments
documentDirectory, corpusDirectory, freqOrder, alphaOrder = params.corpCreateFromDocDirectory(sys.argv[1:], documentDirectory, corpusDirectory, freqOrder, alphaOrder)

# create and initialize a corpus object
theCorpus = corpora.corpus()
theCorpus.initializeNewCorpus(corpusDirectory, freqOrder, alphaOrder)

# get the list of documents from the document directory
theCorpus.getSeparateDocumentList(documentDirectory)

# get counts of word types and tokens from separate documents, and print merged corpus file
theCorpus.countAndMergeSeparateDocuments()

# output the various information files
theCorpus.outputCorpusInfo()
theCorpus.outputTargetInfo()
theCorpus.outputDocumentInfo()