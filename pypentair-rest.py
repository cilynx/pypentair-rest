#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from pypentair import Pump

app = Flask(__name__)
api = Api(app)

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

class Speed(Resource):
    @marshal_with(speed_fields, envelope='speed')
    def get(self, pump_id, speed_id):
        return Pump(pump_id).speed(speed_id)

api.add_resource(Speed, '/pump/<int:pump_id>/speed/<int:speed_id>')

program_fields = {
    'index':                fields.Integer,
    'rpm':                  fields.Integer
}

class Program(Resource):
    @marshal_with(program_fields, envelope='program')
    def get(self, pump_id, program_id):
        return Pump(pump_id).program(program_id)

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
