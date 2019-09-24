from pydriller import RepositoryMining, GitRepository
import datetime
import re

def getSPLFeatures(listaCommits):
    features = []
    for commit in RepositoryMining('../soletta',only_commits=listaCommits).traverse_commits():
        for modification in commit.modifications:
            if('kconfig' in modification.filename.lower() and modification.change_type.value == 5):
                for line in modification.source_code:
                    res = re.match(r'^config \S+', line)
                    if((res != None) and not(res.split(' ')[1] in features)):
                        features.append(line)
    return features

