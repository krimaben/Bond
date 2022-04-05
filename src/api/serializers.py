from django.contrib.auth.models import User
from api.models import Bond
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = [
            "seller",
            "bond_name",
            "number_of_bonds",
            "sp_of_bonds",
            "status_of_bond",
            "publication_id",
            "buyer",
        ]


class BondUSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = [
            "seller",
            "bond_name",
            "number_of_bonds",
            "sp_of_bonds",
            "status_of_bond",
            "publication_id",
            "buyer",
            "usd_rates",
        ]
