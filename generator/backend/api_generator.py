#!/usr/bin/env python3
"""
API Endpoint Generator for Store Websites

Generates Flask API endpoints based on store type and requirements.
Provides RESTful APIs for products, orders, customers, etc.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class StoreType(Enum):
    RESTAURANT = "restaurant"
    RETAIL = "retail"
    FLOWER_SHOP = "flower_shop"
    BAKERY = "bakery"
    BOOKSTORE = "bookstore" 
    COFFEE_SHOP = "coffee_shop"

@dataclass
class APIEndpoint:
    path: str
    method: str
    handler_name: str
    description: str
    request_schema: Optional[Dict] = None
    response_schema: Optional[Dict] = None
    auth_required: bool = False

class APIGenerator:
    """Generate Flask API endpoints for store websites"""
    
    def __init__(self, store_type: StoreType, store_name: str):
        self.store_type = store_type
        self.store_name = store_name
        self.endpoints = self._define_endpoints()
    
    def _define_endpoints(self) -> List[APIEndpoint]:
        """Define API endpoints based on store type"""
        endpoints = []
        
        # Common endpoints for all stores
        endpoints.extend(self._get_common_endpoints())
        
        # Store-specific endpoints
        if self.store_type in [StoreType.RETAIL, StoreType.FLOWER_SHOP]:
            endpoints.extend(self._get_ecommerce_endpoints())
        elif self.store_type in [StoreType.RESTAURANT, StoreType.COFFEE_SHOP]:
            endpoints.extend(self._get_restaurant_endpoints())
        elif self.store_type == StoreType.BOOKSTORE:
            endpoints.extend(self._get_bookstore_endpoints())
        
        return endpoints
    
    def _get_common_endpoints(self) -> List[APIEndpoint]:
        """Common endpoints for all store types"""
        return [
            APIEndpoint(
                path="/api/health",
                method="GET",
                handler_name="health_check",
                description="Health check endpoint"
            ),
            APIEndpoint(
                path="/api/contact",
                method="POST",
                handler_name="submit_contact_form",
                description="Submit contact form",
                request_schema={
                    "name": "string",
                    "email": "string",
                    "subject": "string",
                    "message": "string"
                }
            ),
            APIEndpoint(
                path="/api/newsletter/subscribe",
                method="POST",
                handler_name="subscribe_newsletter",
                description="Subscribe to newsletter",
                request_schema={"email": "string"}
            ),
            APIEndpoint(
                path="/api/store/info",
                method="GET",
                handler_name="get_store_info",
                description="Get store information"
            )
        ]
    
    def _get_ecommerce_endpoints(self) -> List[APIEndpoint]:
        """E-commerce specific endpoints"""
        return [
            # Products
            APIEndpoint(
                path="/api/products",
                method="GET",
                handler_name="get_products",
                description="Get all products with filtering"
            ),
            APIEndpoint(
                path="/api/products/<int:product_id>",
                method="GET", 
                handler_name="get_product",
                description="Get single product by ID"
            ),
            APIEndpoint(
                path="/api/products/search",
                method="GET",
                handler_name="search_products",
                description="Search products"
            ),
            APIEndpoint(
                path="/api/products/validate",
                method="POST",
                handler_name="validate_products",
                description="Validate product availability",
                request_schema={"productIds": "array"}
            ),
            
            # Categories
            APIEndpoint(
                path="/api/categories",
                method="GET",
                handler_name="get_categories",
                description="Get product categories"
            ),
            
            # Cart
            APIEndpoint(
                path="/api/cart",
                method="GET",
                handler_name="get_cart",
                description="Get cart contents",
                auth_required=True
            ),
            APIEndpoint(
                path="/api/cart",
                method="POST",
                handler_name="update_cart",
                description="Update cart contents",
                request_schema={
                    "items": "array",
                    "appliedCoupon": "object",
                    "selectedShippingMethod": "object"
                }
            ),
            APIEndpoint(
                path="/api/cart/add",
                method="POST",
                handler_name="add_to_cart",
                description="Add item to cart",
                request_schema={
                    "productId": "integer",
                    "quantity": "integer",
                    "variant": "string"
                }
            ),
            
            # Orders
            APIEndpoint(
                path="/api/orders",
                method="POST",
                handler_name="create_order",
                description="Create new order",
                request_schema={
                    "customerInfo": "object",
                    "shippingAddress": "object",
                    "billingAddress": "object",
                    "items": "array",
                    "paymentInfo": "object"
                }
            ),
            APIEndpoint(
                path="/api/orders/<int:order_id>",
                method="GET",
                handler_name="get_order",
                description="Get order by ID",
                auth_required=True
            ),
            APIEndpoint(
                path="/api/orders",
                method="GET",
                handler_name="get_orders",
                description="Get customer orders",
                auth_required=True
            ),
            
            # Coupons
            APIEndpoint(
                path="/api/coupons/validate",
                method="POST",
                handler_name="validate_coupon",
                description="Validate coupon code",
                request_schema={
                    "code": "string",
                    "subtotal": "number"
                }
            ),
            
            # Reviews
            APIEndpoint(
                path="/api/products/<int:product_id>/reviews",
                method="GET",
                handler_name="get_product_reviews",
                description="Get product reviews"
            ),
            APIEndpoint(
                path="/api/products/<int:product_id>/reviews",
                method="POST",
                handler_name="create_review",
                description="Create product review",
                auth_required=True,
                request_schema={
                    "rating": "integer",
                    "title": "string",
                    "comment": "string"
                }
            )
        ]
    
    def _get_restaurant_endpoints(self) -> List[APIEndpoint]:
        """Restaurant/cafe specific endpoints"""
        return [
            # Menu
            APIEndpoint(
                path="/api/menu",
                method="GET",
                handler_name="get_menu",
                description="Get menu items"
            ),
            APIEndpoint(
                path="/api/menu/categories",
                method="GET",
                handler_name="get_menu_categories",
                description="Get menu categories"
            ),
            
            # Reservations
            APIEndpoint(
                path="/api/reservations",
                method="POST",
                handler_name="create_reservation",
                description="Create table reservation",
                request_schema={
                    "date": "string",
                    "time": "string",
                    "party_size": "integer",
                    "customer_info": "object"
                }
            ),
            APIEndpoint(
                path="/api/reservations/availability",
                method="GET",
                handler_name="check_availability",
                description="Check table availability"
            ),
            
            # Orders (for delivery/takeout)
            APIEndpoint(
                path="/api/orders",
                method="POST",
                handler_name="create_order",
                description="Create food order",
                request_schema={
                    "items": "array",
                    "order_type": "string",
                    "customer_info": "object",
                    "delivery_address": "object"
                }
            ),
            
            # Special offers
            APIEndpoint(
                path="/api/specials",
                method="GET",
                handler_name="get_daily_specials",
                description="Get daily specials"
            )
        ]
    
    def _get_bookstore_endpoints(self) -> List[APIEndpoint]:
        """Bookstore specific endpoints"""
        return [
            # Books (extends products)
            APIEndpoint(
                path="/api/books/search",
                method="GET",
                handler_name="search_books",
                description="Search books by title, author, ISBN"
            ),
            APIEndpoint(
                path="/api/books/recommendations",
                method="GET",
                handler_name="get_book_recommendations",
                description="Get book recommendations"
            ),
            
            # Events
            APIEndpoint(
                path="/api/events",
                method="GET",
                handler_name="get_events",
                description="Get upcoming events"
            ),
            APIEndpoint(
                path="/api/events/<int:event_id>/register",
                method="POST",
                handler_name="register_for_event",
                description="Register for event",
                request_schema={
                    "name": "string",
                    "email": "string",
                    "phone": "string"
                }
            )
        ]
    
    def generate_flask_app(self) -> str:
        """Generate complete Flask application code"""
        app_code = self._generate_app_header()
        app_code += self._generate_models()
        app_code += self._generate_handlers()
        app_code += self._generate_routes()
        app_code += self._generate_app_footer()
        
        return app_code
    
    def _generate_app_header(self) -> str:
        """Generate Flask app header with imports and setup"""
        return f'''#!/usr/bin/env python3
"""
Generated Flask API for {self.store_name}
Store Type: {self.store_type.value}

