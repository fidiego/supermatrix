##############################################################################
# default parameters
corpusDirectory = 0                     # -c    the directory containing the corpus
outputFilename = "docDiversities.txt"   # -o    output filename that will be created
includeListFilename = 0                 # -i    inclusion list filename
excludeListFilename = 0                 # -e    exclusion list filename          
##############################################################################
# import python libraries
import sys
import sm_libs.corpora as corpora
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
corpusDirectory, outputFilename, includeListFilename, excludeListFilename = params.output_targetDocDiversities(sys.argv[1:], corpusDirectory, outputFilename, includeListFilename, excludeListFilename)

# import the information
theCorpus = corpora.corpus()
theCorpus.importCorpusInfo(corpusDirectory)
theCorpus.importTargetInfo()
theCorpus.outputDocDiversities(outputFilename, includeListFilename, excludeListFilename)


