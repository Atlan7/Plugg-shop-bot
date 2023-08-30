from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .base_model import BaseModel

#from tgbot.config import preloaded_config


class Brand(BaseModel):
    """Brand model for sneakers"""

    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False) 

    def __repr__(self) -> str:
        return f'<Brand "{self.name}">'


class Sneakers(BaseModel):
    """Sneakers model"""

    __tablename__ = "sneakers" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    price = Column(Integer)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", backref="sneakers", lazy='joined')

    def get_path_to_sneakers_photo(self) -> str:
        base_media_path = preloaded_config.media.base_path
        return f'{base_media_path}/{self.brand.name}/{self.name}' 
    
    def __repr__(self) -> str:
        return f'<Sneakers <{self.brand}> "{self.name}">'
