from django.apps import apps
from django.contrib import admin
from .models import CityMaster, ContactMaster, StateMaster, CountryMaster


post_models = apps.get_app_config("DRF_Users").get_models()
exclude_models = {
    "StateMaster" : 1,
    "CountryMaster" : 1,
    "CityMaster" : 1,
    "ContactMaster" : 1,
}

for model in post_models:
    try:
        if exclude_models.get( model.__name__, None ) == None :
            admin.site.register(model)

    except Exception as e:
        pass




@admin.register(ContactMaster)
class ContactMasterAdmin(admin.ModelAdmin):
    autocomplete_fields = [ 'cm_country', 'cm_state', 'cm_city' ]
    search_fields = ['city_name', ]


@admin.register(CityMaster)
class CityMasterAdmin(admin.ModelAdmin):
    search_fields = ['city_name', ]


@admin.register(StateMaster)
class StateMasterAdmin(admin.ModelAdmin):
    search_fields = ['state_name', ]

@admin.register(CountryMaster)
class CountryMasterAdmin(admin.ModelAdmin):
    search_fields = ['country_name', ]
