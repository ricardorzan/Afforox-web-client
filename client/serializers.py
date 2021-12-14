import json

import requests

from client.models import Sesion

API_URL = 'http://192.168.100.8:8080/Afforox'


class BusinessSerializer():
    @staticmethod
    def register_business(negocio, sucursal, domicilio, horario):
        print(negocio)
        print(sucursal)
        print(horario)

        domicilio['numeroExterior'] = domicilio.pop('numero_exterior')
        domicilio['numeroInterior'] = domicilio.pop('numero_interior')

        horario['horarioApertura'] = horario.pop('horario_apertura')
        horario['horarioCierre'] = horario.pop('horario_cierre')
        horario['dia'] = "TODOS"

        sucursal['aforoTotal'] = int(sucursal['aforo_total'])
        sucursal['domicilio'] = domicilio
        sucursal['horarios'] = [horario]

        negocio['sucursales'] = [sucursal]
        if negocio['fotoPerfil'] == None:
            negocio['fotoPerfil'] = ''

        response = requests.post(
            url=API_URL + '/negocios',
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer '+ Sesion.token},
            data=json.dumps(negocio, indent=4, sort_keys=True, default=str),
        )
        return response
