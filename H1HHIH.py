import asyncio 
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from kvsqlite.sync import Client as DB
from datetime import date
from pyrogram.errors import FloodWait 
botdb = DB('botdb.sqlite')
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeExpired
from pyrogram.errors.exceptions.bad_request_400 import PasswordHashInvalid
from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
from pyrogram.errors.exceptions.bad_request_400 import PhoneCodeInvalid
#############################################################################
from telethon import TelegramClient
from telethon import __version__ as v2
from telethon.sessions import StringSession
from telethon.errors import (
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from pyromod import listen
from pyrogram import (
    __version__ as v
)

#حقوق احمد @H1HHIH - @Z1ZZIZ
ownerID = int("5108562302") #ايدي الادمن 
api_hash = "84da7f08e87849853b2fa6728e4192a2" #ايبي هاش 
api_id = 19312827 #ايبي ايدي
token = "5882944724:AAFZF7dLV" #توكن البوت


bot = Client(
  'bot'+token.split(":")[0],
  19312827, #ايبي ايدي
 '84da7f08e87849853b2fa6728e4192a2', #ايبي هاش
  bot_token=token, in_memory=True
)
app = Client(
  name="session",
  api_id=api_id, api_hash=api_hash,
  bot_token=token, in_memory=True
)
#bot = app
#app = bot

STARTKEY = InlineKeyboardMarkup(
       [
         [
           InlineKeyboardButton("≈ إذاعة للمستخدمين ≈", callback_data="broadcast")
         ],
         [
           InlineKeyboardButton("≈ الاحصائيات ≈", callback_data="stats"),
           InlineKeyboardButton("≈ الأدمنية ≈", callback_data="adminstats"),
           InlineKeyboardButton("≈ المحظورين ≈", callback_data="bannedstats"),
         ],
         [
           InlineKeyboardButton("≈ كشف مستخدم ≈",callback_data="whois"),
           InlineKeyboardButton("≈ حظر مستخدم ≈",callback_data="ban"),
         ],
         [
           InlineKeyboardButton("≈ الغاء حظر مستخدم ≈",callback_data="unban"),
         ],
         [
           InlineKeyboardButton("≈ رفع ادمن ≈",callback_data="addadmin"),
           InlineKeyboardButton("≈ تنزيل ادمن ≈",callback_data="remadmin"),
         ]
       ]
     )
if not botdb.get("db"+token.split(":")[0]):
   data = {
     "users":[],
     "admins":[],
     "banned":[],
   }
   botdb.set("db"+token.split(":")[0], data)

if not ownerID in botdb.get("db"+token.split(":")[0])["admins"]:
   data = botdb.get("db"+token.split(":")[0])
   data["admins"].append(ownerID)
   botdb.set("db"+token.split(":")[0], data)

@bot.on_message(filters.command("start") & filters.private)
async def on_start(c,m):
   getDB = botdb.get("db"+token.split(":")[0])
   if m.from_user.id in getDB["banned"]:
     return await message.reply("🚫 تم حظرك من استخدام البوت",quote=True)
   if m.from_user.id == ownerID or m.from_user.id in getDB["admins"]:
     await m.reply(f"**• أهلاً بك ⌯ {m.from_user.mention}\n• إليك لوحة تحكم الادمن**",reply_markup=STARTKEY,quote=True)
   if not m.from_user.id in getDB["users"]:
      data = getDB
      data["users"].append(m.from_user.id)
      botdb.set("db"+token.split(":")[0], data)
      for admin in data["admins"]:
         text = f"– New user stats the bot :"
         username = "@"+m.from_user.username if m.from_user.username else "None"
         text += f"\n\n𖡋 𝐔𝐒𝐄 ⌯  {username}"
         text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {m.from_user.mention}"
         text += f"\n𖡋 𝐈𝐃 ⌯  `{m.from_user.id}`"
         text += f"\n𖡋 𝐃𝐀𝐓𝐄 ⌯  **{date.today()}**"
         try: await c.send_message(admin, text, reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (m.from_user.first_name,user_id=m.from_user.id)]]))
         except: pass
   data = {"name":m.from_user.first_name[:25], "username":m.from_user.username, "mention":m.from_user.mention(m.from_user.first_name[:25]),"id":m.from_user.id}
   botdb.set(f"USER:{m.from_user.id}",data)


