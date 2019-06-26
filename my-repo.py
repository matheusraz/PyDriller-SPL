from pydriller import RepositoryMining, GitRepository
import datetime
from splclassifier import SPLClassifier
from manualcommits import getManualResults

dt1 = datetime.datetime(2017, 3, 8, 0, 0, 0)
dt2 = datetime.datetime(2017, 12, 31, 0, 0, 0)

repositorio = ''

GR = GitRepository('../soletta')

#
# d458061abec39e7a0693c49f96b7ab3378c157d9 - only Removeds
# 2c727429e244c074a45c0d99b8ba57ad7fb6df36 - both (add at final)
# da5f77ff470f49e90797db27a8923c988c099e96 - replace inside file
# 9110b309393ec27dee35baf23d1cbefe1a796d8f -

listaCommits = getManualResults()
listaCommitResults = ['Hash,author,KC-Tags,MF-Tags\n']

for commit in RepositoryMining('../soletta',only_commits=listaCommits).traverse_commits():
    # print('Hash {}, author {}'.format(commit.hash, commit.author.name))
    # print('\nModificações do commit: {}\n'.format(commit.hash))
    kconfig_commit_tags = []
    makefile_commit_tags = []
    commitResults = []
    for modification in commit.modifications:
        files_changing_tags = []
        if('kconfig' in modification.filename.lower() and modification.change_type.value == 5):
            # print('Author {} modified {} in commit {}'.format(commit.author.name, modification.filename, commit.hash))
            # print("Diff do arquivo {}".format(modification.filename))
            diff = modification.diff
            parsed_lines = GR.parse_diff(diff)
            added = parsed_lines['added']
            removed = parsed_lines['deleted']
            classifier = SPLClassifier(added,removed)
            # print("Added:\n")
            # print(classifier.added)
            # print("Removed:\n")
            # print(classifier.removed)
            # print("\nResultado:\n")
            files_changing_tags = classifier.classify()
            # print(files_changing_tags)
        for file_tag in files_changing_tags:
            if(file_tag not in kconfig_commit_tags):
                kconfig_commit_tags.append(file_tag)
    print("Commit {}".format(commit.hash))
    if(len(kconfig_commit_tags) > 0):
        kconfig_commit_tags = str(kconfig_commit_tags).replace(',',' |')
    else:
        kconfig_commit_tags = 'rename'
    if(len(makefile_commit_tags) > 0):
        makefile_commit_tags = str(makefile_commit_tags).replace(',',' |')
    else:
        makefile_commit_tags = 'no-tag-changed'
    mountStr = '{},{},{},{}\n'.format(commit.hash,commit.author.name,kconfig_commit_tags,makefile_commit_tags)    
    listaCommitResults.append(mountStr)

arq = open('automated-results.csv','w')
arq.writelines(listaCommitResults)
    


# Commit adhfaslkdgsakjdf:
#     arquivo X (mod): ("Remove", "Depends"), ("Added", "Feature")
#     arquivo Y (mod): ("Modify", "menu"), ("Remove", "Depends")

# Commit adhfaslkdgsakjdf: [("Remove", "Depends"), ("Added", "Feature"), ("Modify", "menu")]

# Teste
# menu "Bindings"	
# config USE_NODEJS	
# 	bool "Node.js bindings"	
# 	depends on HAVE_NODEJS && HAVE_NODEJS_NPM && HAVE_NODE_GYP
# 	default n
# 	help	
# 		Enable Node.js bindings
# endmenu

# if(condition1 && condition2)

# if(condiiton1){
#     if(condition2)
# }