Auto-generated by Store Website Generator
"""

from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json
import uuid
from typing import Dict, List, Any, Optional

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Store configuration
STORE_CONFIG = {{
    'name': '{self.store_name}',
    'type': '{self.store_type.value}',
    'currency': 'USD',
    'tax_rate': 0.085,
    'shipping_cost': 5.99
}}

'''
    
    def _generate_models(self) -> str:
        """Generate SQLAlchemy models"""
        models = '''
# Database Models

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Decimal(10, 2), nullable=False)
    sale_price = db.Column(db.Decimal(10, 2))
    sku = db.Column(db.String(50), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    image_url = db.Column(db.String(500))
    in_stock = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = db.relationship('Category', backref='products')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'sale_price': float(self.sale_price) if self.sale_price else None,
            'sku': self.sku,
            'category': self.category.name if self.category else None,
            'image': self.image_url,
            'in_stock': self.in_stock,
            'stock_quantity': self.stock_quantity,
            'rating': self.rating,
            'review_count': self.review_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image_url,
            'product_count': len(self.products)
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50))
    
    # Addresses (stored as JSON)
    shipping_address = db.Column(db.JSON)
    billing_address = db.Column(db.JSON)
    
    # Order totals
    subtotal = db.Column(db.Decimal(10, 2), nullable=False)
    tax_amount = db.Column(db.Decimal(10, 2), default=0)
    shipping_cost = db.Column(db.Decimal(10, 2), default=0)
    discount_amount = db.Column(db.Decimal(10, 2), default=0)
    total_amount = db.Column(db.Decimal(10, 2), nullable=False)
    
    # Status and dates
    status = db.Column(db.String(50), default='pending')
    payment_status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Order items
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'shipping_address': self.shipping_address,
            'billing_address': self.billing_address,
            'subtotal': float(self.subtotal),
            'tax_amount': float(self.tax_amount),
            'shipping_cost': float(self.shipping_cost),
            'discount_amount': float(self.discount_amount),
            'total_amount': float(self.total_amount),
            'status': self.status,
            'payment_status': self.payment_status,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Decimal(10, 2), nullable=False)
    total_price = db.Column(db.Decimal(10, 2), nullable=False)
    variant = db.Column(db.String(200))
    
    product = db.relationship('Product')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price),
            'variant': self.variant
        }

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(500))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Newsletter(db.Model):
    __tablename__ = 'newsletter_subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

'''
        
        # Add store-specific models
        if self.store_type in [StoreType.RESTAURANT, StoreType.COFFEE_SHOP]:
            models += '''
class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Decimal(10, 2), nullable=False)
    category = db.Column(db.String(100))
    image_url = db.Column(db.String(500))
    available = db.Column(db.Boolean, default=True)
    calories = db.Column(db.Integer)
    allergens = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category,
            'image': self.image_url,
            'available': self.available,
            'calories': self.calories,
            'allergens': self.allergens.split(',') if self.allergens else []
        }

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50))
    party_size = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    reservation_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='confirmed')
    special_requests = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'party_size': self.party_size,
            'reservation_date': self.reservation_date.isoformat(),
            'reservation_time': self.reservation_time.isoformat(),
            'status': self.status,
            'special_requests': self.special_requests,
            'created_at': self.created_at.isoformat()
        }
'''
        
        return models
    
    def _generate_handlers(self) -> str:
        """Generate API endpoint handlers"""
        handlers = '''
# API Handlers

def generate_order_number():
    """Generate unique order number"""
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

def calculate_tax(subtotal):
    """Calculate tax amount"""
    return subtotal * STORE_CONFIG['tax_rate']

def validate_request_data(data, required_fields):
    """Validate request data has required fields"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, None

