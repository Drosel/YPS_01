from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from datetime import datetime


#Initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yard.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


#Description of DB models
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    vehicle_id = db.relationship('Vehicle', backref='respdriver', uselist=False)

    def __repr__(self):
        return f'<Driver #{self.id}>'

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), unique=True) 
    make = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    plate_number = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def __repr__(self):
        return f'<Vehicle #{self.id}>'


#Marshmallow schemas for serialization/deserialization
class DriverSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'created_at', 'updated_at', 'respdriver')
        model = Driver
        datetimeformat = '%d/%m/%Y %H:%M:%S'

driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)

class VehicleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'driver_id', 'make', 'model', 'plate_numb', 'created_at', 'updated_at')
        model = Vehicle
        datetimeformat = '%d/%m/%Y %H:%M:%S'

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)


#API resources
# DRIVER
class DriverListResource(Resource):
    def get(self):
        ra = request.args
        if ra:
            for key in ra.keys():
                coln, comp = key.split("__", 1)
                val = ra.get(key, type=str)
                flt = datetime.strptime(val, '%d-%m-%Y')
                if coln == 'created_at' and comp == 'gte':
                    drivers = Driver.query.filter(Driver.created_at >= flt)
                elif coln == 'created_at' and comp == 'lte':
                    drivers = Driver.query.filter(Driver.created_at <= flt)
                break
        else:
            drivers = Driver.query.all()

        return drivers_schema.dump(drivers)

    def post(self):
        new_driver = Driver(
            first_name=request.json['first_name'],
            last_name=request.json['last_name']
        )
        db.session.add(new_driver)
        db.session.commit()
        return driver_schema.dump(new_driver)

class DriverResource(Resource):
    def get(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        return driver_schema.dump(driver)
    
    def put(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)

        if 'first_name' in request.json:
            driver.first_name = request.json['first_name']
        if 'last_name' in request.json:
            driver.last_name = request.json['last_name']

        db.session.commit()
        return driver_schema.dump(driver)

    def delete(self,driver_id):
        driver = Driver.query.get_or_404(driver_id)
        db.session.delete(driver)
        db.session.commit()
        return '', 204


# VEHICLE
class VehicleListResource(Resource):
    def get(self):
        ra = request.args
        if 'with_drivers' in ra.keys():
            val = ra.get('with_drivers', type=str)
            if val == 'yes':
                vehicles = Vehicle.query.filter(Vehicle.driver_id != 'null')
            elif val == 'no':
                vehicles = Vehicle.query.filter(Vehicle.driver_id == 'null')
        else:
            vehicles = Vehicle.query.all()

        return vehicles_schema.dump(vehicles)

    def post(self):
        new_vehicle = Vehicle(
            make = request.json['make'],
            model = request.json['model'],
            plate_number = request.json['plate_number']
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return vehicle_schema.dump(new_vehicle)

class VehicleResource(Resource):
    def get(self, vehicle_id):
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        return vehicle_schema.dump(vehicle)
    
    def put(self, vehicle_id):
        vehicle = Vehicle.query.get_or_404(vehicle_id)

        if 'make' in request.json:
            vehicle.make = request.json['make']
        if 'model' in request.json:
            vehicle.model = request.json['model']
        if 'plate_number' in request.json:
            vehicle.plate_number = request.json['plate_number']

        db.session.commit()
        return vehicle_schema.dump(vehicle)

    def delete(self,vehicle_id):
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        db.session.delete(vehicle)
        db.session.commit()
        return '', 204

class VehicleDriverResource(Resource):
    def post(self, vehicle_id):
        vehicle = Vehicle.query.get_or_404(vehicle_id)

        if 'respdriver' in request.json:
            vehicle.driver_id = request.json['respdriver']

        db.session.commit()
        return vehicle_schema.dump(vehicle)


#Regestration of API endpoints
api.add_resource(DriverListResource, '/drivers/driver/')
api.add_resource(DriverResource, '/drivers/driver/<int:driver_id>')
api.add_resource(VehicleListResource, '/vehicles/vehicle/')
api.add_resource(VehicleResource, '/vehicles/vehicle/<int:vehicle_id>')
api.add_resource(VehicleDriverResource, '/vehicles/set_driver/<int:vehicle_id>')


if __name__ == '__main__':
    app.run(debug=True)