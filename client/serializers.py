import json

import requests

from client.models import Sesion

API_URL = 'http://192.168.100.8:8080/Afforox'


class BusinessSerializer():
    @staticmethod
    def register_business(negocio, sucursal, domicilio, horario):
        print(negocio)
        print(sucursal)
        print(domicilio)
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
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + Sesion.token},
            data=json.dumps(negocio, indent=4, sort_keys=True, default=str),
        )
        return


class UserSerializer():
    @staticmethod
    def register_user(usuario, domicilio):
        print(usuario)
        print(domicilio)

        domicilio['numeroExterior'] = domicilio.pop('numero_exterior')
        domicilio['numeroInterior'] = domicilio.pop('numero_interior')

        usuario['correoElectronico'] = usuario.pop('correo_electronico')
        usuario['nombreCompleto'] = usuario.pop('nombre_completo')
        usuario['fechaNacimiento'] = usuario.pop('fecha_de_nacimiento')
        usuario['fotoPerfil'] = usuario.pop('foto_de_perfil')

        usuario['domicilio'] = domicilio
        if usuario['fotoPerfil'] == None:
            usuario['fotoPerfil'] = ''

        response = requests.post(API_URL + '/usuarios', data=json.dumps(usuario, indent=4, sort_keys=True, default=str),
                                 headers={'Content-Type': 'application/json'})
        return response
