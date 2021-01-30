from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup


btn_bad = InlineKeyboardButton("КАЛЛ 🤮", callback_data='bt2')
btn_cool = InlineKeyboardButton("КЛАСС 😎", callback_data='bt1')
greet_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(btn_cool, btn_bad)

btn_black = InlineKeyboardButton("⬛", callback_data='c#000000')
btn_wight = InlineKeyboardButton("⬜", callback_data='c#FFFFFF')
btn_green = InlineKeyboardButton("🟩", callback_data='c#00FF00')
btn_yellow = InlineKeyboardButton("🟨", callback_data='c#FFFF00')
btn_red = InlineKeyboardButton("🟥", callback_data='c#FF0000')
btn_blue = InlineKeyboardButton("🟦", callback_data='c#0000FF')

c_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(btn_black, btn_wight, btn_green, btn_yellow, btn_red, btn_blue)

l1= InlineKeyboardButton("в рамке", callback_data='l1')
l2= InlineKeyboardButton("с фильтром", callback_data='l2')

l_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(l1,l2)
