from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from SONALI_MUSIC.utils.join_helper import is_admin

@Client.on_chat_join_request()
async def join_request_handler(client, request):
    user = request.from_user
    chat = request.chat

    try:
        members = await client.get_chat_members_count(chat.id)
    except:
        members = "Unknown"

    text = (
        "<b>ɴᴇᴡ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ 👀</b>\n\n"
        "<b>GROUP INFO</b>\n"
        f"Name: {chat.title}\n"
        f"Members: {members}\n\n"
        "<b>USER INFO</b>\n"
        f"Name: {user.first_name}\n"
        f"Mention: {user.mention}\n"
        f"Id: <code>{user.id}</code>\n"
        f"Scam: {user.is_scam}\n\n"
        '<a href="https://t.me/Ankitgupta21444">Made by DEVIL BOSS PE</a>'
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"jr_accept:{user.id}"),
            InlineKeyboardButton("🚧 Decline", callback_data=f"jr_decline:{user.id}")
        ]
    ])

    await client.send_message(
        chat.id,
        text,
        reply_markup=keyboard,
        parse_mode="html"
    )


@Client.on_callback_query(filters.regex("^jr_"))
async def join_request_buttons(client, cq):
    action, user_id = cq.data.split(":")
    user_id = int(user_id)

    if not await is_admin(client, cq.message.chat.id, cq.from_user.id):
        return await cq.answer("Only admins can use this!", show_alert=True)

    if action == "jr_accept":
        await client.approve_chat_join_request(cq.message.chat.id, user_id)
        await cq.message.edit(f"✅ User <code>{user_id}</code> approved.", parse_mode="html")

    elif action == "jr_decline":
        await client.decline_chat_join_request(cq.message.chat.id, user_id)
        await cq.message.edit(f"🥱 User <code>{user_id}</code> declined.", parse_mode="html")


@Client.on_message(filters.command("acceptall") & filters.group)
async def accept_all(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("Only admins can use this!")

    reqs = await client.get_chat_join_requests(message.chat.id)
    count = 0
    for r in reqs:
        await client.approve_chat_join_request(message.chat.id, r.from_user.id)
        count += 1

    await message.reply(f"✅ Approved {count} users.")


@Client.on_message(filters.command("acceptuser") & filters.group)
async def accept_user(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("Only admins can use this!")

    if len(message.command) < 2:
        return await message.reply("Usage: /acceptuser <user_id>")

    user_id = int(message.command[1])
    await client.approve_chat_join_request(message.chat.id, user_id)
    await message.reply(f"🥳 User `{user_id}` approved.")


@Client.on_message(filters.command("decline") & filters.group)
async def decline_user(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("Only admins can use this!")

    if len(message.command) < 2:
        return await message.reply("Usage: /decline <user_id>")

    user_id = int(message.command[1])
    await client.decline_chat_join_request(message.chat.id, user_id)
    await message.reply(f"🥱 User `{user_id}` declined.")
