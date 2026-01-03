from sqlalchemy import Column, Integer, String, Date, DECIMAL, Text
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    city = Column(String(50))
    country = Column(String(50))
    profile_image = Column(String(255))


class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20))
    cover_image = Column(String(255))


class ItinerarySection(Base):
    __tablename__ = "itinerary_sections"
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer)
    section_name = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(DECIMAL(10, 2))


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    city = Column(String(50))
    activity_type = Column(String(50))
    name = Column(String(100))
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    image = Column(String(255))


class CommunityPost(Base):
    __tablename__ = "community_posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    trip_id = Column(Integer)
    content = Column(Text)
    image = Column(String(255))
