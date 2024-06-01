import time
import asyncio
import random
from datetime import datetime, timedelta
from telethon import TelegramClient

# Чтение api_id и api_hash из файлов
with open('api_id.txt', 'r') as file1:
    api_id = file1.read().strip()

with open('api_hash.txt', 'r') as file2:
    api_hash = file2.read().strip()

# Определение категорий и их файлов
categories_files = {
    'Рандомные фразы': 'citati.txt'
}

# Чтение данных для каждой категории из соответствующих файлов
categories_data = {}
for category, filename in categories_files.items():
    with open(filename, 'r') as file:
        categories_data[category] = [line.strip() for line in file]

client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Печать всех диалогов/разговоров
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    # Получение списка контактов
    contacts = []
    async for dialog in client.iter_dialogs():
        contacts.append(dialog)
    
    # Фильтрация личных контактов (исключение каналов, групп и ботов)
    personal_contacts = [
        contact for contact in contacts 
        if contact.is_user and contact.entity and not str(contact.id).startswith('-') and 'bot' not in (contact.entity.username or '').lower()
        and contact.id != 1567704438
    ]
    
    # Проверка на наличие достаточно личных контактов
    if len(personal_contacts) < 3:
        print("Не достаточно контактов для выбора.")
        return

    # Выбор трех случайных личных контактов
    chosen_contacts = random.sample(personal_contacts, 3)
    print('\n\n\n')
    print(chosen_contacts)

    for i, contact in enumerate(chosen_contacts, 1):
        print(f"Выбран контакт: {contact.name} с ID {contact.id}")

    # Определение времени отправки сообщения - 1 июня 00:00:00
    current_year = datetime.now().year
    target_time = datetime(current_year, 6, 1, 0, 0, 0)
    if datetime.now() > target_time:
        target_time = datetime(current_year + 1, 6, 1, 0, 0, 0)
    
    # Задержка до нужного времени
    await asyncio.sleep((target_time - datetime.now()).total_seconds())

    for i, contact in enumerate(chosen_contacts, 1):
        # Генерация случайных категорий и данных
        random_category = random.choice(list(categories_data.keys()))
        random_data = random.choice(categories_data[random_category])

        # Генерация сообщения
        message = (
            f"Питухончик решил поздравить вас с летом, вы {i} участник из 3 выбранных\n\n"
            f"Рандомная хрень:\n"
            f"Категория: {random_category}\n"
            f"Сама хрень: {random_data}\n\n"
        )
        
        # Отправка сообщения контакту
        await client.send_message(contact.id, message)

# Запуск клиента и выполнение основной функции
with client:
    client.loop.run_until_complete(main())
