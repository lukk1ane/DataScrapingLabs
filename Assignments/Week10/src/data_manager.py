import json
import csv
import os
from typing import List, Dict
import pandas as pd
from datetime import datetime
from loguru import logger

from models import Product
from config import OUTPUT_DIR

class DataManager:
    """Class to handle data storage and analysis."""
    
    def __init__(self):
        self.products: List[Product] = []
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    def add_product(self, product: Product):
        """Add a product to the collection."""
        self.products.append(product)
    
    def save_to_csv(self, filename: str = None):
        """Save products to CSV file."""
        if not filename:
            filename = f'products_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(self.products[0].to_dict().keys()))
                writer.writeheader()
                for product in self.products:
                    writer.writerow(product.to_dict())
            logger.info(f"Saved {len(self.products)} products to {filepath}")
        except Exception as e:
            logger.error(f"Error saving CSV file: {str(e)}")
    
    def save_to_json(self, filename: str = None):
        """Save products to JSON file."""
        if not filename:
            filename = f'products_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([p.to_dict() for p in self.products], f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.products)} products to {filepath}")
        except Exception as e:
            logger.error(f"Error saving JSON file: {str(e)}")
    
    def generate_analysis(self) -> Dict:
        """Generate basic statistical analysis of the data."""
        if not self.products:
            return {}
        
        df = pd.DataFrame([p.to_dict() for p in self.products])
        
        analysis = {
            'total_products': len(df),
            'price_analysis': {
                'average_price': df['current_price'].mean(),
                'min_price': df['current_price'].min(),
                'max_price': df['current_price'].max(),
            },
            'rating_analysis': {
                'average_rating': df['rating'].mean(),
                'products_with_ratings': df['rating'].count(),
            },
            'top_sellers': df['seller'].value_counts().head(5).to_dict(),
            'categories': df['category'].value_counts().to_dict(),
            'availability_summary': df['availability'].value_counts().to_dict()
        }
        
        return analysis
    
    def save_analysis(self, analysis: Dict = None):
        """Save analysis results to a text file."""
        if analysis is None:
            analysis = self.generate_analysis()
            
        filepath = os.path.join(OUTPUT_DIR, f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("Product Catalog Analysis\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Total Products: {analysis['total_products']}\n\n")
                
                f.write("Price Analysis:\n")
                f.write(f"- Average Price: ${analysis['price_analysis']['average_price']:.2f}\n")
                f.write(f"- Minimum Price: ${analysis['price_analysis']['min_price']:.2f}\n")
                f.write(f"- Maximum Price: ${analysis['price_analysis']['max_price']:.2f}\n\n")
                
                f.write("Rating Analysis:\n")
                f.write(f"- Average Rating: {analysis['rating_analysis']['average_rating']:.2f}\n")
                f.write(f"- Products with Ratings: {analysis['rating_analysis']['products_with_ratings']}\n\n")
                
                f.write("Top Sellers:\n")
                for seller, count in analysis['top_sellers'].items():
                    f.write(f"- {seller}: {count} products\n")
                f.write("\n")
                
                f.write("Categories:\n")
                for category, count in analysis['categories'].items():
                    f.write(f"- {category}: {count} products\n")
                f.write("\n")
                
                f.write("Availability Summary:\n")
                for status, count in analysis['availability_summary'].items():
                    f.write(f"- {status}: {count} products\n")
                    
            logger.info(f"Saved analysis to {filepath}")
        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}") 