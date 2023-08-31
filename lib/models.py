from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create the SQLAlchemy database connection
engine = create_engine('sqlite:///freebies.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the models


class Company(Base):
    _tablename_ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    # Establish relationships
    devs = relationship('Dev', secondary='freebies',
                        back_populates='companies')
    freebies = relationship('Freebie', back_populates='company')

    # Method to give a freebie
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(dev=dev, company=self,
                              item_name=item_name, value=value)
        session.add(new_freebie)
        session.commit()

    # Class method to find the oldest company
    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    _tablename_ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Establish relationships
    companies = relationship(
        'Company', secondary='freebies', back_populates='devs')
    freebies = relationship('Freebie', back_populates='dev')

    # Method to check if a dev has received a specific freebie
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    # Method to give away a freebie
    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
            session.commit()


class Freebie(Base):
    _tablename_ = 'freebies'

    id = Column(Integer, primary_key=True)
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    item_name = Column(String)
    value = Column(Integer)

    # Establish relationships
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    # Method to print freebie details
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'


# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session
session = Session()

# Create sample data
company1 = Company(name='Company A', founding_year=1990)
company2 = Company(name='Company B', founding_year=2000)
dev1 = Dev(name='Dev 1')
dev2 = Dev(name='Dev 2')

# Add and commit the sample data
session.add_all([company1, company2, dev1, dev2])
session.commit()

# Give freebies
company1.give_freebie(dev1, 'T-shirt', 10)
company2.give_freebie(dev1, 'Laptop', 1000)
company2.give_freebie(dev2, 'Stickers', 5)

# Test methods
print(dev1.received_one('Laptop'))  # Should print True
print(dev2.received_one('Laptop'))  # Should print False

dev1.give_away(dev2, dev1.freebies[0])
print(dev1.freebies[0].dev.name)  # Should print 'Dev 2'

# Don't forget to commit your changes and close the session when done
session.commit()
session.close()
