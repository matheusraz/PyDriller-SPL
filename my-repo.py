from pydriller import RepositoryMining

for commit in RepositoryMining('https://github.com/matheusraz/elasticNodeJS.git').traverse_commits():
    print('Hash {}, author {}'.format(commit.hash, commit.author.name))
    print('\nModificações do commit: {}\n'.format(commit.hash))
    for modification in commit.modifications:
        print('Author {} modified {} in commit {}'.format(commit.author.name, modification.filename, commit.hash))

# for commit in RepositoryMining('https://github.com/matheusraz/elasticNodeJS.git').traverse_commits():
#     for mod in commit.modifications:
#         print('{} has complexity of {}, and it contains {} methods'.format(
#               mod.filename, mod.complexity, len(mod.methods)))