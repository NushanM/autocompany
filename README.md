**Want to run the project in Docker?**
## Build
- ```docker build -t autocompany .```
## Run
- ``` docker run -p 80:80 -d autocompany```
# Host
-```http://127.0.0.1/```

-> URLs of requests in postman collection are alreay chaned to above port.
-> For any request which add entry into the db, id field should be updated.
-> There are two accounts already.
-> Admin = { "username": "admin", "password": "gapstars" }
-> User = { "username": "user1", "password": "1234" }
-> Only Admin has access to /list_item, /all_carts.
-> Login need to access /add_to_cart, /my_cart, /remove_item.
-> Requests to above endpoints should include authorization token.