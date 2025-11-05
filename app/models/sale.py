from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_title = Column(String(255), nullable=False)
    product_image = Column(String(500), nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)  # Precio unitario
    total = Column(Float, nullable=False)  # Precio total (price * quantity)
    status = Column(String(50), default="Completada")
    date = Column(DateTime, server_default=func.now())
    
    # Relationship
    product = relationship("Product", back_populates="sales")
