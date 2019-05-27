from pydriller import RepositoryMining, GitRepository
import datetime
from splclassifier import SPLClassifier

dt1 = datetime.datetime(2017, 3, 8, 0, 0, 0)
dt2 = datetime.datetime(2017, 12, 31, 0, 0, 0)

repositorio = ''

GR = GitRepository('../soletta')

for commit in RepositoryMining('../soletta',single='2c727429e244c074a45c0d99b8ba57ad7fb6df36').traverse_commits():
    print('Hash {}, author {}'.format(commit.hash, commit.author.name))
    print('\nModificações do commit: {}\n'.format(commit.hash))
    for modification in commit.modifications:
        files_changing_tags = []
        if(modification.filename.lower() == 'kconfig' and modification.change_type.value == 5):
            # print('Author {} modified {} in commit {}'.format(commit.author.name, modification.filename, commit.hash))
            # print("Diff do arquivo {}".format(modification.filename))
            diff = modification.diff
            parsed_lines = GR.parse_diff(diff)
            added = parsed_lines['added']
            removed = parsed_lines['deleted']
            classifier = SPLClassifier(added,removed)
            print("Added:\n")
            print(classifier.added)
            print("Removed:\n")
            print(classifier.removed)
            print("Resultado:\n")
            print(classifier.classify())


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