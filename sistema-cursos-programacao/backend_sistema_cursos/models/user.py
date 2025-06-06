#informações obrigatorias do usuario
class User:
    def __init__(self,id, name, email, password, type): # serve para armazenar todos os dados das variaveis internas
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.type = type # exemplo -aluno, instrutor, admin
    
    def setId(self,id): # todos esses servem para alteração de dados do usuário depois que o proprio ja foi criadoo
        self.id = id   
     
    def setName(self,name):
        self.name = name
    
    def setEmail(self,email):
        self.email = email
        
    def setPassword(self, password):
        self.password = password
    
    def setType(self, type):
        self.type = type
        
    def to_dict(self): # converte o user em dict - dicionario, para poder salvar com json
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "type": self.type
        }
        
    @staticmethod
    def from_dict(data): # recebe dicionario de user.json e retorna um Obj User com base no que recebeu
        return User(
            data["id"],
            data["name"],
            data["email"],
            data["password"],
            data["type"]
        )
        
    def __str__(self): # apenas para mostrar o obj com facilidade com o print (exemplo comentado abaixo)
        return f"Usuário: {self.name} ({self.email}) - Tipo: {self.type}"
    
""""u = User("001", "João", "joao@email.com", "1234", "aluno")
print(u)  # Usuário: João (joao@email.com) - Tipo: aluno
print(u.to_dict()) #sairia exatamente como está no to_dict"""
