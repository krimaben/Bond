from django.contrib import admin
from api.models import Bond


class BondAdmin(admin.ModelAdmin):
    list_display = (
            "seller",
            "bond_name",
            "number_of_bonds",
            "sp_of_bonds",
            "status_of_bond",
            "publication_id",
            "buyer",
            "usd_rates"
    )
admin.site.register(Bond, BondAdmin)