import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Creating the User as a class of Base and creating users table and it's columns
class Users(Base):
	__tablename__ = 'users'
	
	name = Column(String(80), nullable = False)
	email = Column(String(80), nullable = False)
	picture = Column(String(150), nullable = False)
	id = Column(Integer, nullable = False, primary_key = True)

# JSON serialize function for users	
	@property
	def serialize(self):

		return {
			'name': self.name,
			'email': self.email,
			'id': self.id,
		}
# Creating the Categories as a class of Base and creating categories table and it's columns
class Categories(Base):
	__tablename__ = 'categories'
	
	category = Column(String(80), nullable = False)
	cat_id = Column(Integer, nullable = False, primary_key = True)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship(Users)

# JSON serialize function for categories	
	@property
	def serialize(self):

		return {
			'cat_id': self.cat_id,
			'category': self.category,
		}

# Creating the Items as a class of Base and creating items table and it's columns
class Items(Base):
	__tablename__ = 'items'

	item_name = Column(String(80), nullable=False)
	item_id = Column(Integer, nullable = False, primary_key=True)
	description = Column(String(250))
	date_added = Column(DateTime, nullable=False, default=datetime.datetime.now())
	cat_id = Column(Integer, ForeignKey('categories.cat_id'))
	category = Column(String(80), ForeignKey('categories.category'))
	user_id = Column(Integer, ForeignKey('users.id'))
	category = relationship(Categories)
	user = relationship(Users)

# JSON serialize function for Items
	@property
	def serialize(self):

		return {
			'item_name': self.item_name,
			'item_id': self.item_id,
			'description': self.description,
			'date_added': self.date_added,
			'cat_id': self.cat_id,
			'category': self.category.category,
			'user_id': self.user_id,
			'user': self.user.name,
		}
if __name__ == "__main__":
       engine = create_engine('postgresql://catalog:password@localhost/catalogapp')
       Base.metadata.create_all(engine)

