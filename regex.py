import re

teste = 'depends on HAVE_NODEJS'

# st = 'select \"teste so vai\"'
st = 'select n'
st2 = 'I would like to select any values'

res = re.match(r'^select \S+', st2) # SELECT          *
# res = re.match(r'^depends on \S+', teste) DEPENDS     *
# res = re.match(r'^default \S', teste) DEFAULT         *
# res = re.match(r'^menu \"w+\"', st) MENU              *
# res = re.match(r'^config \S+', teste) FEATURE         *
# res = re.match(r'^bool \"w+\"', st) BOOL              *
# res = re.match(r'^prompt \"w+\"', st) PROMPT          *
# res = re.match(r'^option \"w+\"', st) OPTION          *
print(res != None)



# depends on HAVE_NODEJS

