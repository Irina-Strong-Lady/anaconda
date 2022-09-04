from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Сохранять авторизацию')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Имя пользователя', validators=[
        DataRequired(), Length(1, 64), Regexp('^[А-Яа-я][А-Яа-я0-9_.]*$', 0,
                                              'Имя пользователя должно содержать только буквы, '
                                              'цифры, точки или знаки подчеркивания')])
    password = PasswordField('Пароль', validators=[
        DataRequired(), EqualTo('password2', message='Пароли должны совпадать')])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email уже существует')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Имя пользователя уже существует')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    password = PasswordField('Новый пароль', validators=[
        DataRequired(), EqualTo('password2', message='Пароли должны совпадать')])
    password2 = PasswordField('Подтвердите новый пароль', validators=[DataRequired()])
    submit = SubmitField('Обновить пароль')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Сбросить пароль')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[
        DataRequired(), EqualTo('password2', message='Пароли должны совпадать')])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Сбросить пароль')


class ChangeEmailForm(FlaskForm):
    email = StringField('Новый email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Обновить адрес email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email уже зарегистрирован')
