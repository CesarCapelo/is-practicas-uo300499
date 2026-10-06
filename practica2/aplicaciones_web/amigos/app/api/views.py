from flask import request, abort, jsonify
from .. import db
from . import api
from ..models import Amigo

def amigo_a_dict(amigo):
    return {"id": amigo.id, "name": amigo.name,
            "lati": amigo.lati, "longi": amigo.longi,
            "device": amigo.device}

@api.route("/amigo/<int:id>")
def get_amigo(id):
    """
    Retorna JSON con información sobre el amigo cuyo id recibe como parámetro
    o un error 404 si no lo encuentra.
    """
    amigo = Amigo.query.get_or_404(id)
    return jsonify(amigo_a_dict(amigo))

@api.route("/amigo/byName/<name>")
def get_amigo_by_name(name):
    """
    Busca el amigo por su nombre en la base de datos. Si no lo encuentra
    retorna un error 404. Si lo encuentra retorna el JSON con sus datos
    """
    amigo = Amigo.query.filter_by(name = name).first()
    if not amigo:
        abort(404, "No se encuentra ningún amigo con ese nombre")
    return jsonify(amigo_a_dict(amigo))

@api.route("/amigos")
def list_amigos():
    """
    Retorna un JSON con la lista de amigos. Cada amigo es un diccionario
    con los campos 'id', 'name', 'lati', 'longi' y 'device'
    """
    amigos = Amigo.query.all()
    return jsonify([amigo_a_dict(amigo) for amigo in amigos])

@api.route("/amigo/<int:id>", methods=["PUT"])
def edit_amigo(id):
    """
    Modifica en la base de datos el amigo cuyo id recibe como parámetro.

    Retorna el JSON con el amigo tras la modificación
    """
    amigo = Amigo.query.get_or_404(id)

    if not request.json:
        abort(422, "No se ha enviado JSON")

    name = request.json.get("name")
    lati = request.json.get("lati")
    longi = request.json.get("longi")
    device = request.json.get("device")

    # Si el nombre ya lo tiene otro amigo, rechazamos la petición
    if name:
        otro = Amigo.query.filter_by(name = name).first()
        if otro and otro.id != amigo.id:
            abort(422, "Ya existe un amigo con ese nombre")
        amigo.name = name
    if lati:
        amigo.lati = lati
    if longi:
        amigo.longi = longi
    # El dispositivo se acepta aunque sea una cadena vacía
    if device is not None:
        amigo.device = device

    if name or lati or longi or device is not None:
        db.session.commit()

    return jsonify(amigo_a_dict(amigo))

@api.route("/amigo/<int:id>", methods=["DELETE"])
def delete_amigo(id):
    """
    Elimina un amigo cuyo id recibe como parámetro de la base de datos.
    """
    amigo = Amigo.query.get_or_404(id)
    db.session.delete(amigo)
    db.session.commit()
    return ('', 204)

@api.route("/amigos", methods=["POST"])
def new_amigo():
    """
    Modifica en la base de datos añadiendo un amigo cuyos datos
    recibe en JSON.

    Retorna el JSON con el amigo tras la creación, para que el cliente
    pueda conocer el id del amigo recién creado.
    """
    if not request.json:
        abort(422, "No se ha enviado JSON")

    name = request.json.get("name")
    if not name:
        abort(422, "El JSON no incluye el campo 'name'")

    amigo = Amigo.query.filter_by(name = name).first()
    if amigo:
        abort(422, "Ya existe un amigo con ese nombre")

    lati = request.json.get("lati", "0")
    longi = request.json.get("longi", "0")
    device = request.json.get("device")

    amigo = Amigo(name=name, lati=lati, longi=longi, device=device)
    db.session.add(amigo)
    db.session.commit()

    return jsonify(amigo_a_dict(amigo))

@api.route("/devices")
def list_devices():
    """
    Retorna un JSON con la lista de dispositivos no vacíos de los amigos
    """
    amigos = Amigo.query.all()
    return jsonify([amigo.device for amigo in amigos if amigo.device])
