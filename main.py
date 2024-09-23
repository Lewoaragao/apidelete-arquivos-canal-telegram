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
    lote_count = 0  # Contador de lotes

    async for message in client.iter_messages(channel):
        # Descomentar essa linha para apagar apenas mensagens que têm arquivos
        if message.file:
	# Descomentar essa linha para apagar todos os tipos de mensagens
        # if message:
            message_ids.append(message.id)

            # Se atingir 100 mensagens, apaga em lote
            if len(message_ids) == 100:
                lote_count += 1
                await client.delete_messages(channel, message_ids)
                total_deleted += len(message_ids)
                
                logging.info(f"Lote {lote_count} apagou 100 mensagens. Total até agora: {total_deleted} mensagens apagadas.")
                
                message_ids.clear()  # Limpa a lista após a exclusão
                await asyncio.sleep(5)  # Delay de 5 segundos entre as exclusões em lote

    # Apaga quaisquer mensagens restantes que não foram apagadas em lote
    if message_ids:
        lote_count += 1
        await client.delete_messages(channel, message_ids)
        total_deleted += len(message_ids)
        
        logging.info(f"Lote {lote_count} apagou {len(message_ids)} mensagens restantes. Total até agora: {total_deleted} mensagens apagadas.")

    logging.info(
        f"{total_deleted} mensagens foram apagadas no total do canal {CHANNEL}."
    )


# Executa a função principal
with client:
    client.loop.run_until_complete(main())
