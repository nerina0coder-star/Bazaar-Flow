from app.extensions import db


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    content = db.Column(db.Text, nullable=False)
    picture_url = db.Column(db.String(255), nullable=False)

    # Price In Rial
    price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

    # one-to-many
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Item %r>' % self.name
