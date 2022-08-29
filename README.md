# College-Bazaar
A Online Community Marketplace for College Students to buy and sell products

##To run the app

```
uvicorn --port 8000 --host 127.0.0.1 app:app --reload
```
open link on browser - ```http://127.0.0.1:8000```

## To Generate Secret Key

```
openssl rand -hex 32
```