from app.extensions import db

# for many-to-many relationship of users and chambers

participants = db.Table('participants',
                        db.Column('chamber_id', db.Integer, db.ForeignKey('chamber.id')),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                        )

