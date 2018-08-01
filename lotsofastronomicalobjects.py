from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import Base, Categories, Items, Users

engine = create_engine('sqlite:///catalogapp.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Adding users to the user table
admin = Users(name="Admin", email="admin@admin.cool", picture="https://pics.me.me/wow-disne-the-doge-king-such-king-16626810.png")

session.add(admin)
session.commit()

stuart = Users(name="Stuart", email="Stu@Stu.Stu", picture="https://i.vimeocdn.com/portrait/6620681_300x300")

session.add(stuart)
session.commit()

spacestu = Users(name="SpaceStu", email="SpaceStu@Space.Stu", picture="https://pbs.twimg.com/profile_images/378800000500696537/65f4063ad15e8a5cfa2c1bf1ddaaadcb.jpeg")

session.add(spacestu)
session.commit()


# Adding categories and items for galaxies (source = http://www.astro.cornell.edu/academics/courses/astro201/galaxies/types.htm)
astro_cat1 = Categories(category="Galaxies", user_id=1)

session.add(astro_cat1)
session.commit()

Item1 = Items(item_name="Elliptical Galaxies", description="Shaped like a spheriod, or elongated sphere. These galaxies look like elliptical, or oval, shaped disks.",
					 date_added=datetime.datetime.now(), category=astro_cat1, user_id=1)

session.add(Item1)
session.commit()


Item2 = Items(item_name="Spiral Galaxies", description="Spiral galaxies have three main components: a bulge, disk, and halo. Our Sun is located in an arm of our galaxy, the Milky Way.",
					 date_added=datetime.datetime.now(), category=astro_cat1, user_id=1)

session.add(Item2)
session.commit()

Item3 = Items(item_name="Irregular Galaxies", description="Irregular galaxies have no regular or symmetrical structure",
					 date_added=datetime.datetime.now(), category=astro_cat1, user_id=1)

session.add(Item3)
session.commit()

#  Adding categories and items for Stars (source = http://www.enchantedlearning.com/subjects/astronomy/stars/startypes.shtml)
astro_cat2 = Categories(category="Stars", user_id=2)

session.add(astro_cat2)
session.commit()

Item1 = Items(item_name="Supergiant", description="A supergiant is the largest known type of star. When they die they supernova and become black holes",
					 date_added=datetime.datetime.now(), category=astro_cat2, user_id=2)

session.add(Item1)
session.commit()

Item2 = Items(item_name="White Dwarf", description="A white dwarf is a small, very dense, hot star near the end of its life. ",
					 date_added=datetime.datetime.now(), category=astro_cat2, user_id=2)

session.add(Item2)
session.commit()

Item3 = Items(item_name="Blue Giant", description="A blue giant is a huge, very hot, blue star. It is a post-main sequence star that burns helium",
					 date_added=datetime.datetime.now(), category=astro_cat2, user_id=2)

session.add(Item3)
session.commit()

#  Adding categories and items for Space Telescopes (source = https://www.space.com/6716-major-space-telescopes.html)
astro_cat3 = Categories(category="Space Telescopes", user_id=3)

session.add(astro_cat3)
session.commit()

Item1 = Items(item_name="Hubble Space Telescope", description="Launched in 1990, the Hubble Space Telescope has revolutionized astronomy. Giving astronomers their most distant views of the universe with the Hubble Deep Field and Ultra Deep Field",
					 date_added=datetime.datetime.now(), category=astro_cat3, user_id=3)

session.add(Item1)
session.commit()

Item2 = Items(item_name="Chandra X-ray", description="Launched in 1999, Chandra is the world's most powerful X-ray telescope. It has discovered new black holes",
					 date_added=datetime.datetime.now(), category=astro_cat3, user_id=3)

session.add(Item2)
session.commit()

Item3 = Items(item_name="James Webb Space Telescope", description="The JWST is the successor to Hubble. It will search for light from the first stars and galaxies which formed in the universe after the Big Bang",
					 date_added=datetime.datetime.now(), category=astro_cat3, user_id=3)

session.add(Item3)
session.commit()

# Output at completion
print "added astronomical items!"
print session.query(Categories).all()