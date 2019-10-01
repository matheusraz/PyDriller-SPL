import re

teste = 'depends on HAVE_NODEJS'

# st = 'select \"teste so vai\"'
st = 'select n'
st2 = 'I would like to select any values'

# res = re.match(r'^select \S+', st2)  SELECT           *
# res = re.match(r'^depends on \S+', teste) DEPENDS     *
# res = re.match(r'^default \S', teste) DEFAULT         *
# res = re.match(r'^menu \"w+\"', st) MENU              *
# res = re.match(r'^config \S+', teste) FEATURE         *
# res = re.match(r'^bool \"w+\"', st) BOOL              *
# res = re.match(r'^prompt \"w+\"', st) PROMPT          *
# res = re.match(r'^option \"w+\"', st) OPTION          *
# print(res != None)

# Mapping (mapeamento)
# ifdef
# build

# --------------- MAPPING ---------------
# dale = 'obj-core-$(MAINLOOP_GLIB)-extra-cflags += $(GLIB_CFLAGS)'
# res = re.match(r'^\S* := \S*', dale)
# res2 = re.match(r'^\S* \+= \S*', dale)
# if(res != None or res2 != None):
#     print('MAPPING')

# --------------- IFDEF ---------------
# dale = 'ifdef LINUX'
# res = re.match(r'^ifeq \S*', dale)
# res2 = re.match(r'^ifneq \S*', dale)
# res3 = re.match(r'^ifdef \S*', dale)
# if(res != None or res2 != None or res3 != None):
#     print('IFDEF')

dale = 'adfadf-$(KDBUS)-asdfasdfa += asdhfisadhflaskjdf'
result = re.search(r'\S*\$\((.*)\)\S* \+= \S*', dale)
if(result):
    print(result.group(1))





# obj-core-$(KDBUS)-extra-cflags := $(SYSTEMD_CFLAGS) -- ANTES
                                                    # -- MappingA
# obj-core-$(KDBUS)-extra-cflags := $(TESTE) -- DEPOIS

# Mapping - X := / += Y






# depends on HAVE_NODEJS

