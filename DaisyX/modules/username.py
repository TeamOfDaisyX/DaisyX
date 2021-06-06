from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
import asyncio
from AlainX.events import register as Daisy
from AlainX import bot as tbot
from AlainX import ubot




async def is_register_admin(chat, user):

    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


@Daisy(pattern="^/namehistory ?(.*)")
async def _(event):

    if event.fwd_from:

        return

    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        else:
            return
    if not event.reply_to_msg_id:

        await event.reply("```Reply to any user message.```")

        return

    reply_message = await event.get_reply_message()

    if not reply_message.text:

        await event.reply("```reply to text message```")

        return

    chat = "@SangMataInfo_bot"
    uid = reply_message.sender_id
    reply_message.sender

    if reply_message.sender.bot:

        await event.edit("```Reply to actual users message.```")

        return

    lol = await event.reply("```Processing```")

    async with ubot.conversation(chat) as conv:

        try:

            # response = conv.wait_event(
            #   events.NewMessage(incoming=True, from_users=1706537835)
            # )

            await silently_send_message(conv, f"/search_id {uid}")

            #responses = await silently_send_message(conv, f"/search_id {uid}")
            await asyncio.sleep(1.7)
            async for msg in ubot.iter_messages(461843263, limit=4):
                if not "/search_id" in msg.text:
                    await tbot.send_message(event.chat_id,msg)
                else:
                    pass
        except YouBlockedUserError:

            await event.reply("```Please unblock @SangMataInfo_bot and try again```")

            return
        await lol.delete()
        # await lol.edit(f"{response.message.message}")
