from sqlite3 import connect

from pathlib import Path

from utils.schemas import WarnSchema, QOTDSchema, SchemaAbstract

databases = [
    WarnSchema.WarnSchema,
    QOTDSchema.QOTDSchema
]


def create_dbs():

    Path('./data').mkdir(parents=True, exist_ok=True)

    for db_schema in databases:
        db = connect(db_schema.DB_PATH + db_schema.DB_NAME + '.db')

        cursor = db.cursor()
        cursor.executescript(db_schema.create())

        db.commit()
        db.close()