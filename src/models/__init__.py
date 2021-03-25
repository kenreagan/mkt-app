from src import db, login_manager
from flask_login import UserMixin
import datetime
import hashlib
from markdown import markdown
import bleach


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    subscribed = db.Column(db.Boolean, default=False)
    product_owned = db.Column(db.Integer, db.ForeignKey('product.id'))
    package = db.Column(db.String(250))

    def __repr__(self):
        return f'<{self.name}>'

    def to_dict(self):
        return {
                "id" : self.id,
                "name" : self.name,
                "last_seen": self.last_seen
                }

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(int(id))


"""
    each product relates to the user who has paid for an account
    once the maximum number of products the user owns has been reached the acccount is said to be invalid
"""
class Product(db.Model):
    __searchable__ = ['name']
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer)
    available = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.Text)
    description_html = db.Column(db.Text)
    category = db.Column(db.String(200), default=None)
    is_deleted = db.Column(db.Boolean, default=False)
    Productlikes = db.Column(db.Integer, default=0, nullable=False)
    path = db.Column(db.String(250))

    def __repr__(self):
        return '%s'%self.name

    @staticmethod
    def on_description_change(target, value, oldvalue, initiator):
        allowed_tags = ["h1", "h2", "p", "a", "blockquote", "br", "span", "div" , "h3", "ul", "li", "tr", "td", "tbody", "table"]
        target.description_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))


    def to_dict(self):
        return {
                "id": self.id,
                "name": self.name,
                "quantity": self.quantity,
                "date created": self.date_created,
                "path": self.path
            }

class ProductReviews(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	texts = db.Column(db.Text)

	@staticmethod
	def on_review_change(target, value, oldvalue, initiator):
		allowed_tags = ["h1", "h2", "p", "a", "blockquote", "br", "span", "div" , "h3", "ul", "li", "tr"]
		target.design = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))


