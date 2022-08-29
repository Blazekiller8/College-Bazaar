# College-Bazaar
A Online Community Marketplace for College Students to buy and sell products
==
## Prerequisites:
* Python 3.8+
* `pip install -r requirements.txt`

___
## To run the app :

```
uvicorn --port 8000 --host 127.0.0.1 app:app --reload
```

open link on browser - ```http://127.0.0.1:8000``` 

___
## To Generate Secret Key :

```
openssl rand -hex 32
```
___
## TODO :
- Add authentication
- Add Session
- Add Student page
- Add Admin page
- Add Product page
- Add Tags
- Add Search
- Add Filter
- Add Chat with Seller
- Add Approval by Admin
- Add Homepage

___