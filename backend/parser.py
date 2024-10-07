import json
from pymongo import MongoClient
from dataclasses import dataclass
from datetime import datetime
from config import Config

client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
db = client[Config.MONGO_DB_NAME]
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

def import_data():
    with open('udata.json') as f:  
        data = json.load(f)
        
        users_data = data.get('users', [])
        
        users = []
        for item in users_data:
            if isinstance(item, dict):
                if collection.find_one({'username': item.get('user')}):
                    print(f'Usuário {item.get("user")} já existe no banco de dados. Pulando...')
                    continue
                user = User(
                    username=item.get('user'), 
                    password=item.get('password'),
                    roles=parse_roles(item),  
                    preferences=UserPreferences(item.get('user_timezone')).__dict__,  
                    active=item.get('is_user_active', True),
                    created_ts=parse_created_at(item.get('created_at'))  
                )
                users.append(user.__dict__)  

        # Inserir os dados no MongoDB
        if users:
            collection.insert_many(users)
            print(f'{len(users)} usuários importados com sucesso!')
        else:
            print('Nenhum dado de usuário foi importado.')

if __name__ == "__main__":
    import_data()
