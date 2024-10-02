import asyncio
import os

from telethon.errors import FloodWaitError

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, DEVS
from userbot.utils import edit_delete, edit_or_reply, man_cmd

# File untuk menyimpan blacklist GCAST
BLACKLIST_FILE = "blacklist_gcast.txt"

# Fungsi untuk menambah atau membaca dari file blacklist
def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "r") as file:
            return [line.strip().split(' ', 1) for line in file.readlines()]
    return []

def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, "w") as file:
        for group_id, group_name in blacklist:
            file.write(f"{group_id} {group_name}\n")

@man_cmd(pattern="gcast(?: |$)(.*)")
async def gcast(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await edit_delete(event, "**Berikan Sebuah Pesan atau Reply**")
    kk = await edit_or_reply(event, "`Globally Broadcasting Msg...`")
    er = 0
    done = 0
    blacklist = [int(group_id) for group_id, _ in load_blacklist()]
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            if chat not in blacklist:
                try:
                    await event.client.send_message(chat, msg)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWaitError as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg)
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **Grup, Gagal Mengirim Pesan Ke** `{er}` **Grup**"
    )


@man_cmd(pattern="gucast(?: |$)(.*)")
async def gucast(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await edit_delete(event, "**Berikan Sebuah Pesan atau Reply**")
    kk = await edit_or_reply(event, "`Globally Broadcasting Msg...`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            if chat not in DEVS:
                try:
                    await event.client.send_message(chat, msg)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWaitError as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg)
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **chat, Gagal Mengirim Pesan Ke** `{er}` **chat**"
    )


@man_cmd(pattern="blchat$")
async def show_blacklist(event):
    blacklist = load_blacklist()
    if blacklist:
        bl_list = "\n".join([f"ID: {group_id}, Nama: {group_name}" for group_id, group_name in blacklist])
        await edit_or_reply(
            event,
            f"🔮 **Blacklist GCAST:** `Enabled`\n\n📚 **Blacklist Group:**\n{bl_list}\n\nKetik `.addblacklist` di grup yang ingin anda tambahkan ke daftar blacklist gcast."
        )
    else:
        await edit_delete(event, "🔮 **Blacklist GCAST:** `Disabled`")


@man_cmd(pattern="addbl(?:\\s|$)([\\s\\S]*)")
async def add_to_blacklist(event):
    xxnx = await edit_or_reply(event, "`Processing...`")
    gc = event.chat_id
    group_name = (await event.get_chat()).title

    blacklist = load_blacklist()

    if any(gc == int(group_id) for group_id, _ in blacklist):
        await xxnx.edit(f"**Grup ini sudah ada di blacklist GCAST.**")
        return
    
    blacklist.append((str(gc), group_name))
    save_blacklist(blacklist)

    await xxnx.edit(
        f"**Berhasil Menambahkan** `{group_name}` **(ID: {gc}) ke daftar blacklist gcast.**"
    )


@man_cmd(pattern="delbl(?:\\s|$)([\\s\\S]*)")
async def remove_from_blacklist(event):
    xxnx = await edit_or_reply(event, "`Processing...`")
    gc = event.chat_id

    blacklist = load_blacklist()

    new_blacklist = [entry for entry in blacklist if int(entry[0]) != gc]
    if len(new_blacklist) == len(blacklist):
        await edit_delete(xxnx, "**Grup ini tidak ada dalam daftar blacklist gcast.**")
        return

    save_blacklist(new_blacklist)
    await xxnx.edit(f"**Berhasil Menghapus grup dari daftar blacklist gcast.**")


@man_cmd(pattern="listbl$")
async def list_blacklist(event):
    blacklist = load_blacklist()
    if blacklist:
        bl_list = "\n".join([f"ID: {group_id}, Nama: {group_name}" for group_id, group_name in blacklist])
        await edit_or_reply(
            event,
            f"📚 **Blacklist Group List:**\n{bl_list}"
        )
    else:
        await edit_delete(event, "🔮 **Tidak ada grup di blacklist.**")

CMD_HELP.update(
    {
        "gcast": f"**Plugin : **`gcast`\
        \n\n  •  **Syntax :** `{cmd}gcast` <text/reply media>\
        \n  •  **Function : **Mengirim Global Broadcast pesan ke seluruh grup yang kamu masuk. (Bisa mengirim media/sticker)\
        \n\n  •  **Syntax :** `{cmd}blchat`\
        \n  •  **Function : **Untuk mengecek informasi daftar blacklist gcast.\
        \n\n  •  **Syntax :** `{cmd}addblacklist`\
        \n  •  **Function : **Untuk menambahkan grup tersebut ke blacklist gcast.\
        \n\n  •  **Syntax :** `{cmd}delblacklist`\
        \n  •  **Function : **Untuk menghapus grup tersebut dari blacklist gcast.\
        \n\n  •  **Syntax :** `{cmd}listbl`\
        \n  •  **Function : **Menampilkan daftar grup yang ada dalam blacklist beserta nama dan ID grupnya.\
    "
    }
)

CMD_HELP.update(
    {
        "gucast": f"**Plugin : **`gucast`\
        \n\n  •  **Syntax :** `{cmd}gucast` <text/reply media>\
        \n  •  **Function : **Mengirim Global Broadcast pesan ke seluruh private chat (PC) yang masuk. (Bisa mengirim media/sticker)\
    "
    }
)
