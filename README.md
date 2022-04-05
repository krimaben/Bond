# Django sample application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/krimaben/Bond.git
$ cd bond
```

We have docker environment to install dependencies and run project:
Commands to run project
```sh
$ make build-web
$ make up
$ make syncdb
$ make createsuperuser
```
And navigate to `http://0.0.0.0:8000/admin/`.

Generate token from Banco de mexico for current rate exchange via
`https://www.banxico.org.mx/SieAPIRest/service/v1/token` to get your **BMX-token** credentials.
Please set generated BMX_token in view.py file.
## API Documentation

##### 1. Generate JWT Token
Request-type: POST
API: http://0.0.0.0:8000/bond/users/token/
Response Format: 
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MTc0NTQ3MCwiaWF0IjoxNjQ5MTUzNDcwLCJqdGkiOiIwODBmNjUwYTg5ZjE0MDU1OGJjNjEzZTc5YTk5MjI3MyIsInVzZXJfaWQiOjF9.30WK9zaZp-kz1gYfZ_rsj7YPips8QkHSeYRIeRDYllQ",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5MjM5ODcwLCJpYXQiOjE2NDkxNTM0NzAsImp0aSI6IjVlZTk3ODkyYjU4YzRkYmFiYjM4NjA1NzY2NDAwMmNlIiwidXNlcl9pZCI6MX0.4rGdM1VY-ZDqcJSbZUcxgx8CCy0PJfKIRUzgVOfS6Pc"
}
```

##### NOTE - All API calls are authenticated hence before API call add the token generated in Header
###### {"Authorizarion": "Bearer "your_token_here""}
#
##### 2. Publish Bond
Request-type: POST
API: http://0.0.0.0:8000/bond/api
Payload Format: JSON

    {
        "bond_name": "bond_name",
        "number_of_bonds": 125,
        "sp_of_bonds": 12.3698
    }

Response Format: 
```
{
    "success": "Bond Published Successfully by user "
}
```
In case if user misses any of the field in payload, user would get error
```
{
    "error": "Please provide all details for bond publication"
}
```

##### 3. Get all published Bonds
Request-type: GET
API: http://0.0.0.0:8000/bond/api
Response Format: 
```
[
    {
        "seller": 1,
        "bond_name": "bond_name",
        "number_of_bonds": 125,
        "sp_of_bonds": "12.3698",
        "status_of_bond": "available",
        "publication_id": 1,
        "buyer": null
    }
]
```

##### 4. Get bond by publication_id
Request-type: GET
API: http://0.0.0.0:8000/bond/api/{int:publication_id}
Response Format: 
```
[
    {
        "seller": 1,
        "bond_name": "bond_name",
        "number_of_bonds": 125,
        "sp_of_bonds": "12.3698",
        "status_of_bond": "available",
        "publication_id": 1,
        "buyer": null
    }
]
```
In case if publication_id doesn't exist API throws error as
```
{
    "error": "Bond with this publication id does not exists"
}
```

##### 5. Purchase bond by publication_id
Request-type: PUT
API: http://0.0.0.0:8000/bond/api/{int:publication_id}/
Response Format: 
```
{
    "seller": 1,
    "bond_name": "bond_name",
    "number_of_bonds": 125,
    "sp_of_bonds": "12.3698",
    "status_of_bond": "purchased",
    "publication_id": 1,
    "buyer": 1
}
```
In case if publication_id doesn't exist API throws error as
```
{
    "error": "Bond with this publication id does not exists"
}
```
In case if bond is already purchased API throws error as
```
{
    "error": "Could not purchase this bond.Buyer already linked"
}
```

##### 6. List published item in USD rates
Request-type: PUT
API: http://0.0.0.0:8000/bond/api/USD
Response Format: 
```
[
    {
        "seller": 1,
        "bond_name": "bond_name",
        "number_of_bonds": 125,
        "sp_of_bonds": "12.3698",
        "status_of_bond": "purchased",
        "publication_id": 1,
        "buyer": 1,
        "usd_rates": "0.6265"
    }
]
```
##### 7. Update published bond
Request-type: PUT
API: http://0.0.0.0:8000/bond/api/update/{int:publication_id}/

Payload:
```
{
    "bond_name": "UpdatedBond"
}
```
Response Format: 
```
{
    "seller": 1,
    "bond_name": "UpdatedBond",
    "number_of_bonds": 1235,
    "sp_of_bonds": "5.0000",
    "status_of_bond": "available",
    "publication_id": 1,
    "buyer": null
}
```
NOTE - Only user who created the bond can update the bond, once bond is purchased that bond can't be updated

###### Error Responses:-
#
```
{
    "error": "Sorry! you can't update this field"
}
```
```
{
    "error": "Object with publication id does not exists"
}
```
```
{
    "error": "Sorry! you can't update the purchased bond item"
}
```
```
{
    "error": "Sorry! you are not authorised person to update the bond item"
}
```
##### 8. Delete published bond
Request-type: PUT
API: http://0.0.0.0:8000/bond/api/delete/{int:publication_id}/
Response Format: 
```
{
    "message": "Bond Item is deleted successfully!"
}
```
###### Error Responses:-
#
```
{
    "error": "Object with publication id does not exists"
}
```
```
{
    "error": "Sorry! you can't update the purchased bond item"
}
```
```
{
    "error": "Sorry! you are not authorised person to update the bond item"
}
```