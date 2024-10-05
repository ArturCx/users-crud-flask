import json
from pymongo import MongoClient
from dataclasses import dataclass
from datetime import datetime

# Conecte-se ao MongoDB
client = MongoClient("localhost", 27017)
db = client['user_database']
collection = db['users']

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool
    created_ts: float

# Mapeamento de roles (a partir dos campos is_user_admin, is_user_manager, etc.)
def parse_roles(item):
    roles = []
    if item.get('is_user_admin'):
        roles.append('admin')
    if item.get('is_user_manager'):
        roles.append('manager')
    if item.get('is_user_tester'):
        roles.append('tester')
    return roles

# Função para converter a data no formato ISO para timestamp
def parse_created_at(created_at_str):
    return datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M:%SZ').timestamp()

# Carregar dados do JSON
def import_data():
    with open('udata.json') as f:  
        data = json.load(f)  # Carregando o arquivo JSON
        
        users_data = data.get('users', [])  # Obtém a lista de usuários a partir da chave 'users'
        
        users = []
        for item in users_data:
            # Certifique-se de que 'item' é um dicionário e possui os campos corretos
            if isinstance(item, dict):
                user = User(
                    username=item.get('user'),  # 'user' no JSON
                    password=item.get('password'),
                    roles=parse_roles(item),  # Faz o parsing das roles
                    preferences=UserPreferences(item.get('user_timezone')).__dict__,  # 'user_timezone' no JSON
                    active=item.get('is_user_active', True),  # 'is_user_active' no JSON
                    created_ts=parse_created_at(item.get('created_at'))  # Converter a data para timestamp
                )
                users.append(user.__dict__)  # Converte o dataclass para dict

        # Inserir os dados no MongoDB
        if users:
            collection.insert_many(users)
            print(f'{len(users)} usuários importados com sucesso!')
        else:
            print('Nenhum dado de usuário foi importado.')

if __name__ == "__main__":
    import_data()
