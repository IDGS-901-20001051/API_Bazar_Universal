from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import json

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    discountPercentage = Column(Float, default=0.0)
    category = Column(String(100), nullable=False, index=True)
    brand = Column(String(100), nullable=True)
    rating = Column(Float, default=0.0)
    stock = Column(Integer, default=0)
    tags = Column(Text, nullable=True)  # JSON string of tags
    sku = Column(String(50), nullable=True)
    weight = Column(Float, nullable=True)
    warrantyInformation = Column(Text, nullable=True)
    shippingInformation = Column(Text, nullable=True)
    availabilityStatus = Column(String(50), nullable=True)
    returnPolicy = Column(Text, nullable=True)
    minimumOrderQuantity = Column(Integer, nullable=True)
    images = Column(Text, nullable=True)  # JSON string de URLs de imágenes
    features = Column(Text, nullable=True)  # JSON string de características
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationship
    sales = relationship("Sale", back_populates="product")
    
    @property
    def images_list(self):
        """Convert images JSON string to list"""
        if self.images:
            try:
                return json.loads(self.images)
            except:
                return []
        return []
    
    @images_list.setter
    def images_list(self, value):
        """Convert list to JSON string"""
        self.images = json.dumps(value) if value else None
    
    @property
    def features_list(self):
        """Convert features JSON string to list"""
        if self.features:
            try:
                return json.loads(self.features)
            except:
                return []
        return []
    
    @features_list.setter
    def features_list(self, value):
        """Convert list to JSON string"""
        self.features = json.dumps(value) if value else None
