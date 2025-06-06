import json
from   models.user import User

# carregar os arquivos json
with open("sistema-cursos-programacao\\backend_sistema_cursos\\data\\users.json", "r", encoding="utf=8") as file:
    data = json.load(file) # transforma os dados do JSON em uma lista de dict Python 
    
#criar objetos user a partir dos dados
users_ = [User.from_dict(u) for u in data] # Para cada dict u na lista data, você usa User.from_dict() para transformar em um obj

# exibit todos os usuarios

for user in users_:
    print(user)

#add novo dict
new_user = User("003", "Carlos Nunes", "carlos@gmail.com", "senha123", "admin")
# Verifica se o email já existe
if not any(u.email == "carlos@gmail.com" for u in users_):
    users_.append(new_user)


# salvar todos os users de volta ao json
with open("sistema-cursos-programacao\\backend_sistema_cursos\\data\\users.json", "w", encoding="utf=8") as file: #Converte cada obj User da lista users_ para dicionário com to_dict()
    json.dump([u.to_dict() for u in users_], file, indent=4)#Salva a nova lista no JSON com identação de 4 espaços