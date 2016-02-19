from django.contrib import admin

from repository.models import Repository, RepositoryStar, RepositoryFork


admin.site.register(Repository)
admin.site.register(RepositoryStar)
admin.site.register(RepositoryFork)
