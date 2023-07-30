from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Bakery(db.Model, SerializerMixin):
    __tablename__ = "bakeries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    # Set up the one-to-many relationship with BakedGood
    baked_goods = db.relationship("BakedGood", back_populates="bakery")
    # Exclude the circular reference
    serialize_rules = ("-baked_goods.bakery",)


class BakedGood(db.Model, SerializerMixin):
    __tablename__ = "baked_goods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"))
    bakery = db.relationship("Bakery", back_populates="baked_goods")
    # serialize_rules = ("-bakery.baked_goods",)
