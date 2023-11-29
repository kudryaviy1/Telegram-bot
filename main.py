from distutils.log import Log
from urllib import request, response
import telebot
import config
from telebot import types
from telebot.types import LabeledPrice  
from tool import log, language_check, create_markup, reply_markup_combiner, create_inlineKeyboard, create_inlineKeyboard_url
from app import app, bot, db, fsm
import models
import keyboa
import config



#Start
@bot.message_handler(commands=["start"])
@log
def start(message):
	fsm.reset_state(message.from_user.id)
	text = language_check(message.from_user.id)
	if message.from_user.id in config.ADMIN:
		keyboard = reply_markup_combiner(create_markup(text["start_buttons"], 2), create_markup(text["admin_start"]))
	else:
		keyboard = create_markup(text["start_buttons"])

	img = open('hello.jpeg', 'rb')
	bot.send_photo(message.from_user.id, img, text["start"], reply_markup=keyboard)



@bot.message_handler(func=lambda message: True and message.text == language_check(message.from_user.id)["start_buttons"][0])
@log
def buttons_change_text(message):
	text = language_check(message.from_user.id)
	keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["more_info_programe"], 2), create_inlineKeyboard_url(text["more_info_programe_href"], 1), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"})))
	img = open('hello.jpeg', 'rb')
	bot.send_photo(message.from_user.id, img, text["start"], reply_markup=keyboard)


@bot.message_handler(func=lambda message: True and message.text == language_check(message.from_user.id)["start_buttons"][1])
@log
def buttons_change_text23(message):
	text = language_check(message.from_user.id)
	new_text = models.Text.query.first()
	if new_text:
		action_and_sale_text = new_text.new_text
	else:
		action_and_sale_text = text["action_and_sale"]["text"]
	keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["action_and_sale"]["buttons"], 2), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"})))
	bot.send_message(message.from_user.id, action_and_sale_text, reply_markup=keyboard)



@bot.message_handler(func=lambda message: True and message.text == language_check(message.from_user.id)["start_buttons"][2])
@log
def buttons_change_tex(message):
	text = language_check(message.from_user.id)
	keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard({"Оплатить": "to_pay"}, 1), create_inlineKeyboard({"Проверить оплату": "to_pay"}, 1), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"})))
	img = open('hello.jpeg', 'rb')
	bot.send_photo(message.from_user.id, img, text["start"], reply_markup=keyboard)


@bot.message_handler(func=lambda message: True and message.text == language_check(message.from_user.id)["admin_start"][0])
@log
def buttons_change_text(message):
	text = language_check(message.from_user.id)
	if message.from_user.id in config.ADMIN:
		keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["admin"]["buttons"], 1), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"})))
		bot.send_message(message.from_user.id, text["admin"]["admin_hello"], reply_markup=keyboard)


@bot.message_handler(func=lambda message: True and message.text == language_check(message.from_user.id)["start_buttons"][3])
@log
def buttons_change_text1(message):
	text = language_check(message.from_user.id)
	bot.send_message(message.from_user.id, text["questions"]["enter_question"], reply_markup=create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"}))
	fsm.set_state(message.from_user.id, "enter_question")



@bot.message_handler(func=lambda message: True and fsm.get_state(message.from_user.id).state == "enter_question")
@log
def enter_question(message):
	text = language_check(message.from_user.id)
	msg = bot.send_message(config.CHAT_ID, message.text)
	db.session.add(models.BotUser(message_id=msg.id, user_id=message.from_user.id))
	db.session.commit()
	bot.send_message(message.from_user.id, text["questions"]["question_success"])
	fsm.reset_state(message.from_user.id)



@bot.message_handler(content_types=["text"], func=lambda message: True)
@log
def start2(message):
	if message.reply_to_message != None:
		msg = models.BotUser.query.filter_by(message_id=message.reply_to_message.id).first()
		if msg:
			bot.delete_message(config.CHAT_ID, message.reply_to_message.id)
			bot.send_message(msg.user_id, message.text)
			db.session.delete(msg)
			db.session.commit()
			



#Start buttons
@bot.callback_query_handler(func=lambda call: True and call.data.split()[0] == "start_buttons")
@log
def start_buttons(call):
	bot.delete_message(call.from_user.id, call.message.message_id)
	text = language_check(call.from_user.id)
	new_text = models.Text.query.first()
	if new_text:
		action_and_sale_text = new_text.new_text
	else:
		action_and_sale_text = text["action_and_sale"]["text"]

	if call.data.split()[1] == "more_info_programe":
		keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["more_info_programe"], 1), create_inlineKeyboard_url(text["more_info_programe_href"], 1), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"})))
		bot.send_message(call.from_user.id, text["start"], reply_markup=keyboard)
	elif call.data.split()[1] == "action_and_sale":
		keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["action_and_sale"]["buttons"], 1), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"})))
		bot.send_message(call.from_user.id, action_and_sale_text, reply_markup=keyboard)
	elif call.data.split()[1] == "to_pay":
		keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard({"Оплатить": "to_pay"}, 1), create_inlineKeyboard({"Проверить оплату": "to_pay"}, 1), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"})))
		bot.send_message(call.from_user.id, text["start"], reply_markup=keyboard)
	elif call.data.split()[1] == "admin":
		keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["admin"]["buttons"], 1), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel"})))
		bot.send_message(call.from_user.id, text["admin"]["admin_hello"], reply_markup=keyboard)
	


