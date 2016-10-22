import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Users(Base):
	__tablename__ = 'Users'
	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	email = Column(String(255), nullable=True)
	profilePicURL = Column(String(255), default="http://placehold.it/200x200")
	
class Items(Base):
	__tablename__ = 'Items'
	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	sellerID = Column(Integer, ForeignKey("Users.id"))
	description = Column(String(255), nullable=False)
	price = Column(Integer, nullable=False)
	onSale = Column(String(5), default="False")
	onClearance = Column(String(5), default="False")
	imageURL = Column(String(255), nullable=False)
	qty = Column(Integer, default=0)

	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'sellerID': self.sellerID,
			'description': self.description,
			'price': self.price,
			'onSale': self.onSale,
			'onClearance': self.onClearance,
			'imageURL': self.imageURL,
			'qty': self.qty
		}



engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.create_all(engine)
