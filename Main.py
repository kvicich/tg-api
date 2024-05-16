from telethon import TelegramClient, events
import asyncio

async def main():
    # Read api_id and api_hash from files
    with open('api_id.txt', 'r') as f:
        api_id = int(f.read().strip())

    with open('api_hash.txt', 'r') as f:
        api_hash = f.read().strip()

    async with TelegramClient('anon', api_id, api_hash) as client:
        # Replace 'user_id' with the actual ID of the user
        user_id = 1291888924  # Example user ID
        while True:
            await client.send_message(user_id, 'Райзен какашка')
            await client.send_message(user_id, 'Райзен какашка')
            await asyncio.sleep(30)

# Run the main function
asyncio.run(main())
