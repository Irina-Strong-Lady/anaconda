from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField,\
    SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('Введите Ваше имя?', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class EditProfileForm(FlaskForm):
    name = StringField('Ваши Ф.И.О.', validators=[Length(0, 64)])
    location = StringField('Ваш населенный пункт', validators=[Length(0, 64)])
    about_me = TextAreaField('Обо мне')
    submit = SubmitField('Отправить')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Имя пользователя', validators=[
        DataRequired(), Length(1, 64), 
        Regexp('^[А-Яа-я][А-Яа-я0-9_.]*$', 0,
               'Имя пользователя должно содержать буквы, цифры, точки или '
               'нижние подчеркивания')])
    confirmed = BooleanField('Подтвердить')
    role = SelectField('Роль', coerce=int)
    name = StringField('Ваши Ф.И.О.', validators=[Length(0, 64)])
    location = StringField('Ваш населенный пункт', validators=[Length(0, 64)])
    about_me = TextAreaField('Обо мне')
    submit = SubmitField('Отправить')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) 
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email уже существует')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Имя пользователя уже существует')


class PostForm(FlaskForm):
    body = PageDownField("Здесь можно написать Ваше сообщение в общий чат", validators=[DataRequired()])
    submit = SubmitField('Отправить')


class CommentForm(FlaskForm):
    body = StringField('Введите Ваш комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')