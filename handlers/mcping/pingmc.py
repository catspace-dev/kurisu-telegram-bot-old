from aiogram.types import Message
from mcstatus import MinecraftServer
import socket

async def pingmc_cmd(msg: Message):
    try:
        _, addr = msg.parse_entities().split(' ', 1)
    except ValueError:
        await msg.answer("Использование: "
                         "<code>/pingmc "
                         "&lt;IP_Сервера&gt;[:&lt;Порт&gt;]"
                         "</code>", "HTML")
    else:
        msg = await msg.answer("⌛️ Пингую...")
        server = MinecraftServer.lookup(addr)
        try:
            status = server.status()
        except socket.timeout:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Таймаут)</i>", "HTML")
        except ConnectionResetError:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Удаленный хост принудительно "
                                "разорвал существующее подключение)"
                                "</i>", "HTML")
        except ConnectionRefusedError:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Подключение не установлено, т.к. "
                                "конечный хост отверг запрос на подключение)"
                                "</i>", "HTML")
        except ConnectionAbortedError:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Установленное соединение было прервано "
                                "программным обеспечением на вашем "
                                "хост-компьютере)"
                                "</i>", "HTML")
        else:
            online = str(status.players.online)
            maxonline = str(status.players.max)
            vername = str(status.version.name)
            latency = str(status.latency)
            await msg.edit_text("🎾 <b>Сервер включен.</b>"
                                f"\n * Онлайн: <i>{online} из {maxonline}</i>"
                                f"\n * Версия сервера: <i>{vername}</i>"
                                f"\n * Задержка: <i>{latency}</i>", "HTML")