'''
        
        # Generate handler for each endpoint
        for endpoint in self.endpoints:
            handlers += self._generate_handler_function(endpoint)
        
        return handlers
    
    def _generate_handler_function(self, endpoint: APIEndpoint) -> str:
        """Generate individual handler function"""
        # This is a simplified version - in a real implementation,
        # you'd generate more sophisticated handlers based on the endpoint
        
        handler_code = f'''
def {endpoint.handler_name}():
    """{endpoint.description}"""
    try:
'''
        
        if endpoint.method == 'GET':
            if 'products' in endpoint.path:
                handler_code += '''
        # Get products with filtering
        query = Product.query
        
        # Apply filters from query parameters
        category = request.args.get('category')
        if category:
            query = query.join(Category).filter(Category.name == category)
        
        search = request.args.get('search')
        if search:
            query = query.filter(Product.name.contains(search))
        
        in_stock = request.args.get('in_stock')
        if in_stock == 'true':
            query = query.filter(Product.in_stock == True)
        
        price_min = request.args.get('price_min', type=float)
        if price_min:
            query = query.filter(Product.price >= price_min)
        
        price_max = request.args.get('price_max', type=float)
        if price_max:
            query = query.filter(Product.price <= price_max)
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        
        products = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'products': [p.to_dict() for p in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        })
