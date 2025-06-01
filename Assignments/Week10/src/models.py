from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Product:
    """Data class to store product information."""
    name: str
    description: Optional[str]
    current_price: float
    original_price: Optional[float]
    image_url: str
    rating: Optional[float]
    review_count: Optional[int]
    availability: str
    seller: str
    category: str
    url: str
    timestamp: datetime = datetime.now()

    def to_dict(self):
        """Convert product to dictionary format."""
        return {
            'name': self.name,
            'description': self.description,
            'current_price': self.current_price,
            'original_price': self.original_price,
            'image_url': self.image_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'availability': self.availability,
            'seller': self.seller,
            'category': self.category,
            'url': self.url,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create Product instance from dictionary."""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data) 