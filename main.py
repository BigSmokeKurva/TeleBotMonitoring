from telethon.sync import TelegramClient, events
from threading import Thread
from time import sleep
import json


class Config:
    with open('config.json', encoding="utf-8") as json_file:
        data = json.load(json_file)
        #print(data)

        name = data["name"]
        api_id = int(data["api_id"])
        api_hash = data["api_hash"]
        owner = data["owner"]
        hooks = data["hooks"]
        send_owner = True if data["send_owner"] == "True" else False
        send_sender = True if data["send_sender"] == "True" else False
        sleep_time = int(data["sleep_time"])


config = Config
no_send_ids_temp = {}
time = 0


def timer():
    global time, no_send_ids_temp
    while True:
        for id in [i for i in no_send_ids_temp.keys()]:
            if no_send_ids_temp[id] == time:
                del no_send_ids_temp[id]
        time += 1
        sleep(1)


with TelegramClient(config.name, config.api_id, config.api_hash) as client:
    @client.on(events.NewMessage())
    async def handler(event):
        sender = await event.get_sender()
        if sender.id not in no_send_ids_temp:
            message = event.message.message
            for key in config.hooks.keys():
                if key in message.lower():
                    if config.send_owner:
                        await client.send_message(entity=config.owner, message=f"@{sender.username}:\n{message}")
                    if config.send_sender:
                        await client.send_message(entity=sender.id, message=config.hooks[key])
                    no_send_ids_temp[event.sender_id] = time + config.sleep_time
                    break

    Thread(target=timer, args=()).start()
    client.run_until_disconnected()
