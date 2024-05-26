from telethon import TelegramClient
import asyncio

async def main():
    # Read api_id and api_hash from files
    with open('api_id.txt', 'r') as f:
        api_id = int(f.read().strip())

    with open('api_hash.txt', 'r') as f:
        api_hash = f.read().strip()

    # Initialize TelegramClient
    client = TelegramClient('anon', api_id, api_hash)

    # Initialize dictionary to store dialogs
    dialogs = {}

    async with client:
        # Retrieve dialogs and store them in the dictionary
        async for dialog in client.iter_dialogs():
            dialogs[dialog.name] = dialog

        # Main loop
        while True:
            # Display dialog list
            print("Доступные чаты:")
            for i, (name, dialog) in enumerate(dialogs.items(), start=1):
                print(f"{i}. {name}")

            # Prompt for user input
            choice = await run_prompt('Выберите чат (введите номер) или введите "exit" для выхода: ')

            # Check if user wants to exit
            if choice.lower() == 'exit':
                break

            # Check if input is valid
            try:
                choice = int(choice)
                if choice not in range(1, len(dialogs) + 1):
                    raise ValueError
            except ValueError:
                print("Ошибка: Неверный выбор. Пожалуйста, введите число от 1 до", len(dialogs))
                continue

            # Get the selected dialog
            selected_dialog = list(dialogs.values())[choice - 1]

            # Enter the selected dialog
            print(f"Вы зашли в чат: {selected_dialog.name}. Для выхода введите '/exit'.")

            # Prompt for the number of messages
            num_messages = await run_prompt('Введите количество сообщений для отправки: ')

            # Validate the number of messages
            try:
                num_messages = int(num_messages)
                if num_messages <= 0:
                    raise ValueError
            except ValueError:
                print("Ошибка: Неверное количество сообщений. Пожалуйста, введите положительное число.")
                continue

            # Prompt for the message text
            message_text = await run_prompt('Введите текст сообщения: ')

            # Send the specified number of messages
            for _ in range(num_messages):
                await client.send_message(selected_dialog, message_text)
                print(f"Сообщение '{message_text}' отправлено в {selected_dialog.name}")

# Define a custom async prompt function
async def run_prompt(*args, **kwargs):
    from prompt_toolkit import PromptSession

    session = PromptSession()
    return await session.prompt_async(*args, **kwargs)

# Run the main function
asyncio.run(main())
