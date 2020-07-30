from aiogram.types import Message
from mcstatus import MinecraftServer
import socket


async def querymc_cmd(msg: Message):
    try:
        _, addr = msg.parse_entities().split(' ', 1)
    except ValueError:
        await msg.answer("Использование: <code>/querymc &lt;IP_Сервера&gt;:&lt;Порт_Query&gt;</code>", "HTML")
    else:
        msg = await msg.answer(":hourglass: Пингую...")
        srv = MinecraftServer.lookup(addr)
        try:
            qry = srv.query()
        except socket.timeout:
            await msg.edit_text(":volleyball: <b>Сервер выключен.</b>", "HTML")
        else:
            online = str(qry.players.online)
            maxonline = str(qry.players.max)
            if not qry.players.names:
                await msg.edit_text(":tennis: <b>Сервер включен.</b>\nОнлайн: " + online + " из " + maxonline, "HTML")
            else:
                playerlist = ""
                for playername in qry.players.names:
                    playerlist += "<code>" + str(playername) + "</code> "
                await msg.edit_text(":tennis: <b>Сервер включен.</b>\nОнлайн: <i>" + online + " из " + maxonline + "</i>\nИгроки: " + playerlist, "HTML")
