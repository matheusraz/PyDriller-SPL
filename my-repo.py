import sys
from pydriller import RepositoryMining, GitRepository
import datetime
from splclassifier import SPLClassifier
from manualcommits import getManualResultsKconfig, getMakeFileResultsManual, getAMFileResultsManual
from features import getSPLFeatures
import re

dt1 = datetime.datetime(2017, 3, 8, 0, 0, 0)
dt2 = datetime.datetime(2017, 12, 31, 0, 0, 0)

repositorio = ''

GR = GitRepository('../soletta')

# KCONFIG EXAMPLES
# d458061abec39e7a0693c49f96b7ab3378c157d9 - only Removeds
# 2c727429e244c074a45c0d99b8ba57ad7fb6df36 - both (add at final)
# da5f77ff470f49e90797db27a8923c988c099e96 - replace inside file
# 9110b309393ec27dee35baf23d1cbefe1a796d8f -

# MAKEFILE EXAMPLES
# 17022a2622ddce9fbbd478a551f46e639d991cb0
# e6e17e41bbeb92125541c9cc4c06273ef1566c22
# ec6c506d1e926efa1007e9b5946d57a5e3f3804a
# 3e677dd8f3c6427a861a36f139f49c814f5dad88 FUDEU!!!!!! (REVER)
# 0c45273fb09534946b704fea99f64c7acbb14eea

fileKind = sys.argv[1]
listaCommitsKconfig = getManualResultsKconfig()
listaCommitsMakeFile = getMakeFileResultsManual()
listaCommitsAM = getAMFileResultsManual()
if(fileKind == 'makefile'):
    listaCommits = listaCommitsMakeFile
elif(fileKind == 'kconfig'):
    listaCommits = listaCommitsKconfig
else:
    listaCommits = listaCommitsAM
listaCommitResults = ['Hash,author,KC-Tags,MF-Tags,AM-Tags\n']
features = getSPLFeatures(listaCommits)


# for commit in RepositoryMining('../soletta',single='fa7f6e4c8099e18ec7381605e392a6c8cdf24cf2').traverse_commits():
for commit in RepositoryMining('../soletta',only_commits=listaCommits).traverse_commits():
    print(commit.hash)
    kconfig_commit_tags = []
    makefile_commit_tags = []
    am_commit_tags = []
    commitResults = []
    for modification in commit.modifications:
        files_changing_tags = []
        if(('kconfig' in modification.filename.lower() or 'makefile' in modification.filename.lower())):
            diff = modification.diff
            parsed_lines = GR.parse_diff(diff)
            added = parsed_lines['added']
            removed = parsed_lines['deleted']
            file_source_code = modification.source_code.split('\n')
            classifier = SPLClassifier(added, removed, file_source_code)
            files_changing_tags = classifier.classify(modification.filename.lower(),features)
        else:
            if(modification.change_type.value != 1 and modification.change_type.value != 4):
                diff = modification.diff
                parsed_lines = GR.parse_diff(diff)
                added = parsed_lines['added']
                removed = parsed_lines['deleted']
                file_source_code = modification.source_code.split('\n')
                classifier = SPLClassifier(added, removed, file_source_code)
                files_changing_tags = classifier.classify(modification.filename.lower(),features)
                files_changing_tags.append('changeAsset')
            else:
                if(modification.change_type.value == 1):
                    files_changing_tags.append('AddAsset')
                elif(modification.change_type.value == 4):
                    files_changing_tags.append('removeAsset')
        for file_tag in files_changing_tags:
            if('kconfig' in modification.filename.lower() and (file_tag not in kconfig_commit_tags)):
                kconfig_commit_tags.append(file_tag)
            elif('makefile' in modification.filename.lower() and (file_tag not in makefile_commit_tags)):
                makefile_commit_tags.append(file_tag)
            elif('kconfig' not in modification.filename.lower() and 'makefile' not in modification.filename.lower() and file_tag not in am_commit_tags):
                am_commit_tags.append(file_tag)
    if(len(kconfig_commit_tags) > 0):
        kconfig_commit_tags = str(kconfig_commit_tags).replace(',',' |')
    else:
        kconfig_commit_tags = 'no-tag-changed'
    if(len(makefile_commit_tags) > 0):
        makefile_commit_tags = str(makefile_commit_tags).replace(',',' |')
    else:
        makefile_commit_tags = 'no-tag-changed'
    if(len(am_commit_tags) > 0):
        am_commit_tags = str(am_commit_tags).replace(',',' |')
    else:
        am_commit_tags = 'no-tag-changed'
    mountStr = '{},{},{},{},{}\n'.format(commit.hash, commit.author.name, kconfig_commit_tags, makefile_commit_tags, am_commit_tags)
    listaCommitResults.append(mountStr)

arq = open('automated-results-{}.csv'.format(fileKind),'w')
arq.writelines(listaCommitResults)