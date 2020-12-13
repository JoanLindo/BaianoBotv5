# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

import time
from datetime import datetime
from random import choice

from telethon.events import StopPropagation

from userbot import CMD_HELP  # noqa
from userbot.events import register

from userbot import (  # noqa pylint: disable=unused-import isort:skip
    AFKREASON,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    COUNT_MSG,
    ISAFK,
    PM_AUTO_BAN,
    USERS,
)

# ========================= CONSTANTS ============================
AFKSTR = [
    "Estou no modo baiano fdp nao me ",
    "Estou no modo baiano fdp para de me incomoda",
    "Filha da puta tá vendo que eu tô em afk caraio.",
    "Vai se fode estou em afk pare de me mencionar !.",
    "Espera eu voltar arrombado !.",
    "Si continuar me mencionando eu vou comer teu cu eu tou em afk fdp",
    "Estou baianando pode esperar o pai cair da rede.",
    "Desculpa ae fml o pai n tá on !.",
    "Si for o kadso que tiver me mencionando vai tomar no cu.",
    "Tô em afk agora !",
    "AAAAAAAAAAAAAAAAAAAAAA FILHA DA PUTA EU TO OFF DESGRAÇA",
    "Si for o junin que tiver me marcando vai tomar no cu.",
    "Eu fui comer seu cu\n---->",
    "Eu fui voltei ta um oco agora\n<----",
    "Ado ado quem me chamou e viado.",
    "Fodase kadso eu estou em afk",
    "Oi estou em afk gostosa por favor n me chamar ok ?",
    "Seu cu",
    "Lmao. ",
    "ok depois eu ti como",
    "To no zapzap!",
    "to cagando arrombado..",
    "ate?",
]

global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
afk_start = {}

# =================================================================


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    global reason
    USER_AFK = {}
    afk_time = None
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if string:
        AFKREASON = string
        await afk_e.edit(
            f"Ativei o modo baiano!\
        \nRazão: `{string}`"
        )
    else:
        await afk_e.edit("Ativei o modo baiano!")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nVocê ficou ausente!")
    ISAFK = True
    afk_time = datetime.now()  # pylint:disable=E0602
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if ISAFK:
        ISAFK = False
        msg = await notafk.respond("Não estou mais AFK.")
        time.sleep(3)
        await msg.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Você recebeu "
                + str(COUNT_MSG)
                + " mensagens de "
                + str(len(USERS))
                + " chats enquanto esteve fora",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "["
                    + name0
                    + "](tg://user?id="
                    + str(i)
                    + ")"
                    + " te enviou "
                    + "`"
                    + str(USERS[i])
                    + " mensagens`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


@register(incoming=True, disable_edited=False)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "algum tempo atrás"
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Ontem"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime("%A")
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m`"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s`"
            else:
                afk_since = f"`{int(seconds)}s`"
            if AFKREASON:
                await mention.reply(
                    f"Estou ausente fazem {afk_since}.\
                    \nRazão: `{AFKREASON}`"
                )
            else:
                await mention.reply(str(choice(AFKSTR)))
            USERS.update({mention.sender_id: 1})
            COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "algum tempo atrás"
    if (
        sender.is_private
        and sender.sender_id != 777000
        and not (await sender.get_sender()).bot
    ):
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved

                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Ontem"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime("%A")
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m`"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s`"
            else:
                afk_since = f"`{int(seconds)}s`"
            if AFKREASON:
                await sender.reply(
                    f"Estou ausente fazem {afk_since}.\
                    \nRazão: `{AFKREASON}`"
                )
            else:
                await sender.reply(str(choice(AFKSTR)))
            USERS.update({sender.sender_id: 1})
            COUNT_MSG = COUNT_MSG + 1


CMD_HELP.update(
    {
        "afk": ".afk [Motivo Opcional]\
\nUso: Define você como ausente.\nResponde qualquer pessoa que envia PMs/marca \
você e diz o motivo da ausência(razão).\n\nDesliga o AUSENTE quando digitar qualquer coisa, em qualquer lugar.\
"
    }
)