'''
            elif endpoint.path == '/api/health':
                handler_code += '''
        return jsonify({
            'status': 'healthy',
            'store': STORE_CONFIG['name'],
            'timestamp': datetime.utcnow().isoformat()
        })
'''
            else:
                handler_code += '''
        # Generic GET handler
        return jsonify({'message': 'Endpoint implemented'})
'''
        
        elif endpoint.method == 'POST':
            if 'contact' in endpoint.path:
                handler_code += '''
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        valid, error = validate_request_data(data, required_fields)
        if not valid:
            return jsonify({'error': error}), 400
        
        # Create contact record
        contact = Contact(
            name=data['name'],
            email=data['email'],
            subject=data.get('subject', ''),
            message=data['message']
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({'message': 'Contact form submitted successfully'}), 201
'''
            elif 'newsletter' in endpoint.path:
                handler_code += '''
        data = request.get_json()
        
        if 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if already subscribed
        existing = Newsletter.query.filter_by(email=data['email']).first()
        if existing:
            if existing.active:
                return jsonify({'message': 'Already subscribed'}), 200
            else:
                existing.active = True
                db.session.commit()
                return jsonify({'message': 'Subscription reactivated'}), 200
        
        # Create new subscription
        subscriber = Newsletter(email=data['email'])
        db.session.add(subscriber)
        db.session.commit()
        
        return jsonify({'message': 'Successfully subscribed to newsletter'}), 201
'''
            else:
                handler_code += '''
        data = request.get_json()
        # Generic POST handler
        return jsonify({'message': 'Data received', 'data': data}), 201
'''
        
        handler_code += '''
    except Exception as e:
        return jsonify({'error': str(e)}), 500

'''
        
        return handler_code
    
    def _generate_routes(self) -> str:
        """Generate Flask routes"""
        routes = '''
# API Routes

'''
        
        for endpoint in self.endpoints:
            routes += f'''@app.route('{endpoint.path}', methods=['{endpoint.method}'])
def {endpoint.handler_name}_route(*args, **kwargs):
    return {endpoint.handler_name}()

'''
        
        return routes
    
    def _generate_app_footer(self) -> str:
        """Generate Flask app footer with database initialization"""
        return '''
# Database initialization
@app.before_first_request
def create_tables():
    """Create database tables"""
    db.create_all()
    
    # Seed initial data if tables are empty
    if Category.query.count() == 0:
        seed_initial_data()

def seed_initial_data():
    """Seed database with initial data"""
    # Create default categories
    categories = []
'''
        
        # Add store-specific categories
        if self.store_type == StoreType.FLOWER_SHOP:
            footer += '''
    categories = [
        Category(name='Roses', description='Beautiful roses for any occasion'),
        Category(name='Tulips', description='Fresh tulips in various colors'),
        Category(name='Lilies', description='Elegant lilies for special moments'),
        Category(name='Bouquets', description='Pre-arranged beautiful bouquets'),
        Category(name='Plants', description='Live plants for home and office')
    ]
'''
        elif self.store_type == StoreType.RETAIL:
            footer = footer.replace('categories = []', '''
    categories = [
        Category(name='Electronics', description='Latest technology products'),
        Category(name='Clothing', description='Fashion and apparel'),
        Category(name='Home & Garden', description='Items for your home'),
        Category(name='Sports', description='Sports and outdoor equipment'),
        Category(name='Books', description='Books and magazines')
    ]
''')
        
        footer += '''
    
    for category in categories:
        db.session.add(category)
    
    db.session.commit()
    
    # Create sample products
    products = []
    for i, category in enumerate(categories):
        for j in range(3):  # 3 products per category
            product = Product(
                name=f'Sample {category.name[:-1]} {j+1}',
                description=f'High quality {category.name.lower()[:-1]} product',
                price=10.99 + (i * 5) + (j * 2),
                sku=f'SKU-{category.name[:3].upper()}-{j+1:03d}',
                category_id=category.id,
                in_stock=True,
                stock_quantity=50,
                rating=4.0 + (j * 0.3)
            )
            products.append(product)
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
        
        return footer

def generate_api_for_store(store_type: str, store_name: str) -> str:
    """Generate complete Flask API for a store"""
    store_type_enum = StoreType(store_type)
    generator = APIGenerator(store_type_enum, store_name)
    return generator.generate_flask_app()

if __name__ == "__main__":
    # Example usage
    api_code = generate_api_for_store("flower_shop", "Bloom & Petals")
    print(api_code) 