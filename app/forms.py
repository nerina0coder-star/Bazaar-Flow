from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ReadOnly, Disabled


def DataRequiredError():
    return 'موفق نبود، به نظر می‌رسد یک یا چند مورد از گزینه ها خالی است'


class RegistrationForm(FlaskForm):
    dtr_msg = DataRequiredError()

    username = StringField(_('نام کاربری'),
                           validators=[DataRequired(_(dtr_msg)), Length(max=63, message=_(
                               'شکست خورد، نام کاربری نباید بیشتر از ۶۳ کاراکتر باشد'))],
                           render_kw={"class": "form-control", "autofocus": True})
    email = EmailField(_('ایمیل'),
                       validators=[DataRequired(_(dtr_msg)),
                                   Email(_("به دلیل غلط بودن ایمیل شکست خورد"), check_deliverability=True),
                                   Length(max=119, message=_('شکست خورد، طول ایمیل نباید بیشتر از ۱۱۹ کاراکتر باشد'))],
                       render_kw={"class": "form-control", "autocomplete": "email"})
    password = PasswordField(_('رمز عبور'),
                             validators=[
                                 DataRequired(_(dtr_msg)),
                                 Length(8, message=_('شکست خورد٬ رمز عبور باید حداقل ۸ کاراکتر باشد'))],
                             render_kw={"class": "form-control", "autocomplete": "new-password"})
    confirmPassword = PasswordField(_('تکرار رمز عبور'),
                                    validators=[
                                        DataRequired(_(dtr_msg)),
                                        EqualTo('password',
                                                message=_("شکست خورد، رمز عبور با رمز عبور تاییدی مطابقت ندارد"))],
                                    render_kw={"class": "form-control", "autocomplete": "new-password"})


class LoginForm(FlaskForm):
    dtr_msg = DataRequiredError()

    username = StringField(_('نام کاربری'),
                           validators=[DataRequired(_(dtr_msg))],
                           render_kw={"class": "form-control", "autofocus": True, "autocomplete": "username"})
    email = EmailField(_('ایمیل'),
                       validators=[DataRequired(_(dtr_msg)),
                                   Email(_("به دلیل غلط بودن ایمیل شکست خورد"), check_deliverability=True)],
                       render_kw={"class": "form-control", "autocomplete": "email"})
    password = PasswordField(_('رمز عبور'),
                             validators=[
                                 DataRequired(_(dtr_msg))],
                             render_kw={"class": "form-control pe-4", "autocomplete": "current-password"})


class CreateChamberForm(FlaskForm):
    dtr_msg = DataRequiredError()

    name = StringField(_('نام تالار'),
                       validators=[DataRequired(_(dtr_msg)),
                                   Length(max=99, message=_('شکست خورد، نام تالار نباید بیش از ۹۹ کاراکتر باشد'))],
                       render_kw={"class": "form-control", "autofocus": True})
    entrance_code = StringField(_('کد ورود'),
                                validators=[DataRequired(_(dtr_msg)), Length(4, 99, message=_(
                                    'شکست خورد، کد ورود نباید بیش از ۹۹ یا زیر ۴ کاراکتر باشد.'))],
                                render_kw={"class": "form-control"})
    description = TextAreaField(_('توضیحات'),
                                validators=[DataRequired(_(dtr_msg)), Length(max=499, message=_(
                                    'شکست خورد، توضیحات نباید از ۴۹۹ کاراکتر بیشتر باشد'))],
                                render_kw={"class": "form-control", "rows": 3})


class EditChamberForm(FlaskForm):
    dtr_msg = DataRequiredError()

    name = StringField(_('نام تالار'),
                       validators=[DataRequired(_(dtr_msg)),
                                   Length(max=99, message=_('شکست خورد، نام تالار نباید بیش از ۹۹ کاراکتر باشد'))],
                       render_kw={"class": "form-control", "autofocus": True})
    entrance_code = StringField(_('کد ورود'),
                                validators=[DataRequired(_(dtr_msg)), Length(4, 99, message=_(
                                    'شکست خورد، کد ورود نباید بیش از 99 یا زیر ۴ کاراکتر باشد.'))],
                                render_kw={"class": "form-control"})
    description = TextAreaField(_('توضیحات'),
                                validators=[DataRequired(_(dtr_msg)), Length(max=499,
                                                                             message=_(
                                                                                 'شکست خورد، توضیحات نباید از ۴۹۹ کاراکتر بیشتر باشد'))],
                                render_kw={"class": "form-control", "rows": 3})
    is_public = BooleanField()
    is_primary = BooleanField()


class EditProfileForm(FlaskForm):
    dtr_msg = DataRequiredError()

    username = StringField(_('نام کاربری'),
                           validators=[DataRequired(_(dtr_msg)),
                                       Length(max=63,
                                              message=_('شکست خورد، نام کاربری نباید بیشتر از ۶۳ کاراکتر باشد'))],
                           render_kw={"class": "form-control", "autofocus": True, "autocomplete": "username"})
    email = StringField(validators=[ReadOnly(), Disabled()],
                        render_kw={"class": "form-control"})
    description = TextAreaField(_('توضیحات پروفایل'),
                                validators=[
                                    Length(max=199, message=_('شکست خورد، طول توضیحات نباید بیش از ۲۰۰ کاراکتر شود'))],
                                render_kw={"class": "form-control"})

    language = SelectField('زبان / Language',
                           validators=[DataRequired(_(dtr_msg))],
                           choices=[('en', 'English / اینگلیسی'), ('fa', 'Persian / فارسی')],
                           render_kw={"class": "form-select"})
    timezone = SelectField('منطقه زمانی / Timezone',
                           validators=[DataRequired(_(dtr_msg))],
                           choices=[('US/Eastern - ایالات متحده/جنوبی', 'Asia/Tehran - آسیا/تهران')],
                           render_kw={"class": "form-select"})
    is_public = BooleanField()

    password = PasswordField(_('رمز عبور'), render_kw={'class': 'form-control', 'autocomplete': 'current-password'})
    new_password = PasswordField(_('رمز عبور جدید'),
                                 render_kw={'class': 'form-control', 'autocomplete': 'new-password'})
    confirm_password = PasswordField(_('تکرار رمز عبور جدید'), validators=[EqualTo('new_password')],
                                     render_kw={'class': 'form-control', 'autocomplete': 'new-password'})