# ======= # Отмена # ======= #
@bot.callback_query_handler(func=lambda call: True and call.data.split(" ")[0] == "back_apanel")
@log
def back_apanel(call):
	bot.delete_message(call.from_user.id, call.message.message_id)
	text = language_check(call.from_user.id)
	if call.data.split()[1] == "1":
		keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["start_buttons"], 2), create_inlineKeyboard(text["admin"]["admin_start"], 2)))
		bot.send_message(call.from_user.id, text["start"], reply_markup=keyboard)
	if call.data.split()[1] == "2":
		pass
		#fsm.reset_state(call.from_user.id)
	
	elif call.data.split()[1] == "3":
		keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["more_info_programe"], 2), create_inlineKeyboard_url(text["more_info_programe_href"], 1), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 2"})))
		bot.send_message(call.from_user.id, text["start"], reply_markup=keyboard)
	



#admin buttons
@bot.callback_query_handler(func=lambda call: True and call.data.split()[0] == "admin")
@log
def start_buttons(call):
	bot.delete_message(call.from_user.id, call.message.message_id)
	text = language_check(call.from_user.id)
	if call.data.split()[1] == "edit_photo":
		bot.send_message(call.from_user.id, text["admin"]["edit_photo_text"])
		fsm.set_state(call.from_user.id, "edit_photo_text")
	elif call.data.split()[1] == "edit_photo_2":
		bot.send_message(call.from_user.id, text["admin"]["edit_photo_text"])
		fsm.set_state(call.from_user.id, "edit_photo_text_2")
	elif call.data.split()[1] == "edit_text":
		bot.send_message(call.from_user.id, text["admin"]["edit_text_text"])
		fsm.set_state(call.from_user.id, "edit_text_text")




@bot.message_handler(func=lambda message: True and fsm.get_state(message.from_user.id).state == "edit_text_text")
@log
def edit_text_text(message):
	print(1)
	new_text = models.Text.query.first()
	if new_text:
		db.session.delete(new_text)
		db.session.commit()
	text = language_check(message.from_user.id)
	db.session.add(models.Text(new_text=message.text))
	db.session.commit()
	bot.send_message(message.from_user.id, text["admin"]["edit_text_success"])
	



@bot.message_handler(content_types=["photo"], func=lambda message: True and fsm.get_state(message.from_user.id).state == "edit_photo_text")
@log
def edit_photo_text(message):
	text = language_check(message.from_user.id)
	db.session.add(models.Photo(photo_id=message.photo[0].file_id))
	db.session.commit()
	bot.send_message(message.from_user.id, text["admin"]["edit_photo_success"])
	
	#keyboard = keyboa.keyboa_combiner(keyboards=(create_inlineKeyboard(text["admin"]["buttons"], 2), create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 1"})))
	#bot.send_message(message.from_user.id, text["admin"]["admin_hello"], reply_markup=keyboard)



@bot.message_handler(content_types=["photo"], func=lambda message: True and fsm.get_state(message.from_user.id).state == "edit_photo_text_2")
@log
def edit_photo_text_2(message):
	text = language_check(message.from_user.id)
	db.session.add(models.PhotoResult(photo_id=message.photo[0].file_id))
	db.session.commit()
	bot.send_message(message.from_user.id, text["admin"]["edit_photo_success"])
	



#more_info_programe buttons
@bot.callback_query_handler(func=lambda call: True and call.data.split()[0] == "more_info_programe")
@log
def start_buttons(call):
	bot.delete_message(call.from_user.id, call.message.message_id)
	text = language_check(call.from_user.id)
	if call.data.split()[1] == "example_dish":
		dishes = models.Photo.query.all()
		media_group = [telebot.types.InputMediaPhoto(dish.photo_id) for dish in dishes]
		bot.send_media_group(call.from_user.id, media=media_group)
	elif call.data.split()[1] == "result_and_response":
		dishes = models.PhotoResult.query.all()
		media_group = [telebot.types.InputMediaPhoto(dish.photo_id) for dish in dishes]
		bot.send_media_group(call.from_user.id, media=media_group)
	elif call.data.split()[1] == "contraindication":
		bot.send_message(call.from_user.id, text["contraindication"]["text"], reply_markup=create_inlineKeyboard({text["admin"]["cancel"]: "back_apanel 3"}))



@bot.callback_query_handler(func=lambda call: True and call.data.split()[0] == "to_pay")
@log
def start_buttons(call):
	bot.delete_message(call.from_user.id, call.message.message_id)
	text = language_check(call.from_user.id)
	bot.send_message(call.from_user.id, text["action_and_sale"]["text2"])


if __name__ == '__main__':
	bot.polling(none_stop=True)



