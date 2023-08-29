from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import redis
import json

# Povezivanje s Redis poslužiteljem u Docker kontejneru
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_data_from_cache(key):
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

def store_data_in_cache(key, data):
    redis_client.set(key, json.dumps(data))

Base = declarative_base()

Base = declarative_base()

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    players = relationship('Player', back_populates='team')

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(String)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team', back_populates='players')

class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    home_team_id = Column(Integer, ForeignKey('teams.id'))
    away_team_id = Column(Integer, ForeignKey('teams.id'))
    home_team = relationship('Team', foreign_keys=[home_team_id])
    away_team = relationship('Team', foreign_keys=[away_team_id])
    goals = relationship('Goal', back_populates='match')

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    minute = Column(Integer)
    player_id = Column(Integer, ForeignKey('players.id'))
    match_id = Column(Integer, ForeignKey('matches.id'))
    player = relationship('Player', back_populates='goals')
    match = relationship('Match', back_populates='goals')

class Stadium(Base):
    __tablename__ = 'stadiums'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)

class League(Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    teams = relationship('Team', back_populates='league')

Team.league_id = Column(Integer, ForeignKey('leagues.id'))
Team.league = relationship('League', back_populates='teams')

# Ovdje definiramo putanju prema svojoj bazi podataka
db_path = 'sqlite:///football.db'
engine = create_engine(db_path)

# Kreiranje tablica u bazi podataka
Base.metadata.create_all(engine)

# Stvaranje sesije za interakciju s bazom podataka
Session = sessionmaker(bind=engine)
session = Session()

def get_teams():
    teams_data = get_data_from_cache('teams')
    if not teams_data:
        teams_data = session.query(Team).all()
        store_data_in_cache('teams', [team.__dict__ for team in teams_data])
    return teams_data
