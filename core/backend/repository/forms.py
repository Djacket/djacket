from django import forms

from repository.models import Repository, REPOSITORY_NAME_MAX_LENGTH, REPOSITORY_NAME_MIN_LENGTH, REPOSITORY_DESCRIPTION_MAX_LENGTH
from utils.system import rename_tree
from git.repo import Repo


def name_length_validator(value):
    """
        Validates given name in terms of length and uniqeness among user's repositories.
    """

    if len(value) < REPOSITORY_NAME_MIN_LENGTH or len(value) > REPOSITORY_NAME_MAX_LENGTH:
        raise forms.ValidationError(u'Repository name length should be greater than {0} and less than {1}.'
                        .format(REPOSITORY_NAME_MIN_LENGTH, REPOSITORY_NAME_MAX_LENGTH))


def ascii_validator(value):
    """
        Checks to see if the given name is in "ASCII" format.
    """

    try:
        value.encode('ascii')
    except UnicodeEncodeError:
        raise forms.ValidationError(u'Repository name should be in English characters.')


def special_characters_validator(value):
    """
        Checks to if the given name has any special characters:
            !, @, #, $, %, ^, &, *, (, ), +, =, {, }, [, ], :, ;, ", \, ', \, /, <, >, ',', ?
    """

    if set('!@#$%^&*.()+={}[]:;"\'\/<>,?').intersection(value):
        raise forms.ValidationError(u'Repository name should only contain letters, numbers, hyphen and underscore.')


class RepositoryCreationForm(forms.Form):
    """
        Form for creating a new repository.
    """

    name = forms.CharField(required=True, validators=[name_length_validator, ascii_validator, special_characters_validator])
    description = forms.CharField(required=False)
    private = forms.BooleanField(required=False)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self._initialize_form(kwargs.pop('instance', None))
        self.edit = kwargs.pop('edit', False)   # boolean flag to indicate we're not creating a new object.
        super(RepositoryCreationForm, self).__init__(*args, **kwargs)


    def _initialize_form(self, instance):
        """
            If instance object is provided then we initialize form with
                the given instance.
        """

        if instance is not None:
            assert isinstance(instance, Repository), "Instance should be of Repository type."
            self.instance = instance
            self.repo_entering_name = instance.name  # store current repository name in case user changed it's name.


    def _moderate_name(self, name):
        """
            Returns name string without whitespaces and concatenates name parts with '-' character.
        """

        return '-'.join(name.split())


    def _repo_exists(self, repository_name):
        """
            Checks to see if user has an exact repository with the given name.
        """

        user_repos = Repository.objects.all_repositores(user=self.user)
        if not self.edit: # if a new object is being created we check for it's name uniqeness.
            if len(user_repos) > 0:
                return len(user_repos.filter(name=repository_name)) > 0
        elif self.edit and self.instance is not None:   # if object is being edited we check for a name conflict with other repos.
            if set(repo.name for repo in user_repos.filter(name=repository_name)
                        if repo.id != self.instance.id).intersection({repository_name}):
                return True
        return False


    def _update_instance(self, data):
        """
            Updates given instance with provided data kwargs.
        """

        assert self.instance is not None, "Instance object shoud not be None."
        self.instance.name = data['name']
        self.instance.description = data['description']
        self.instance.private = data['private']
        self.instance.save()


    def clean(self):
        """
            Clean method for moderating repository name.
        """

        self.cleaned_data['name'] = self._moderate_name(self.data['name'])
        name = self.cleaned_data['name']

        if self._repo_exists(name):
            raise forms.ValidationError(u'You have another repository with this name.')
        return self.cleaned_data


    def save(self):
        """
            Save method to create a new repository with provided information from registration form.
        """

        data = self.cleaned_data

        if self.edit:
            self._update_instance(data)
            if self.instance.name != self.repo_entering_name:   # rename repository folder if it's name has changed.
                rename_tree(Repo.get_repository_location(
                                self.instance.owner.username, self.repo_entering_name), '{0}.git'.format(self.instance.name))
        elif not self.edit:
            repository = Repository.objects.create(name=data['name'],
                            description=data['description'], owner=self.user, private=data['private'])
            repository.save()


class RepositoryArea51Form(forms.Form):
    """
        Form for deleting repository (and probably other dangerous stuffs in future).
    """

    confirmed_deletion = forms.BooleanField(required=False)


    def __init__(self, *args, **kwargs):
        self.repository = kwargs.pop('repository')
        super(RepositoryArea51Form, self).__init__(*args, **kwargs)


    def save(self):
        """
            Save method to commit dangerous operations to repository.
        """

        data = self.cleaned_data

        if data['confirmed_deletion']:
            self.repository.delete()