@bot.on_message(filters.private & ~filters.service)
async def on_messages(c,m):       
   if botdb.get(f"broad:{m.from_user.id}") and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      text = "**— جاري إرسال الإذاعة إلى المستخدمين**\n"
      reply = await m.reply(text,quote=True)
      count=0
      users=botdb.get("db"+token.split(":")[0])["users"]
      for user in users:
        try:
          await m.copy(user)
          count+=1
          await reply.edit(text+f"**— تم ارسال الإذاعة الى [ {count}/{len(users)} ] مستخدم**")
        except FloodWait as x:
          await asyncio.sleep(x.value)
        except Exception:
          pass
      return True
   
   if m.text and botdb.get(f"whois:{m.from_user.id}") and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      getUser=botdb.get(f"USER:{m.text[:15]}")
      if not getUser:
        return await m.reply("– لا يوجد مستخدم بهذا الآيدي",quote=True)
      else:
         name=getUser["name"]
         id=getUser["id"]
         mention=getUser["mention"]
         username="@"+getUser["username"] if getUser["username"] else "None"
         language=botdb.get(f"LANG:{id}")
         text = f"𖡋 𝐔𝐒𝐄 ⌯  {username}"
         text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {name}"
         text += f"\n𖡋 𝐈𝐃 ⌯  `{id}`"
         text += f"\n𖡋 𝑳𝐀𝐍𝐆 ⌯  {language}"
         text += f"\n𖡋 𝐀𝐂𝐂 𝑳𝐈𝐍𝐊 ⌯  **{mention}**"
         return await m.reply(text,quote=True)
   
   if m.text and botdb.get(f"ban:{m.from_user.id}") and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      getUser=botdb.get(f"USER:{m.text[:15]}")
      if not getUser:
        return await m.reply("– لا يوجد مستخدم بهذا الآيدي",quote=True)
      else:
        if getUser["id"] in botdb.get("db"+token.split(":")[0])["admins"]:
          return await m.reply(f"– لا يمكنك حظر ⌯ {getUser['mention']} ⌯ لأنه ادمن",quote=True)
        else:
          if getUser["id"] in botdb.get("db"+token.split(":")[0])["banned"]:
            return await m.reply(f"– لا يمكنك حظر ⌯ {getUser['mention']} ⌯ لأنه محظور مسبقاً",quote=True)
          name=getUser["mention"]
          id=getUser["id"]
          username="@"+getUser["username"] if getUser["username"] else "None"
          language=botdb.get(f"LANG:{id}")
          text = f"- This user added to blacklist:\n\n"
          text += f"𖡋 𝐔𝐒𝐄 ⌯  {username}"
          text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {name}"
          text += f"\n𖡋 𝑳𝐀𝐍𝐆 ⌯  {language}"
          text += f"\n𖡋 𝐈𝐃 ⌯  `{id}`"
          data = botdb.get("db"+token.split(":")[0])
          data["banned"].append(id)
          botdb.set("db"+token.split(":")[0],data)
          return await m.reply(text,quote=True)
   
   if m.text and botdb.get(f"unban:{m.from_user.id}") and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      getUser=botdb.get(f"USER:{m.text[:15]}")
      if not getUser:
        return await m.reply("– لا يوجد مستخدم بهذا الآيدي",quote=True)
      else:
        if getUser["id"] in botdb.get("db"+token.split(":")[0])["admins"]:
          return await m.reply(f"– لا يمكنك الغاء حظر ⌯ {getUser['mention']} ⌯ لأنه ادمن",quote=True)
        else:
          if not getUser["id"] in botdb.get("db"+token.split(":")[0])["banned"]:
            return await m.reply(f"– لا يمكنك الغاء حظر ⌯ {getUser['mention']} ⌯ لأنه غير محظور مسبقاً",quote=True)
          name=getUser["mention"]
          id=getUser["id"]
          username="@"+getUser["username"] if getUser["username"] else "None"
          language=botdb.get(f"LANG:{id}")
          text = f"- This user deleted from blacklist:\n\n"
          text += f"𖡋 𝐔𝐒𝐄 ⌯  {username}"
          text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {name}"
          text += f"\n𖡋 𝑳𝐀𝐍𝐆 ⌯  {language}"
          text += f"\n𖡋 𝐈𝐃 ⌯  `{id}`"
          data = botdb.get("db"+token.split(":")[0])
          data["banned"].remove(id)
          botdb.set("db"+token.split(":")[0],data)
          return await m.reply(text,quote=True)
   
   if m.text and botdb.get(f"add:{m.from_user.id}") and m.from_user.id == ownerID:
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      getUser=botdb.get(f"USER:{m.text[:15]}")
      if not getUser:
        return await m.reply("– لا يوجد مستخدم بهذا الآيدي",quote=True)
      else:
        if getUser["id"] in botdb.get("db"+token.split(":")[0])["admins"]:
          return await m.reply(f"– لا يمكنك رفع ⌯ {getUser['mention']} ⌯ لأنه ادمن مسبقاً",quote=True)
        if getUser["id"] in botdb.get("db"+token.split(":")[0])["banned"]:
          return await m.reply(f"– لا يمكنك رفع ⌯ {getUser['mention']} ⌯ لأنه محظور",quote=True)
        else:          
          name=getUser["mention"]
          id=getUser["id"]
          username="@"+getUser["username"] if getUser["username"] else "None"
          language=botdb.get(f"LANG:{id}")
          text = f"- This user added to admins list:\n\n"
          text += f"𖡋 𝐔𝐒𝐄 ⌯  {username}"
          text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {name}"
          text += f"\n𖡋 𝑳𝐀𝐍𝐆 ⌯  {language}"
          text += f"\n𖡋 𝐈𝐃 ⌯  `{id}`"
          data = botdb.get("db"+token.split(":")[0])
          data["admins"].append(id)
          botdb.set("db"+token.split(":")[0],data)
          return await m.reply(text,quote=True)
   
   if m.text and botdb.get(f"rem:{m.from_user.id}") and m.from_user.id == ownerID:
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      getUser=botdb.get(f"USER:{m.text[:15]}")
      if not getUser:
        return await m.reply("– لا يوجد مستخدم بهذا الآيدي",quote=True)
      else:
        if not getUser["id"] in botdb.get("db"+token.split(":")[0])["admins"]:
          return await m.reply(f"– لا يمكنك تنزيل ⌯ {getUser['mention']} ⌯ لأنه مو ادمن",quote=True)
        if getUser["id"] == ownerID:
          return await m.reply(f"– لا يمكنك تنزيل ⌯ {getUser['mention']} ⌯ لأنه مالك البوت",quote=True)
        else:
          name=getUser["mention"]
          id=getUser["id"]
          username="@"+getUser["username"] if getUser["username"] else "None"
          language=botdb.get(f"LANG:{id}")
          text = f"- This user deleted from admins list:\n\n"
          text += f"𖡋 𝐔𝐒𝐄 ⌯  {username}"
          text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {name}"
          text += f"\n𖡋 𝑳𝐀𝐍𝐆 ⌯  {language}"
          text += f"\n𖡋 𝐈𝐃 ⌯  `{id}`"
          data = botdb.get("db"+token.split(":")[0])
          data["admins"].remove(id)
          botdb.set("db"+token.split(":")[0],data)
          return await m.reply(text,quote=True)

