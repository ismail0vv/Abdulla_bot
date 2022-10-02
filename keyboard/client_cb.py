from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_button = KeyboardButton("Cancel")
cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
).add(cancel_button)

bishkek_button = KeyboardButton('📍 Бишкек')
osh_button = KeyboardButton('📍 Ош')
talas_button = KeyboardButton('📍 Талас')
yssyk_kol_button = KeyboardButton('📍 Ыссык-Куль')
naryn_button = KeyboardButton('📍 Нарын')
batken_button = KeyboardButton('📍 Баткен')
jalal_abad_button = KeyboardButton('📍 Жалал-Абад')
chui_button = KeyboardButton('📍 Чуй')

regions_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
).add(bishkek_button, chui_button, osh_button, talas_button, yssyk_kol_button, naryn_button, batken_button, jalal_abad_button).row(cancel_button)