# YPS_01
---

**Practice task #1 for YPS.** REST API for yard.

REST API created using Flask Framework with RESTful extension, SQLAlchemy with SQLite and Marshmallow.

# Usage

## This API has following endpoints:

### Work with driver:
+ `__GET__ /drivers/driver/`<br>outputs list of all drivers

+ `__GET__ /drivers/driver/?created_at__gte=<date>`<br>
utputs list of all drivers created after <date> in format dd-mm-yyyy
+ `__GET__ /drivers/driver/?created_at__lte=<date>`<br>utputs list of all drivers created before <date> in format dd-mm-yyyy

+ `__GET__ /drivers/driver/<driver_id>`<br>
отримання інформації по певному водію
+ `__POST__ /drivers/driver`<br>
створення нового водія
+ `__PUT__ /drivers/driver/<driver_id>`<br>
редагування водія
+ `__DELETE__ /drivers/driver/<driver_id>`<br>
видалення водія

Vehicle:
+ `__GET__ /vehicles/vehicle/`<br>
вивід списку машин
+ `__GET__ /vehicles/vehicle/?with_drivers=yes`<br>
вивід списку машин з водіями
+ `__GET__ /vehicles/vehicle/?with_drivers=no`<br>
вивід списку машин без водіїв

+ `__GET__ /vehicles/vehicle/<vehicle_id>`<br>
отримання інформації по певній машині
+ `__POST__ /vehicles/vehicle/`<br>
створення нової машини
+ `__PUT__ /vehicles/vehicle/<vehicle_id>`<br>
редагування машини
+ `__POST__ /vehicles/set_driver/<vehicle_id>`<br>
садимо водія в машину / висаджуємо водія з машини  
+ `__DELETE__ /vehicles/vehicle/<vehicle_id>`

***
_Author:_ Andrii Androsiuk

_P.S:_ not fully functional
