import os
import logging
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis do arquivo .env
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL = os.getenv("CHANNEL")

# Crie uma sessão com sua conta de usuário
client = TelegramClient("session_name", API_ID, API_HASH)


async def main():
    # Conecta ao cliente
    await client.start(phone=PHONE_NUMBER)

    # Obtém o canal
    channel = await client.get_entity(CHANNEL)

    # Lista para armazenar IDs das mensagens
    message_ids = []
    total_deleted = 0

    async for message in client.iter_messages(channel):
        if message.file:  # Apaga apenas mensagens que têm arquivos
            message_ids.append(message.id)

            # Se atingir 100 mensagens, apaga em lote
            if len(message_ids) == 100:
                await client.delete_messages(channel, message_ids)
                total_deleted += len(message_ids)
                message_ids.clear()  # Limpa a lista após a exclusão
                await asyncio.sleep(1)  # Delay de 1 segundo entre as exclusões em lote

    # Apaga quaisquer mensagens restantes que não foram apagadas em lote
    if message_ids:
        await client.delete_messages(channel, message_ids)
        total_deleted += len(message_ids)

    logging.info(
        f"{total_deleted} mensagens com arquivos foram apagadas do canal {CHANNEL}."
    )


# Executa a função principal
with client:
    client.loop.run_until_complete(main())
