from pydriller import RepositoryMining, GitRepository
import datetime
import re

def getSPLFeatures(listaCommits):
    features = []
    for commit in RepositoryMining('../soletta',only_commits=listaCommits).traverse_commits():
        for modification in commit.modifications:
            if('kconfig' in modification.filename.lower() and modification.change_type.value == 5):
                currentSourceCode = modification.source_code.replace('\t','').strip().split('\n')
                for line in currentSourceCode:
                    res = re.match(r'^config \S+', line)
                    if((res != None) and not(line.split()[1] in features)):
                        features.append(line.split()[1])
    return features

