<h1 align="center">Earth-chan</h1>
<p align="center"><img align="center" src="./docs/earth-chan.png"></p>

<h2 align="center"><a href="https://save-earth-chan-server.herokuapp.com">Root API</a></h2>

# POST Disaster Data
## [POST /api/disaster](https://save-earth-chan-server.herokuapp.com/api/disaster)
<br> Example:
<img src="./docs/ss_2.png">

# GET All Disaster Data
## [GET /api/disaster](https://save-earth-chan-server.herokuapp.com/api/disaster)

<br> Example:
<img src="./docs/ss_1.png">

# GET Disaster by id
## [GET /api/disaster/{id}](https://save-earth-chan-server.herokuapp.com/api/disaster/1)
<br> Example:
<img src="./docs/ss_3.png">

# GET DISASTER by Query 
## [/api/disaster/search](https://save-earth-chan-server.herokuapp.com/api/disaster)

# Additional Parameters
| Parameters       | Details                  |
-------------------|---------------------------
| ``perPage``      | (int) Max item per page  |
| ``page``         | (int) nth Page           |
| ``query``        | (string) query field     |