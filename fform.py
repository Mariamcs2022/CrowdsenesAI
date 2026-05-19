from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from wtforms import SelectField, IntegerField

# =========================
# Register Form
# =========================
class RegisterForm(FlaskForm):

    fullname = StringField("Full Name", validators=[
        DataRequired(message="الاسم الكامل مطلوب"),
        Length(min=3, max=75, message="يجب أن يكون الاسم بين 3 و 75 حرف")
    ])

    email = StringField("Email", validators=[
        DataRequired(message="البريد الإلكتروني مطلوب"),
        Email(message="صيغة البريد الإلكتروني غير صحيحة")
    ])

    password = PasswordField("Password", validators=[
        DataRequired(message="كلمة المرور مطلوبة"),
        Length(min=8, message="يجب أن تكون كلمة المرور 8 أحرف على الأقل"),
        Regexp(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]).+$',
            message="يجب أن تحتوي كلمة المرور على حروف وأرقام ورمز خاص"
        )
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(message="يرجى تأكيد كلمة المرور"),
        EqualTo("password", message="كلمتان المرور غير متطابقتين")
    ])

    submit = SubmitField("تسجيل")
# =========================
# Login Form
# =========================
class LoginForm(FlaskForm):

    email = StringField("Email", validators=[
        DataRequired(message="البريد الاكتروني مطلوب"),
        Email(message="صيغة البريد الاكتروني غير صحيحة")
    ])

    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required.")
    ])

    submit = SubmitField("دخول")

# =========================
# Application Form
# =========================
class ApplicationForm(FlaskForm):

    fullname = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired()])

    age = IntegerField("Age", validators=[DataRequired()])

    gender_section = SelectField(
        "Gender Section",
        choices=[
            ("Male", "Male"),
            ("Female", "Female")
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("organiser", "Organiser"),
            ("security", "Security")
        ]
    )

    organization_name = StringField(
        "Organization Name",
        validators=[DataRequired()]
    )

    crowd_experience = StringField("Crowd Experience")
    event_experience = StringField("Event Experience")
    security_experience = StringField("Security Experience")
    emergency_handling = StringField("Emergency Handling")
    volunteer_before = StringField("Volunteer Before")

    submit = SubmitField("Submit Application")

    
# =========================
# Supervisor Login Form
# =========================
class SupervisorLoginForm(FlaskForm):

    email = StringField("Email", validators=[
        DataRequired(message="البريد الإلكتروني مطلوب"),
        Email(message="صيغة البريد الإلكتروني غير صحيحة")
    ])

    password = PasswordField("Password", validators=[
        DataRequired(message="كلمة المرور مطلوبة")
    ])

    submit = SubmitField("دخول")


class SupervisorRegisterForm(FlaskForm):

    fullname = StringField("Full Name", validators=[
        DataRequired(message="الاسم الكامل مطلوب"),
        Length(min=3, max=75, message="يجب أن يكون الاسم بين 3 و 75 حرف")
    ])

    username = StringField("Username", validators=[
        DataRequired(message="اسم المستخدم مطلوب"),
        Length(min=3, max=30, message="اسم المستخدم يجب ان يكون بين 3 و 30 حرف")
    ])

    email = StringField("Email", validators=[
        DataRequired(message="البريد الإلكتروني مطلوب"),
        Email(message="صيغة البريد الإلكتروني غير صحيحة")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="كلمة المرور مطلوبة"),
        Length(min=8, message="يجب أن تكون كلمة المرور 8 أحرف على الأقل"),
        Regexp(
            r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$',
            message="يجب أن تحتوي كلمة المرور على حروف وأرقام ورمز خاص"
        )
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(message="يرجى تأكيد كلمة المرور"),
        EqualTo("password", message="كلمتان المرور غير متطابقتين")
    ])

    submit = SubmitField("تسجيل")