"""
Скрипт для загрузки кода на GitHub через API
Замените GITHUB_TOKEN на ваш персональный токен GitHub
(Settings → Developer settings → Personal access tokens)
"""

import os
import requests
import base64


def get_github_token():
    """Получение GitHub токена"""
    token = input("Введите ваш GitHub Personal Access Token: ")
    return token


def get_all_files(directory):
    """Получение всех файлов в директории"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if '.git' not in filepath:  # Исключаем .git папку
                files.append(filepath)
    return files


def upload_file_to_github(file_path, github_token, branch='main'):
    """Загрузка одного файла на GitHub"""
    
    # Чтение файла
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Преобразование пути относительно корня репозитория
    rel_path = os.path.relpath(file_path, '.')
    
    # SHA файла (заполним пустым, он вычислится при загрузке нового файла)
    sha = None
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Сначала проверяем существует ли файл
    url = f"https://api.github.com/repos/lolybox/tg-avito-bot/contents/{rel_path}?ref={branch}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        sha = data.get('sha')
        print(f"✓ Файл существует: {rel_path}")
    elif response.status_code == 404:
        print(f"• Новый файл: {rel_path}")
    
    # Загрузка файла
    if sha:
        # Обновление существующего файла
        url = f"https://api.github.com/repos/lolybox/tg-avito-bot/contents/{rel_path}"
    else:
        # Создание нового файла
        url = f"https://api.github.com/repos/lolybox/tg-avito-bot/contents/{rel_path}"
    
    params = {
        "message": f"Update {rel_path}",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch
    }
    
    if sha:
        params["sha"] = sha
    
    response = requests.put(url, json=params, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ Успешно загружен: {rel_path}")
        return True
    else:
        print(f"❌ Ошибка загрузки {rel_path}: {response.text}")
        return False


def main():
    print("=" * 50)
    print("GitHub Code Uploader")
    print("=" * 50)
    print()
    
    # Получаем токен
    github_token = get_github_token()
    if not github_token:
        print("Ошибка: Токен не указан!")
        return
    
    # Получаем все файлы
    print("\nПоиск файлов...")
    files = get_all_files('.')
    print(f"Найдено {len(files)} файлов\n")
    
    # Загружаем каждый файл
    success_count = 0
    failed_count = 0
    
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Загрузка: {file_path}")
        
        if upload_file_to_github(file_path, github_token):
            success_count += 1
        else:
            failed_count += 1
        
        # Пауза между запросами (чтобы не превысить лимиты API)
        import time
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print(f"Готово! Загружено файлов: {success_count} из {len(files)}")
    if failed_count > 0:
        print(f"⚠️ Ошибок: {failed_count}")
    print("=" * 50)


if __name__ == "__main__":
    main()
