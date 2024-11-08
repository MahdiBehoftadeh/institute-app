from configs.DatabaseConnection import DatabaseConnection
from models.VipResource import VipResource


class VipResourceController:

    def __init__(self):
        db = DatabaseConnection()
        connection = db.connect()

        vp = VipResource(connection)
        vp.create({
            'name': 'Vip',
            'description': 'Vibkbp',
        })



vv = VipResourceController()