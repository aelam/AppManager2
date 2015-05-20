__author__ = 'ryan'


from django.contrib import admin
from models import App, Package, Comment, ProvisioningProfile

class AppAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'app_identifier',]


class PackageAdmin(admin.ModelAdmin):
    list_display = ['bundle_name', 'bundle_short_version',]
    pass


admin.site.register(App, AppAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Comment)
admin.site.register(ProvisioningProfile)



# class ProvisioningProfileAdmin(admin.ModelAdmin):
#     fields = ('profile_path',)

# admin.site.register(ProvisioningProfileAdmin)