from app import db


def auto_repr(self):
	""" Автоматическое REPR форматирование для обьектов """
	base_repr = "<{}(".format(self.__class__.__name__)
	for name in self.__dict__:
		if name[0] == "_":
			continue
		value = self.__dict__[name]
		base_repr += "{}='{}',".format(name,value)
	base_repr = base_repr[:-1]
	base_repr += ")>"
	return base_repr



class Photo(db.Model):
	""" Модель юзеров бота """
	__tablename__ = "Photo"
	id = db.Column(db.Integer(), primary_key=True)
	photo_id = db.Column(db.String())


	def __repr__(self):
		return auto_repr(self)
	

class PhotoResult(db.Model):
	""" Модель юзеров бота """
	__tablename__ = "Photo Result"
	id = db.Column(db.Integer(), primary_key=True)
	photo_id = db.Column(db.String())


	def __repr__(self):
		return auto_repr(self)


class BotUser(db.Model):
	""" Модель юзеров бота """
	__tablename__ = "Bot User"
	id = db.Column(db.Integer(), primary_key=True)
	message_id = db.Column(db.String())
	user_id = db.Column(db.String())


	def __repr__(self):
		return auto_repr(self)


class Text(db.Model):
	""" Модель юзеров бота """
	__tablename__ = "Text"
	id = db.Column(db.Integer(), primary_key=True)
	new_text = db.Column(db.String())


	def __repr__(self):
		return auto_repr(self)
	


db.create_all()
db.session.commit()






