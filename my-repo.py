from pydriller import RepositoryMining, GitRepository
import datetime

dt1 = datetime.datetime(2017, 3, 8, 0, 0, 0)
dt2 = datetime.datetime(2017, 12, 31, 0, 0, 0)

GR = GitRepository('../soletta')

for commit in RepositoryMining('../soletta',since=dt1,to=dt2,filepath="Kconfig").traverse_commits():
    print('Hash {}, author {}'.format(commit.hash, commit.author.name))
    print('\nModificações do commit: {}\n'.format(commit.hash))
    for modification in commit.modifications:
        if(modification.filename.lower() == 'kconfig' and modification.change_type.value == 5):
            print('Author {} modified {} in commit {}'.format(commit.author.name, modification.filename, commit.hash))
            print("Diff do arquivo {}".format(modification.filename))
            diff = modification.diff
            parsed_lines = GR.parse_diff(diff)
            print("Arquivo após mods:\n")
            # print(modification.source_code)
            lista = modification.source_code.split('\n')
            qtdEmptyLines = 0
            # Conta quantas linhas há em branco e tira espaço e \t de todas as linhas do arquivo
            for i in range(len(lista)):
                if(lista[i].strip() == ''):
                    qtdEmptyLines += 1
                lista[i] = lista[i].strip()
            # Remove linha em branco
            for i in range(qtdEmptyLines):
                lista.remove('')
            print(len(lista))
            print(modification.nloc)
            print(lista)
            print("Linhas adicionadas:\n")
            print(parsed_lines['added'])
            print('Linhas removidas:\n')
            print(parsed_lines['deleted'])
