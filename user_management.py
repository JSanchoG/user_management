import json
import random
import string
import re
import os

FILE_USERS_PATH = "data/users.json"

if not os.path.exists("data"): os.makedirs("data")

def add_user(user_data:dict):
    '''
    Dodaje nowego użytkownika
    '''
    if not os.path.exists(FILE_USERS_PATH):
        with open(FILE_USERS_PATH, 'w') as file:
            json.dump([], file)
    
    if validate_pesel(user_data['pesel']) == True and validate_nip(user_data['nip']) == True and validate_regon(user_data['regon'] == True):       
        with open(FILE_USERS_PATH, 'r') as file:
            userData = json.load(file)
        
        userData.append(user_data)
        
        with open(FILE_USERS_PATH, 'w') as file:
            json.dump(userData, file, indent=4)

def edit_user(user_id: int, updated_data: dict) -> bool:
    """
    Edytuje dane użytkownika na podstawie user_id.

    :param user_id: ID użytkownika do edycji.
    :param updated_data: Słownik z nowymi danymi użytkownika.
    :return: True, jeśli edycja zakończona sukcesem, False w przeciwnym razie.
    """
    if not os.path.exists(FILE_USERS_PATH):
        raise FileNotFoundError(f"Plik {FILE_USERS_PATH} nie istnieje.")
    
    with open(FILE_USERS_PATH, 'r') as file:
        users = json.load(file)

    user_found = False
    for user in users:
        if user['user_id'] == user_id:
            user.update(updated_data)
            user_found = True
            break

    if not user_found: return False
    
    with open(FILE_USERS_PATH, 'w') as file:
        json.dump(users, file, indent=4)

    return True

def remove_user(user_id: int) -> bool:
    """
    Ustawia status użytkownika na 'removed' w pliku JSON na podstawie user_id.
    
    :param user_id: ID użytkownika do usunięcia
    :return: True, jeśli użytkownik został znaleziony i status został zmieniony, False w przeciwnym razie
    """
    try:
        with open(FILE_USERS_PATH, "r", encoding="utf-8") as file:
            users = json.load(file)

        user_found = False
        for user in users:
            if user["user_id"] == user_id:
                user["status"] = "removed"
                user_found = True
                break

        if user_found:
            with open(FILE_USERS_PATH, "w", encoding="utf-8") as file:
                json.dump(users, file, indent=4, ensure_ascii=False)
            return True

        return False
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd podczas przetwarzania pliku: {e}")
        return False

def validate_nip(nip:str) -> bool:
    '''
    Waliduje numer NIP
    '''
    if len(nip) != 10 or not nip.isdigit():
        return False
    
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    checksum = sum(int(digit) * weight for digit, weight in zip(nip[:9], weights)) % 11
    
    return checksum == int(nip[9])

def validate_pesel(pesel:str) -> bool:
    '''
    Waliduje numer PESEL
    '''
    if len(pesel) != 11 or not pesel.isdigit():
        return False
    
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = (sum(int(digit) * weight for digit, weight in zip(pesel[:10], weights)) % 10)
    checksum = (10 - checksum) % 10
    
    return checksum == int(pesel[10])

def validate_regon(regon:str) -> bool:
    '''
    Waliduje numer REGON
    '''
    if len(regon) not in [9, 14] or not regon.isdigit():
        return False
    
    if len(regon) == 9:
        weights = [8, 9, 2, 3, 4, 5, 6, 7]
        checksum = sum(int(digit) * weight for digit, weight in zip(regon[:8], weights)) % 11
        checksum = 0 if checksum == 10 else checksum
        return checksum == int(regon[8])
    
    if len(regon) == 14:
        if not validate_regon(regon[:9]):
            return False
        weights = [2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8]
        checksum = sum(int(digit) * weight for digit, weight in zip(regon[:13], weights)) % 11
        checksum = 0 if checksum == 10 else checksum
        return checksum == int(regon[13])

def generate_password() -> str:
    """
    Generuje silne hasło zawierające małe litery, duże litery, cyfry i znaki specjalne.
    Długość hasła wynosi co najmniej 12 znaków.
    """
    length = 12
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    password += random.choices(all_characters, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

def validate_password(password: str) -> bool:
    """
    Waliduje hasło, sprawdzając czy zawiera:
    - co najmniej 12 znaków
    - przynajmniej jedną małą literę
    - przynajmniej jedną dużą literę
    - przynajmniej jedną cyfrę
    - przynajmniej jeden znak specjalny
    """
    if len(password) < 12:
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=;`~]', password):
        return False
    return True

def load_users() -> list:
    """
    Odczytuje istniejących użytkowników z pliku JSON.
    Wyświetla informacje o użytkownikach.
    
    :return: Lista użytkowników jako obiekty słowników. Zwraca pustą listę, jeśli plik jest pusty lub nie istnieje.
    """
    try:
        with open(FILE_USERS_PATH, "r", encoding="utf-8") as file:
            users = json.load(file)
            if not users:
                print("Brak zapisanych użytkowników.")
            else:
                for user in users:
                    print(f"Użytkownik ID {user['user_id']}:")
                    for key, value in user.items():
                        print(f"  {key}: {value}")
            return users
    except FileNotFoundError:
        print("Plik z użytkownikami nie istnieje.")
        return []
    except json.JSONDecodeError:
        print("Plik zawiera nieprawidłowe dane JSON.")
        return []