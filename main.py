from os import system, name, path
from random import choice
from asyncio import run
from requests import get
from telethon import TelegramClient, errors, functions, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.tl.functions.channels import UpdateUsernameRequest, DeleteChannelRequest, CreateChannelRequest
from bs4 import BeautifulSoup as S
from telebot import TeleBot
from datetime import datetime

token = "6688042392:AAHCEQ1s1BUms3vxFhgo9-jf7Vsl30qI9N0" # توكنك
id = "1958060577" # ايديك

sessionL = input('[+] Enter Session : ')
client = TelegramClient(StringSession(sessionL), "25324581", "08feee5eeb6fc0f31d5f2d23bb2c31d0").start()

def usernames():
    k = ''.join(choice('qwertyuiopasdfghjklzxcvbnm') for i in range(1))
    n = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    c = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    z = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    g = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    _ = ''.join("_")
    e = ''.join(choice('qwertyuiopasdfghjklzxcvbnm') for i in range(1))
    u1 = k + c + e + e + e
    u2 = k + z + z + z + n
    u3 = k + k + k + n + c
    s = u1,u2,u3
    return choice(s)

async def channels2(username):
    async for chat in client.iter_dialogs():
        if chat.name == f'[ {username} ]' and not chat.entity.username:
            await client(DeleteChannelRequest(channel=chat.entity))
            print('- Flood : ' + username + ' .')
            return False
    return True

async def fragment(username):
    try:
        ok = get(url=f'https://fragment.com/username/{username}').text
        if "An auction to get the Telegram" in ok or "Telegram and secure your ownership" in ok or "Check the current availability of" in ok:
        	return True
        elif "Secure your name with blockchain in an ecosystem of 700+ million users" in ok:
        	await fragment(username)
        elif "is taken" in ok:
        	return "is taken"
        else:
        	return False
    except: await fragment(username=username) 

async def telegram(claim, username):
    global token, id
    if claim:
        text = f"⌯ Done UserName\n⌯ UserName : @{username} .\n⌯ Date : {datetime.now().strftime('%H:%M:%S')}"
    else:
        text = f"⌯ New UserName Flood\n⌯ UserName : @{username} .\n⌯ Date : {datetime.now().strftime('%H:%M:%S')}"
    try:
        TeleBot(token=token).send_message(id, text=text)
    except Exception:
        pass
    await client.send_message('me', text)

async def claimed(username):
    result = await client(CreateChannelRequest(
                title=f'Claim [ {username} ]',
        about=f'IG : @9f05 , Tele : @skrawi',
        megagroup=False))
    try:
        await client(UpdateUsernameRequest(channel=result.chats[0], username=username))
        await client.send_message(username, f"⌯ Done UserName\n⌯ UserName : @{username} .\n⌯ Date : {datetime.now().strftime('%H:%M:%S')}.\n⌯ UserName Person : @skrawi")
        return True
    except Exception as e:
        await client.send_message("me", f'⌯ Error Message .\nMessage : {e} .')
        return False

async def checker(username):
    try:
        check = await client(CheckUsernameRequest(username=username))
        if check:
            print('- Available : ' + username + ' .')
            claimer = await claimed(username)
            claim = claimer and (await fragment(username)) == "is taken"
            print('- Claimer ? ' + str(claim) + '\n' + '_ ' * 20)
            flood = await channels2(username)
            if not flood:
                with open('flood.txt', 'a') as floodX: floodX.write(username + "\n")
            else:
                print('- Taken : ' + username + ' .')
            await telegram(claim, username)
    except errors.rpcbaseerrors.BadRequestError:
        print('- Banned : ' + username + ' .')
        with open("banned4.txt", "a") as file:
            file.write(username + '\n')
    except errors.FloodWaitError as timer:
        print(f'- Flood Account [ {timer.seconds} Seconds ] .')
    except errors.UsernameInvalidError:
        print('- Error : ' + username + ' .')

async def start(username):
    try:
        ok = await fragment(username)
    except:
        return
    try:
        if not ok:
            await checker(username)
        elif ok == "is taken":
            print('- Taken : ' + username + ' .')
        else:
            print('- Fragment : ' + username + ' .')
            with open("fragment.txt", "a") as frag_file:
                frag_file.write(username + '\n')
    except Exception as e:
        print(e)

@client.on(events.NewMessage(pattern=r'/.فحص'))
def Cstatus(event):
    event.reply("الفحص شغال الان")

async def main():
    print("h")
    print("z")
    if not path.exists('banned4.txt'): open('banned4.txt', 'w').close()
    if not path.exists('flood.txt'): open('flood.txt', 'w').close()
    if not path.exists('fragment.txt'): open('fragment.txt', 'w').close()

    while True:
        username = usernames()
        file1 = open('banned4.txt', 'r').read() or ''
        file2 = open('fragment.txt', 'r').read() or ''
        if username in file1:
            print('- Banned : ' + username + ' .')
            continue
        if username in file2:
            print('- Fragment : ' + username + ' .')
            continue
        await start(username)

run(main())
