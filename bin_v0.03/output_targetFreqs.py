##############################################################################
# default parameters
corpusDirectory = 0                     # -c    the directory containing the corpus
outputFilename = "freqs.txt"            # -o    output filename that will be created
includeListFilename = 0                 # -i    inclusion list filename
excludeListFilename = 0                 # -e    exclusion list filename
sortByFreq = 0                          # -s    whether you want to output the words in frequency order
partsPerMillion = 0                     # -p    whether you want to output the targets' freqs as ppm: 1000000*(freq/numTokens)
logged = 0                              # -l    whether you want to output the values as log10 freqs            
##############################################################################
# import python libraries
import sys
import sm_libs.corpora as corpora
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
corpusDirectory, outputFilename, includeListFilename, excludeListFilename, sortByFreq, partsPerMillion, logged = params.output_targetFreqs(sys.argv[1:], corpusDirectory, outputFilename, includeListFilename, excludeListFilename, sortByFreq, partsPerMillion, logged)

# import the information
theCorpus = corpora.corpus()
theCorpus.importCorpusInfo(corpusDirectory)
theCorpus.importTargetInfo()
theCorpus.outputFreqs(outputFilename, includeListFilename, excludeListFilename, sortByFreq, partsPerMillion, logged)


