##############################################################################
# define and set program parameters
corpusDirectory = 0                 # -c: the path of the directory containing the corpus.
outputFilename = 0                  # -o: the name of the target list file that will be created
frequencyThreshold = 0              # -f: the frequency threshold; targets with frequency less than this amount will excluded
numTargetsThreshold = 0             # -n: the maximum number of targets to have in the final output list. If zero, all targets meeting freq and doc threholds will be included
docPropThreshold = 0                # -d: the minimum proportion of docs a target must occur in to be included in the sublist
includeListFilename = 0             # -i: the path of the file that is a list of targets to force include
excludeListFilename = 0             # -e: the path of the file that is a list of targets to force exclude
##############################################################################
# import python libraries
import sys
import sm_libs.scriptParams as params
import sm_libs.corpora as corpora
##############################################################################

# process command line arguments
corpusDirectory, outputFilename, frequencyThreshold, numTargetsThreshold, docPropThreshold, includeListFilename, excludeListFilename = params.corpGetTargetSublist(sys.argv[1:], corpusDirectory, outputFilename, frequencyThreshold, numTargetsThreshold, docPropThreshold, includeListFilename, excludeListFilename)

# create and initialize a corpus object, import corpus info
theCorpus = corpora.corpus()
theCorpus.importCorpusInfo(corpusDirectory)
theCorpus.importTargetInfo()
theCorpus.importDocumentInfo()

# create and initialize a corpus object, import corpus info
theCorpus.outputTargetSubList(outputFilename, frequencyThreshold, numTargetsThreshold, docPropThreshold, includeListFilename, excludeListFilename)
