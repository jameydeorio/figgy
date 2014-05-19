from django.contrib import admin

from storage.models import Book, Alias, Edition


class InlineAliasAdmin(admin.StackedInline):
    model = Alias
    extra = 0


class EditionAdmin(admin.ModelAdmin):
    inlines = [InlineAliasAdmin]

    list_display = ['id', 'title', 'edition_number', 'list_aliases']
    ordering = ['title', 'edition_number']

    fields = ['book', 'title', 'edition_number', 'description']

    def list_aliases(self, obj):
        if obj:
            return '<pre>%s</pre>' % '\n'.join([o.value for o in obj.aliases.all()])

    list_aliases.allow_tags = True


class InlineEditionAdmin(admin.StackedInline):
    model = Edition
    extra = 0


class BookAdmin(admin.ModelAdmin):
    inlines = [InlineEditionAdmin]
    list_display = ['id', 'title', 'list_editions']

    def list_editions(self, obj):
        if obj:
            return '<pre>%s</pre>' % '\n'.join([o.title for o in obj.editions.all()])

    list_editions.allow_tags = True


admin.site.register(Book, BookAdmin)
admin.site.register(Edition, EditionAdmin)
