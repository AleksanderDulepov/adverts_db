from datetime import datetime as date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

def age_valid(value):
	today=date.today()
	delta=relativedelta(today, value).years
	print(delta)
	if delta<9:
		raise ValidationError(
			"Запрещено регистрироваться пользователям младше 9 лет",
			params={'value':value}
		)