@bot.on_callback_query()
async def on_Callback(c,m):      
   if m.data == "broadcast" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      await m.edit_message_text("• أرسل الإذاعة الآن ( صورة ، نص ، ملصق ، ملف ، صوت )\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"broad:{m.from_user.id}",True)
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      
   if m.data == "whois" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      await m.edit_message_text("• ارسل الآن ايدي المستخدم للكشف عنه\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"whois:{m.from_user.id}",True)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      
   if m.data == "ban" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      await m.edit_message_text("• ارسل الآن ايدي المستخدم لحظره\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"ban:{m.from_user.id}",True)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
   
   if m.data == "unban" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      await m.edit_message_text("• ارسل الآن ايدي المستخدم لرفع حظره\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"unban:{m.from_user.id}",True)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
   
   if m.data == "addadmin" and m.from_user.id == ownerID:
      await m.edit_message_text("• ارسل الآن ايدي المستخدم لرفعه ادمن\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"add:{m.from_user.id}",True)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
   
   if m.data == "remadmin" and m.from_user.id == ownerID:
      await m.edit_message_text("• ارسل الآن ايدي المستخدم لرفعه ادمن\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"rem:{m.from_user.id}",True)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")

   if m.data == "back" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      #await m.answer("• تم الرجوع بنجاح والغاء كل شي ",show_alert=True)
      await m.edit_message_text(f"**• أهلاً بك ⌯ {m.from_user.mention}\n• إليك لوحة تحكم الادمن**",reply_markup=STARTKEY)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      
   if m.data == "stats" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      users = len(botdb.get("db"+token.split(":")[0])["users"])
      await m.answer(f"• احصائيات البوت ⌯ {users}", show_alert=True,cache_time=10)
      
   if m.data == "adminstats" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      admins = len(botdb.get("db"+token.split(":")[0])["admins"])
      await m.answer(f"• احصائيات الادمنية ⌯ {admins}\n• سيتم ارسال بيانات كل آدمن", show_alert=True,cache_time=60)
      text = "- الادمنية:\n\n"
      count = 1
      for admin in botdb.get("db"+token.split(":")[0])["admins"]:
         if count==101: break
         getUser = botdb.get(f"USER:{admin}")
         mention=getUser["mention"]
         id=getUser["id"]
         text += f"{count}) {mention} ~ (`{id}`)\n"
         count+=1
      text+="\n\n—"
      await m.message.reply(text,quote=True)
   
   if m.data == "bannedstats" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      bans = botdb.get("db"+token.split(":")[0])["banned"]
      if not bans:  return await m.answer("• لا يوجد محظورين", show_alert=True,cache_time=60)
      await m.answer(f"• احصائيات المحظورين ⌯ {len(bans)}\n• سيتم ارسال بيانات كل المحظورين", show_alert=True,cache_time=60)
      text = "- المحظورين:\n\n"
      count = 1
      for banned in bans:
         if count==101: break
         getUser = botdb.get(f"USER:{banned}")
         mention=getUser["mention"]
         id=getUser["id"]
         text += f"{count}) {mention} ~ (`{id}`)\n"
         count+=1
      text+="\n\n—"
      await m.message.reply(text,quote=True)




#############################################################################

@app.on_message(filters.command("start") & filters.private)
async def start_msg(app, message):
      reply_markup = ReplyKeyboardMarkup(
        [
          [
            KeyboardButton ("بـايـروجـرام"), KeyboardButton ("تـيـلـيـثـون")
          ],
          [KeyboardButton ("مـعـلـومـات عـن الـبـوت")]
        ],
        resize_keyboard=True, placeholder='استخراج جلسات'
      )
      await message.reply('''
- مرحـبـًا عـزيـزي 🙋 {},
في بوت استخـراج جلسات 
- لبـدء استخـراج الجلسة اختـر الجلسـة بالاسفل.
- إذا كنـت تريـد أن يكون حسـابك في أمـان تام فاختر بايروجـرام أمـا إذا كـان رقمك حقيقـي فاختر تيليثون .
 - ملاحظـة :
- احـذر مشاركـة الكود لأحـد لأنه يستطيـع اختراق حسـابك ⚠️ .
'''.format(message.from_user.mention), reply_markup=reply_markup, quote=True)

@app.on_message(filters.text & filters.private)
async def generator_and_about(app,m):
    if m.text == "مـعـلـومـات عـن الـبـوت":
      text = ''
      text += "🐍 اللـغـة الـبـرمـجـيـة - بـايـثـون "
      text += f"\n🔥 اصـدار بايروجرام {v}"
      text += f"\n🌱 اصـدار تـيـلـيـثـون {v2}"
      text += f"\n\n👤 مـطـور الـبـوت: @Z1ZZIZ"
      await m.reply(text, quote=True)

    if m.text == "بـايـروجـرام":
        rep = await m.reply(
        "**⏳ يـعالـج..**", reply_markup=ReplyKeyboardRemove ()
        ,quote=True)
        c = Client(
          f"pyro{m.from_user.id}",api_id,api_hash,
          device_model="Pyrogram", in_memory=True
        )
        await c.connect()
        await rep.delete()
        phone_ask = await m.chat.ask(
          "⎆ يـرجـى إرسـال رقـم هاتفـك مـع رمـز الدولة مثــال 📱: \n+963995×××××",
          reply_to_message_id=m.id, filters=filters.text
        )
        phone = phone_ask.text
        try:
          send_code = await c.send_code(phone)
        except PhoneNumberInvalid:
          return await phone_ask.reply("⎆ رقـم الهـاتف الذي أرسلـته غير صالح أعـد استخـراج الجلسـة مـرة أخـرى .\n/start", quote=True)
        except Exception:
          return await phone_ask.reply("خطأ! ، يرجى المحاولة مرة أخرى لاحقًا 🤠\n/start",quote=True)
        hash = send_code.phone_code_hash
        code_ask = await m.chat.ask(
          "⎆ أرسـل الكـود\n إذا جاءك في هـذه الطريقـة '12345' أرسـل بين كـل رقـم فـراغ\nمثـال : ' 1 2 3 4 5' .",filters=filters.text
        )
        code = code_ask.text
        try:
          await c.sign_in(phone, hash, code)
        except SessionPasswordNeeded:
          password_ask = await m.chat.ask("⎆ يـرجـى إرسـال التحقق الخـاص بحسـابك ..", filters=filters.text)
          password = password_ask.text
          try:
            await c.check_password(password)
          except PasswordHashInvalid:
            return await password_ask.reply("» التحقـق بخطوتيـن الخـاص بـك غيـر صـالح.\nيرجـى إعـادة استخـراج الجلسـة مـرة أخـرى.\n/start", quote=True)
        except (PhoneCodeInvalid, PhoneCodeExpired):
          return await code_ask.reply("رمز الهاتف غير صالح!", quote=True)
        try:
          await c.sign_in(phone, hash, code)
        except:
          pass
        rep = await m.reply("**⏳ يـعـالـج ..**", quote=True)
        get = await c.get_me()
        text = '**✅ تم تسجيل الدخول بنجاح\n'
        text += f'👤 الاسم الأول : {get.first_name}\n'
        text += f'🆔 بطاقة تعريف : {get.id}\n'
        text += f'📞 رقم الهاتف : {phone}\n'
        text += f'🔒 تم حفظ الجلسة في الرسائل المحفوظة'
        string_session = await c.export_session_string()
        await rep.delete()
        await c.send_message('me', f'تم استخراج جلسة بايروجرام {v2} هذه الجلسة\n\n`{string_session}`')
        await c.disconnect()
        await app.send_message(
          m.chat.id, text
        )




    if m.text == "تـيـلـيـثـون":
        rep = await m.reply(
          "**⏳ يـعـالـج..**",
          reply_markup=ReplyKeyboardRemove ()
          ,quote=True
        )
        c = TelegramClient(StringSession(), api_id, api_hash)
        await c.connect()
        await rep.delete()
        phone_ask = await m.chat.ask( "⎆ يـرجـى إرسـال رقـم هاتفـك مـع رمـز الدولة مثــال 📱: \n+963995××××× ",
          reply_to_message_id=m.id, filters=filters.text
        )
        phone = phone_ask.text
        try:
          send_code = await c.send_code_request(phone)
        except PhoneNumberInvalidError:
          return await phone_ask.reply("⎆ رقـم الهـاتف الذي أرسلـته غير صالح أعـد استخـراج الجلسـة مـرة أخـرى .\n/start", quote=True)
        except Exception:
          return await phone_ask.reply("خطأ! ، يرجى المحاولة مرة أخرى لاحقًا 🤠\n/start",quote=True)
        code_ask = await m.chat.ask("*⎆ أرسـل الكـود\n إذا جاءك في هـذه الطريقـة '12345' أرسـل بين كـل رقـم فـراغ\nمثـال : ' 1 2 3 4 5' .",filters=filters.text)
        code = code_ask.text.replace(" ","")
        try:
          await c.sign_in(phone, code, password=None)
        except SessionPasswordNeededError:
          password_ask = await m.chat.ask("⎆ يـرجـى إرسـال التحقق الخـاص بحسـابك ..", filters=filters.text)
          password = password_ask.text
          try:
            await c.sign_in(password=password)
          except PasswordHashInvalidError:
            return await password_ask.reply("» التحقـق بخطوتيـن الخـاص بـك غيـر صـالح.\nيرجـى إعـادة استخـراج الجلسـة مـرة أخـرى.\n/start", quote=True)
        except (PhoneCodeExpiredError, PhoneCodeInvalidError):
          return await code_ask.reply("رمز الهاتف غير صالح!", quote=True)
        await c.start(bot_token=phone)
        rep = await m.reply("**⏳ يـعـالـج ..**", quote=True)
        get = await c.get_me()
        text = '**✅ تم تسجيل الدخول بنجاح \n'
        text += f'👤 الاسم الأول : {get.first_name}\n'
        text += f'🆔 بطاقة تعريف : {get.id}\n'
        text += f'📞 رقم الهاتف : {phone}\n'
        text += f'🔒 تم حفظ الجلسة في الرسائل المحفوظة'
        string_session = c.session.save()
        await rep.delete()
        await c.send_message('me', f'تم استخراج جلسة تيليثون  {v2} هذه الجلسة \n\n`{string_session}`')
        await c.disconnect()

        await app.send_message(
          m.chat.id,
          text
        )

app.start()
bot.start()
print("تم تشغيل البوت @Z1ZZIZ")
idle()