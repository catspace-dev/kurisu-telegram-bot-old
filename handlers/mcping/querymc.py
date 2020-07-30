from aiogram.types import Message
from loguru import logger
from mcstatus import MinecraftServer
import socket


async def querymc_cmd(msg: Message):
    try:
        _, addr = msg.parse_entities().split(' ', 1)
    except ValueError:
        await msg.answer("Использование: "
                         "<code>/querymc "
                         "&lt;IP_Сервера&gt;:&lt;Порт_Query&gt;"
                         "</code>", "HTML")
    else:
        msg = await msg.answer("⌛️ Пингую...")
        srv = MinecraftServer.lookup(addr)
        try:
            qry = srv.query()
        except socket.timeout:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Таймаут)</i>", "HTML")
        except ConnectionResetError:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Удаленный хост принудительно "
                                "разорвал существующее подключение)"
                                "</i>", "HTML")
        else:
            online = str(qry.players.online)
            maxonline = str(qry.players.max)
            if not qry.players.names:
                await msg.edit_text("🎾 <b>Сервер включен.</b>"
                                    "\n * Онлайн: " + online
                                    " из " + maxonline, "HTML")
            else:
                playerlist = ""
                for playername in qry.players.names:
                    playerlist += "<code>" + str(playername) + "</code> "
                await msg.edit_text("🎾 <b>Сервер включен.</b>"
                                    "\n * Онлайн: <i>" + online
                                    " из " + maxonline + "</i>"
                                    "\n * Игроки: " + playerlist, "HTML")
