#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from pypentair import Pump

app = Flask(__name__)
api = Api(app)

class PumpAddress(Resource):
    def get(self, pump_id):
        return {'address': Pump(pump_id).address}

    def put(self, pump_id):
        Pump(pump_id).address = int(request.form['address'])
        return {'address': Pump(int(request.form['address']) - 95).address}

api.add_resource(PumpAddress, '/pump/<int:pump_id>/address')

class PumpID(Resource):
    def get(self, pump_id):
        return {'id': Pump(pump_id).id}

    def put(self, pump_id):
        Pump(pump_id).id = int(request.form['id'])
        return {'id': Pump(int(request.form['id'])).id}

api.add_resource(PumpID, '/pump/<int:pump_id>/id')

class PumpRamp(Resource):
    def get(self, pump_id):
        return {'rpm': Pump(pump_id).ramp}

    def put(self, pump_id):
        Pump(pump_id).ramp = int(request.form['rpm'])
        return {'rpm': Pump(pump_id).ramp}

api.add_resource(PumpRamp, '/pump/<int:pump_id>/ramp')

speed_fields = {
    'mode':                 fields.String,
    'rpm':                  fields.Integer,
    'index':                fields.Integer,
    'schedule_start':       fields.List(fields.Integer),
    'schedule_end':         fields.List(fields.Integer),
    'egg_timer':            fields.List(fields.Integer)
}

class Speeds(Resource):
    @marshal_with(speed_fields, envelope='speeds')
    def get(self, pump_id):
        return Pump(pump_id).speeds

api.add_resource(Speeds, '/pump/<int:pump_id>/speeds')

class Speed(Resource):
    @marshal_with(speed_fields, envelope='speed')
    def get(self, pump_id, speed_id):
        return Pump(pump_id).speed(speed_id)

api.add_resource(Speed, '/pump/<int:pump_id>/speed/<int:speed_id>')

program_fields = {
    'index':                fields.Integer,
    'rpm':                  fields.Integer
}

class Programs(Resource):
    @marshal_with(program_fields, envelope='programs')
    def get(self, pump_id):
        return Pump(pump_id).programs

api.add_resource(Programs, '/pump/<int:pump_id>/programs')

class Program(Resource):
    @marshal_with(program_fields, envelope='program')
    def get(self, pump_id, program_id):
        return Pump(pump_id).program(program_id)

    def put(self, pump_id, program_id):
        Pump(pump_id).program(program_id).rpm = int(request.form['rpm'])
        return {'rpm': Pump(pump_id).program(program_id).rpm}

api.add_resource(Program, '/pump/<int:pump_id>/program/<int:program_id>')

pump_fields = {
    'id':                   fields.Integer,
    'soft_prime_counter':   fields.Integer,
    'rpm':                  fields.Integer,
    'trpm':                 fields.Integer,
    'programs':             fields.Nested(program_fields),
    'speeds':               fields.Nested(speed_fields)
}

class PumpAPI(Resource):
    @marshal_with(pump_fields, envelope='pump')
    def get(self, pump_id):
        return Pump(pump_id)

api.add_resource(PumpAPI, '/pump/<int:pump_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
