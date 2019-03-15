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

class PumpRPM(Resource):
    def get(self, pump_id):
        return {'rpm': Pump(pump_id).rpm}
    def put(self, pump_id):
        Pump(pump_id).rpm = int(request.form['rpm'])
        return {'rpm': Pump(pump_id).rpm}

api.add_resource(PumpRPM, '/pump/<int:pump_id>/rpm')

speed_fields = {
    'mode':                 fields.String,
    'rpm':                  fields.Integer,
    'index':                fields.Integer,
    'schedule_start':       fields.List(fields.Integer),
    'schedule_end':         fields.List(fields.Integer),
    'egg_timer':            fields.List(fields.Integer)
}

class PumpSpeeds(Resource):
    @marshal_with(speed_fields, envelope='speeds')
    def get(self, pump_id):
        return Pump(pump_id).speeds

api.add_resource(PumpSpeeds, '/pump/<int:pump_id>/speeds')

class PumpSpeed(Resource):
    @marshal_with(speed_fields, envelope='speed')
    def get(self, pump_id, speed_id):
        return Pump(pump_id).speed(speed_id)

    @marshal_with(speed_fields, envelope='speed')
    def put(self, pump_id, speed_id):
        speed = Pump(pump_id).speed(speed_id)
        if request.form.get('mode'):
            speed.mode = request.form['mode']
        if request.form.get('rpm'):
            speed.rpm = int(request.form['rpm'])
        if request.form.get('schedule_start'):
            speed.schedule_start = [int(x) for x in request.form['schedule_start'].split(':')]
        if request.form.get('schedule_end'):
            speed.schedule_end = [int(x) for x in request.form['schedule_end'].split(':')]
        if request.form.get('egg_timer'):
            speed.egg_timer = [int(x) for x in request.form['egg_timer'].split(':')]
        return Pump(pump_id).speed(speed_id)

api.add_resource(PumpSpeed, '/pump/<int:pump_id>/speed/<int:speed_id>')

program_fields = {
    'index':                fields.Integer,
    'rpm':                  fields.Integer
}

class PumpPrograms(Resource):
    @marshal_with(program_fields, envelope='programs')
    def get(self, pump_id):
        return Pump(pump_id).programs

api.add_resource(PumpPrograms, '/pump/<int:pump_id>/programs')

class PumpProgram(Resource):
    @marshal_with(program_fields, envelope='program')
    def get(self, pump_id, program_id):
        return Pump(pump_id).program(program_id)

    @marshal_with(program_fields, envelope='program')
    def put(self, pump_id, program_id):
        Pump(pump_id).program(program_id).rpm = int(request.form['rpm'])
        return Pump(pump_id).program(program_id)

api.add_resource(PumpProgram, '/pump/<int:pump_id>/program/<int:program_id>')

pump_fields = {
    'id':                   fields.Integer,
    'soft_prime_counter':   fields.Integer,
    'rpm':                  fields.Integer,
    'trpm':                 fields.Integer,
    'programs':             fields.Nested(program_fields),
    'speeds':               fields.Nested(speed_fields)
}

class PumpPump(Resource):
    @marshal_with(pump_fields, envelope='pump')
    def get(self, pump_id):
        return Pump(pump_id)

api.add_resource(PumpPump, '/pump/<int:pump_id>')

class PumpSoftPrimeCounter(Resource):
    def get(self, pump_id):
        return Pump(pump_id).soft_prime_counter

api.add_resource(PumpSoftPrimeCounter, '/pump/<int:pump_id>/soft_prime_counter')

class PumpSVRSAlarm(Resource):
    def get(self, pump_id):
        return Pump(pump_id).svrs_alarm

api.add_resource(PumpSVRSAlarm, '/pump/<int:pump_id>/svrs_alarm')

class PumpSVRSRestartEnable(Resource):
    def get(self, pump_id):
        return Pump(pump_id).svrs_restart_enable
    def put(self, pump_id):
        Pump(pump_id).svrs_restart_enable = int(request.form['state'])
        return Pump(pump_id).svrs_restart_enable

api.add_resource(PumpSVRSRestartEnable, '/pump/<int:pump_id>/svrs_restart_enable')

class PumpSVRSTimer(Resource):
    def get(self, pump_id):
        return Pump(pump_id).svrs_restart_timer
    def put(self, pump_id):
        Pump(pump_id).svrs_restart_timer = int(request.form['time'])
        return Pump(pump_id).svrs_restart_timer

api.add_resource(PumpSVRSTimer, '/pump/<int:pump_id>/svrs_restart_timer')

class PumpTRPM(Resource):
    def get(self, pump_id):
        return Pump(pump_id).trpm

    def put(self, pump_id):
        Pump(pump_id).trpm = int(request.form['rpm'])
        return Pump(pump_id).trpm

api.add_resource(PumpTRPM, '/pump/<int:pump_id>/trpm')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
