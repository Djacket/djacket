import string

from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from user.models import UserProfile, FULLNAME_MAX_LENGTH

RESTRICTED_USERNAMES = ['media', 'static', 'license', 'terms', 'privacy', 'djacket', \
                            'admin', 'help', 'account', 'login', 'logout', 'register', 'settings', \
                            'profile', 'repo', 'about', 'deposit', 'configure', 'configuration', 'configurations',   \
                            'browse', 'history', 'hint', 'hints', 'commit', 'commits', 'graph', 'graphs', 'api', \
                            'branch', 'branches', 'checkout', 'push', 'pull', 'clone', 'star', 'start', 'fork',  \
                            'user', 'accounts']
USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH = 3, 20
PASSWORD_MIN_LENGTH = 5

AVATAR_IMAGE_MAX_SIZE = 640*1024
AVATAR_IMAGE_MAX_DIMENSION = 640
AVATAR_IMAGE_MIN_DIMENSION = 96
VALID_AVATAR_IMAGE_FORMATS = ['jpg', 'jpeg', 'png']


def _fullname_length_exceeds(first_name, last_name):
    """
        Validates length of full name to be less than FULLNAME_MAX_LENGTH.
    """

    return len(first_name) + len(last_name) > FULLNAME_MAX_LENGTH


def _is_alphanumerical(value):
    """
        Checks to see if the given value is alphanumerical or not.
            An allowed set of digits, ASCII letters and underscore is created first,
                if intersection between the given value and this allowed set has no difference
                with value, then surely it's alphanumerical.
    """

    inter = set(value).intersection(set(string.digits+string.ascii_letters+'_'))
    diff = set(value).difference(inter)
    return len(diff) == 0


def username_validator(value):
    """
        Validates given username in terms of uniqeness and length.
    """

    if not _is_alphanumerical(value):
        raise ValidationError(u'Username must only has alphanumerical or underscore characters.')
    elif value in RESTRICTED_USERNAMES:
        raise ValidationError(u'Username is a reserved word')
    elif User.objects.filter(username=value).exists():
        raise ValidationError(u'Username already exists')
    elif value[0].isdigit():
        raise ValidationError(u'Username should start with a letter')
    elif len(value) < USERNAME_MIN_LENGTH or len(value) > USERNAME_MAX_LENGTH:
        raise ValidationError(u'Username should be at least {0} and at most {1} characters long'
                .format(USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH))


def email_validator(value):
    """
        Validates given email in terms of uniqeness and correctness.
    """

    if User.objects.filter(email=value).exists():
        raise ValidationError(u'Email already exists')
    else:
        validate_email(value)


def password_validator(value):
    """
        Validates given password in terms of length.
    """

    if len(value) < PASSWORD_MIN_LENGTH:
        raise ValidationError(u'Password length should be greater than {0}'.format(PASSWORD_MIN_LENGTH))


def image_size_validator(value):
    """
        Validates size of uploaded image.
    """

    if len(value) > AVATAR_IMAGE_MAX_SIZE:
        raise forms.ValidationError(u'Avatar image size should not be greater than 640KiB.')


def image_content_type_validator(value):
    """
        Validates content-type of uploaded image.
            Image format should be of '.jpg' or '.jpeg' or '.png'
    """

    main, ext = value.content_type.split('/')
    if not (main == 'image' and ext in VALID_AVATAR_IMAGE_FORMATS):
        raise forms.ValidationError(u'Avatar image should of either jpeg or png formats.')


def image_dimensions_validator(value):
    """
        Validates dimensions of uploaded image.
            Avatar images should be in square aspect ratios and have size of less than 640*640.
    """

    w, h = get_image_dimensions(value)
    if w != h:
        raise forms.ValidationError(u'Avatar image should have same height and width.')
    elif w > AVATAR_IMAGE_MAX_DIMENSION or h > AVATAR_IMAGE_MAX_DIMENSION:
        raise forms.ValidationError(u'Avatar image width and height should be less than {0} pixels.'
                                        .format(AVATAR_IMAGE_MAX_DIMENSION))
    elif w < AVATAR_IMAGE_MIN_DIMENSION or h < AVATAR_IMAGE_MIN_DIMENSION:
        raise forms.ValidationError(u'Avatar image width and height should be greater than {0} pixels.'
                                        .format(AVATAR_IMAGE_MIN_DIMENSION))


class UserRegistrationForm(forms.Form):
    """
        Form for registering users with username, email and password.
            Avatar and other things are not required at first. User can
            change those in profile settings.
    """

    username = forms.CharField(required=True, validators=[username_validator,])
    email = forms.EmailField(required=True, validators=[email_validator,], widget=forms.EmailInput)
    password = forms.CharField(required=True, validators=[password_validator], widget=forms.PasswordInput)


    def save(self):
        """
            Save method to create a new user with provided information from registration form.
        """

        data = self.cleaned_data

        user = User.objects.create_user(username=(data['username']).lower(), email=(data['email']).lower())
        user.set_password(data['password'])
        user.save()


class UserInfoForm(forms.ModelForm):
    """
        Form for changing user's info.
    """

    old_password = forms.CharField(required=False, validators=[password_validator], widget=forms.PasswordInput)
    new_password = forms.CharField(required=False, validators=[password_validator], widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


    def _password_change_attempted(self, old_password, new_password):
        """
            Returns True if user attempted to change his/her password.
        """

        assert old_password is not None, 'Old Password should not be None.'
        assert new_password is not None, 'New Password should not be None.'

        if len(old_password) == 0 and len(new_password) == 0:
            return False
        elif len(old_password) == 0 and len(new_password) > 0:
            raise forms.ValidationError(u'Old password is not entered.')
        elif len(old_password) > 0 and len(new_password) == 0:
            raise forms.ValidationError(u'New password is not entered.')
        elif len(old_password) > 0 and len(new_password) > 0:
            return True


    def clean(self):
        """
            Clean method to check password correctness before saving, if user attempted to change his/her password.
        """

        if self._password_change_attempted(self.cleaned_data['old_password'], self.cleaned_data['new_password']):
            if self.instance.check_password(self.cleaned_data['old_password']): # Old password entered is correct
                self.instance.set_password(self.cleaned_data['new_password'])       # so new password can be set.
            else:
                raise forms.ValidationError(u'Old password entered is not correct.')
        elif _fullname_length_exceeds(self.data['first_name'], self.data['last_name']):
            raise forms.ValidationError(u'Your full name should be less than {0} characters.'.format(FULLNAME_MAX_LENGTH))

        return self.cleaned_data


class UserProfileForm(forms.Form):
    """
        Form for changing user's profile.
    """

    avatar = forms.ImageField(required=False, validators=[image_size_validator,
                                    image_content_type_validator, image_dimensions_validator])
    birthdate = forms.DateField(required=False)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserProfileForm, self).__init__(*args, **kwargs)


    def save(self):
        """
            Save method to commit changes to user's profile.
        """

        data = self.cleaned_data
        profile = self.user.profile

        if 'avatar' in data:
            profile.avatar = data['avatar'] if data['avatar'] is not None else profile.avatar
        if 'birthdate' in data:
            profile.birthdate = data['birthdate'] if data['birthdate'] is not None else profile.birthdate

        profile.save()


class UserArea51Form(forms.Form):
    """
        Form for deleting user's account entirely.
    """

    confirmed_deletion = forms.BooleanField(required=False)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserArea51Form, self).__init__(*args, **kwargs)


    def save(self):
        """
            Save method to commit dangerous operations to user's account.
        """

        data = self.cleaned_data

        if data['confirmed_deletion']:
            self.user.delete()
