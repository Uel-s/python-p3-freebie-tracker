#!/usr/bin/env python3

# Script goes here!
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

# Create the SQLAlchemy database connection
engine = create_engine('sqlite:///freebies.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create sample data
company1 = Company(name='TechCo', founding_year=2000)
company2 = Company(name='DevGear', founding_year=2010)
company3 = Company(name='Code Wizards', founding_year=2015)

dev1 = Dev(name='Alice')
dev2 = Dev(name='Bob')
dev3 = Dev(name='Charlie')
dev4 = Dev(name='David')

# Add companies and devs to the session
session.add_all([company1, company2, company3, dev1, dev2, dev3, dev4])
session.commit()

# Give freebies
company1.give_freebie(dev1, 'T-shirt', 10)
company2.give_freebie(dev1, 'Laptop', 1000)
company2.give_freebie(dev2, 'Stickers', 5)
company3.give_freebie(dev3, 'Mug', 8)
company3.give_freebie(dev3, 'USB Drive', 15)
company3.give_freebie(dev4, 'Hoodie', 20)

# Commit the changes
session.commit()

# Close the session
session.close()
