from api import serializers
from api.models import Bond
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import json, requests
from django.db.models import F

BMX_token = "a2f6dcc3dc410aa431c13362fc4b81c3048fcdd9932b29be969200905baff4d5"


class CreateBond(APIView):
    # add permission to check if user is authenticated
    permission_classes = [IsAuthenticated]
    # 1. List all
    def get(self, request, *args, **kwargs):
        """
        List all the published bond for given requested user
        """
        bond = Bond.objects.all()
        serializer = serializers.BondSerializer(bond, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        """
        Create the Bond with given data
        """

        data = request.data
        bond_name = data.get("bond_name")
        number_of_bonds = data.get("number_of_bonds")
        sp_of_bonds = data.get("sp_of_bonds")

        if (not number_of_bonds) or (not sp_of_bonds) or (not bond_name):
            return Response(
                json.loads(
                    '{"error":"Please provide all details for bond publication"}'
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "seller": request.user.id,
            "bond_name": bond_name,
            "number_of_bonds": number_of_bonds,
            "sp_of_bonds": sp_of_bonds,
            "status_of_bond": "available",
        }
        serializer = serializers.BondSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "Bond Published Successfully by user "},
                status=status.HTTP_201_CREATED,
            )
        print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyBond(APIView):
    # add permission to check if user is authenticated
    permission_classes = [IsAuthenticated]

    def get_object(self, publication_id):
        """
        Helper method to get the object with given publication_id
        """
        try:
            return Bond.objects.get(publication_id=publication_id)
        except Bond.DoesNotExist:
            return None

    def get(self, request, publication_id, *args, **kwargs):
        """
        Retrieves the publication with given publication_id
        """
        bond_instance = self.get_object(publication_id)
        if not bond_instance:
            return Response(
                {"error": "Bond with this publication id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializers.BondSerializer(bond_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 3. Update
    def put(self, request, publication_id, *args, **kwargs):
        """
        Updates the published bond item with given publication_id if exists
        """
        bond_instance = self.get_object(publication_id)
        if not bond_instance:
            return Response(
                {"error": "Bond with this publication id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if bond_instance.buyer:
            return Response(
                {"error": "Could not purchase this bond.Buyer already linked"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "status_of_bond": "purchased",
            "buyer": request.user.id,
        }
        serializer = serializers.BondSerializer(
            instance=bond_instance, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BondUsd(APIView):
    # add permission to check if user is authenticated
    permission_classes = [IsAuthenticated]
    # 1. List all

    def put(self, request, *args, **kwargs):
        """
        List all the published bond in USD rates.
        """
        url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?locale=en"
        headers = {"Bmx-Token": BMX_token}
        r = requests.get(url, headers=headers)
        res = r.json()
        latest_exchane_rate = (
            res.get("bmx").get("series")[0].get("datos")[0].get("dato")
        )
        Bond.objects.update(usd_rates=F("sp_of_bonds") / latest_exchane_rate)
        bond_instance = Bond.objects.all()
        serializer = serializers.BondUSDSerializer(bond_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateBond(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, publication_id):
        """
        Helper method to get the object with given publication_id, and user_id
        """
        try:
            return Bond.objects.get(publication_id=publication_id)
        except Bond.DoesNotExist:
            return None

    # 1.Update bond details by only creator
    """ Updates the published bond item with given publication_id only by bond creator"""

    def put(self, request, publication_id, *args, **kwargs):
        bond_instance = self.get_object(publication_id)
        IMMUTABLE = ["seller", "status_of_bond", "publication_id", "buyer"]
        if request.data.keys() in IMMUTABLE:
            return Response(
                {"error": "Sorry! you can't update this field"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not bond_instance:
            return Response(
                {"error": "Object with publication id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if bond_instance.buyer:
            return Response(
                {"error": "Sorry! you can't update the purchased bond item"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if bond_instance.seller.id != request.user.id:
            return Response(
                {
                    "error": "Sorry! you are not authorised person to update the bond item"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:
            data = request.data
            serializer = serializers.BondSerializer(
                instance=bond_instance, data=data, partial=True
            )
            if serializer.is_valid():

                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 2. To delete bond.
    """only bond creator can delete bond item by publication id"""

    def delete(self, request, publication_id, *args, **kwargs):

        bond_instance = self.get_object(publication_id)
        if not bond_instance:
            return Response(
                {"error": "Object with publication id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if bond_instance.buyer:
            return Response(
                {"error": "Sorry! you can't delete the purchased bond item"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if bond_instance.seller.id != request.user.id:
            return Response(
                {
                    "error": "Sorry! you are not authorised person to delete the bond item"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            bond_instance.delete()
            return Response(
                {"message": "Bond Item is deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
