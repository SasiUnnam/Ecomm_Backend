import logging
from decimal import Decimal

from app.configs.database import SessionLocal
# Ensure all models are imported so SQLAlchemy relationships configure cleanly
from app.models.cart import Cart, CartItem  # noqa: F401
from app.models.category import Category
from app.models.order import Order, OrderItem  # noqa: F401
from app.models.product import Product
from app.models.sub_category import SubCategory
from app.models.user import User  # noqa: F401

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

CATEGORIES_DATA = [
    {
        "name": "Mobiles",
        "slug": "mobiles",
        "description": "Smartphones, feature phones, and mobile accessories.",
        "image_url": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcSM-3nLNHWCmyXYbvBLy2dvW7s2FqPvnJ_aDnwroLkZ-eBHJY0kn8ItbSj8ENIpA4j9-rPSr3xH9FFaTr4f6jv5ZiDgujjhXiIEWNPlbmk&usqp=CAc",
        "subcategories": [
            {
                "name": "Smartphones",
                "slug": "smartphones",
                "description": "Latest touchscreen Android and iOS smartphones.",
            },
            {
                "name": "Mobile Accessories",
                "slug": "mobile-accessories",
                "description": "Cases, chargers, screen protectors, and cables.",
            },
        ],
    },
    {
        "name": "Electronics",
        "slug": "electronics",
        "description": "Laptops, audio equipment, headphones, and home electronics.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrQ1O3baOT4uRFP6hv_SPrdRL1SRslpbWkLY_9HjWdhQ&s=10",
        "subcategories": [
            {
                "name": "Headphones",
                "slug": "headphones",
                "description": "In-ear, on-ear, and over-ear wireless and wired headphones.",
            },
            {
                "name": "Laptops",
                "slug": "laptops",
                "description": "Ultrabooks, gaming laptops, and budget notebooks.",
            },
            {
                "name": "Audio & Speakers",
                "slug": "audio-speakers",
                "description": "Bluetooth speakers, soundbars, and home audio systems.",
            },
        ],
    },
    {
        "name": "Fashion",
        "slug": "fashion",
        "description": "Men's and women's clothing, footwear, and accessories.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLOutL4UBAFc9zrD_cxbMUqsVjXep4ROdoyNMTRSVvEw&s=10",
        "subcategories": [
            {
                "name": "Men's Shoes",
                "slug": "mens-shoes",
                "description": "Sneakers, running shoes, formal shoes, and loafers.",
            },
            {
                "name": "Men's Clothing",
                "slug": "mens-clothing",
                "description": "T-shirts, shirts, jeans, trousers, and jackets.",
            },
            {
                "name": "Women's Clothing",
                "slug": "womens-clothing",
                "description": "Dresses, tops, jeans, and ethnic wear.",
            },
        ],
    },
    {
        "name": "Home & Kitchen",
        "slug": "home-kitchen",
        "description": "Kitchen appliances, cookware, dining, and home utility products.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmILCN2lmTK8WN5bV9o-MWeWumQTHNtyjZb1S97r6BDw&s=10",
        "subcategories": [
            {
                "name": "Kitchen Appliances",
                "slug": "kitchen-appliances",
                "description": "Kettles, air fryers, mixer grinders, and microwaves.",
            },
            {
                "name": "Kitchen & Dining",
                "slug": "kitchen-dining",
                "description": "Bottles, dinner sets, glassware, and storage containers.",
            },
            {
                "name": "Cookware",
                "slug": "cookware",
                "description": "Pans, pressure cookers, kadhais, and pots.",
            },
        ],
    },
    {
        "name": "Beauty",
        "slug": "beauty",
        "description": "Skincare, cosmetics, personal care, and wellness.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCNXAfO-4U_x1f57jC-0qfoCrxD3uI3JhD4sGH7_2Vag&s=10",
        "subcategories": [
            {
                "name": "Skin Care",
                "slug": "skin-care",
                "description": "Face creams, serums, cleansers, and moisturizers.",
            },
            {
                "name": "Makeup",
                "slug": "makeup",
                "description": "Lipsticks, foundations, eyeliners, and makeup kits.",
            },
        ],
    },
]

PRODUCTS_DATA = [
    # -------------------------------------------------------------
    # 1. MOBILES (5 Products)
    # -------------------------------------------------------------
    {
        "category_slug": "mobiles",
        "subcategory_slug": "smartphones",
        "sku": "MOB-APL-IP15-128",
        "name": "Apple iPhone 15",
        "slug": "apple-iphone-15",
        "brand": "Apple",
        "price": Decimal("69999.00"),
        "compare_at_price": Decimal("79999.00"),
        "description": "Apple iPhone 15 with 128GB storage and advanced camera system.",
        "is_featured": True,
        "specifications": {
            "discount": 13,
            "rating": 4.6,
            "reviews": 1250,
            "stock": 25,
            "storage": "128GB",
            "chipset": "A16 Bionic",
            "camera": "48MP Main Camera",
            "network": "5G",
            "images": [
                "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcSM-3nLNHWCmyXYbvBLy2dvW7s2FqPvnJ_aDnwroLkZ-eBHJY0kn8ItbSj8ENIpA4j9-rPSr3xH9FFaTr4f6jv5ZiDgujjhXiIEWNPlbmk&usqp=CAc",
                "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSp3Xc88igUa0C1jPQ2GtlB2W6E8LMqA-i-A3GJohfpJ8blxjg7T-2G49J211LY6OKShqPcH8dixbG8mGnSXssAhB2iGaymLHeVbbXaDfk&usqp=CAc",
            ],
        },
    },
    {
        "category_slug": "mobiles",
        "subcategory_slug": "smartphones",
        "sku": "MOB-SAM-S24-256",
        "name": "Samsung Galaxy S24",
        "slug": "samsung-galaxy-s24",
        "brand": "Samsung",
        "price": Decimal("64999.00"),
        "compare_at_price": Decimal("74999.00"),
        "description": "Samsung Galaxy S24 with AMOLED display and powerful processor.",
        "is_featured": True,
        "specifications": {
            "discount": 13,
            "rating": 4.5,
            "reviews": 980,
            "stock": 18,
            "display": "6.2 inch Dynamic AMOLED 2X",
            "storage": "256GB",
            "ai_features": "Galaxy AI",
            "images": [
                "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQQ0YtIxYfv8Cd13nNhyAtfYcDDintIV4M8xSw_-Xc4JWWfflNwEyvA5zQfIsIiyvlMHX3GJtfi-f99uauykf07uoI1zPl0NKa7QKAhk8XpTf2aemxJrt16a1xEiKOJqOv6Oh-Hkg&usqp=CAc",
                "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQ1FthsV-hCMt_q08X_I46nD-Hy2K8MK8IIDC2Gvr0kD_YLOwIKy85FQTcbe0svIZKJNSp0MFFVdA6Febb9fksZytALkn3KgN9cTcOtrfGvd42E-nDV4S7ETA9fy1IM-IzhvcOADdI&usqp=CAc",
                "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTmEQuxpeV_tom6YZcsoBIqSXcK8g-mYV81vxN_ZKalfLQrFsEKH2qw7bGTPWO79Jiuv_wQLeZ64H0jKB8ym5SFDa0PKlFryHQ8d445hpvAP1UhzTVXFpqfDUK6SwhkMg&usqp=CAc",
            ],
        },
    },
    {
        "category_slug": "mobiles",
        "subcategory_slug": "smartphones",
        "sku": "MOB-1PL-12-256",
        "name": "OnePlus 12 5G",
        "slug": "oneplus-12-5g",
        "brand": "OnePlus",
        "price": Decimal("64999.00"),
        "compare_at_price": Decimal("69999.00"),
        "description": "Flagship 5G smartphone with Snapdragon 8 Gen 3, Hasselblad 4th Gen camera, and 100W SuperVOOC charge.",
        "is_featured": True,
        "specifications": {
            "discount": 7,
            "rating": 4.6,
            "reviews": 840,
            "stock": 22,
            "ram": "12GB",
            "storage": "256GB",
            "battery": "5400mAh",
            "charging": "100W SUPERVOOC",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8KIepBhtGqHb-s_YlF0BYosE0OAkBGS_eSJF-HF8LRg&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRADT4xvsBUH5l5s7bybX19G8qvI4M1zFmoQkZwaS17tg&s=10",
            ],
        },
    },
    {
        "category_slug": "mobiles",
        "subcategory_slug": "smartphones",
        "sku": "MOB-GGL-PX8-128",
        "name": "Google Pixel 8",
        "slug": "google-pixel-8",
        "brand": "Google",
        "price": Decimal("52999.00"),
        "compare_at_price": Decimal("75999.00"),
        "description": "Engineered by Google with Tensor G3 chip, advanced AI photography, and crisp 120Hz Actua display.",
        "is_featured": False,
        "specifications": {
            "discount": 30,
            "rating": 4.4,
            "reviews": 670,
            "stock": 15,
            "ram": "8GB",
            "storage": "128GB",
            "os": "Android 14 with 7 years of updates",
            "images": [
                "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcSM-3nLNHWCmyXYbvBLy2dvW7s2FqPvnJ_aDnwroLkZ-eBHJY0kn8ItbSj8ENIpA4j9-rPSr3xH9FFaTr4f6jv5ZiDgujjhXiIEWNPlbmk&usqp=CAc",
            ],
        },
    },
    {
        "category_slug": "mobiles",
        "subcategory_slug": "smartphones",
        "sku": "MOB-XIA-RN13P-256",
        "name": "Xiaomi Redmi Note 13 Pro+ 5G",
        "slug": "xiaomi-redmi-note-13-pro-plus",
        "brand": "Xiaomi",
        "price": Decimal("29999.00"),
        "compare_at_price": Decimal("33999.00"),
        "description": "200MP camera phone with 3D curved 1.5K AMOLED display, IP68 protection, and 120W HyperCharge.",
        "is_featured": False,
        "specifications": {
            "discount": 12,
            "rating": 4.3,
            "reviews": 1120,
            "stock": 40,
            "ram": "8GB",
            "storage": "256GB",
            "camera": "200MP OIS",
            "images": [
                "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQ1FthsV-hCMt_q08X_I46nD-Hy2K8MK8IIDC2Gvr0kD_YLOwIKy85FQTcbe0svIZKJNSp0MFFVdA6Febb9fksZytALkn3KgN9cTcOtrfGvd42E-nDV4S7ETA9fy1IM-IzhvcOADdI&usqp=CAc",
            ],
        },
    },

    # -------------------------------------------------------------
    # 2. ELECTRONICS (5 Products)
    # -------------------------------------------------------------
    {
        "category_slug": "electronics",
        "subcategory_slug": "headphones",
        "sku": "ELE-BOA-R450",
        "name": "boAt Rockerz 450",
        "slug": "boat-rockerz-450",
        "brand": "boAt",
        "price": Decimal("1499.00"),
        "compare_at_price": Decimal("3990.00"),
        "description": "Wireless Bluetooth headphones with up to 15 hours battery life.",
        "is_featured": True,
        "specifications": {
            "discount": 62,
            "rating": 4.2,
            "reviews": 5400,
            "stock": 50,
            "driver_size": "40mm Dynamic Drivers",
            "battery_life": "15 Hours",
            "bluetooth_version": "v5.0",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8KIepBhtGqHb-s_YlF0BYosE0OAkBGS_eSJF-HF8LRg&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRADT4xvsBUH5l5s7bybX19G8qvI4M1zFmoQkZwaS17tg&s=10",
            ],
        },
    },
    {
        "category_slug": "electronics",
        "subcategory_slug": "laptops",
        "sku": "ELE-HP-LAP15-512",
        "name": "HP Laptop 15",
        "slug": "hp-laptop-15",
        "brand": "HP",
        "price": Decimal("54999.00"),
        "compare_at_price": Decimal("64999.00"),
        "description": "15.6-inch laptop with 16GB RAM and 512GB SSD.",
        "is_featured": True,
        "specifications": {
            "discount": 15,
            "rating": 4.4,
            "reviews": 620,
            "stock": 10,
            "processor": "Intel Core i5 13th Gen",
            "ram": "16GB DDR4",
            "storage": "512GB NVMe SSD",
            "display": "15.6 inch FHD Anti-Glare",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrQ1O3baOT4uRFP6hv_SPrdRL1SRslpbWkLY_9HjWdhQ&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQuCk-k5554pjdAK0W0ttI0x1mLkSSKzZMXrw3gRTeCw&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9gz7-g_ZaetjS9xziTZWGy6-b3PpIVVacpfp8g9xrdg&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwSa4Bywo-ZUmA2kGI0uJ5sd6OtVkyPbFJawyQeEPotA&s=10",
            ],
        },
    },
    {
        "category_slug": "electronics",
        "subcategory_slug": "headphones",
        "sku": "ELE-SNY-WHXM5-BLK",
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "slug": "sony-wh-1000xm5-wireless-headphones",
        "brand": "Sony",
        "price": Decimal("26990.00"),
        "compare_at_price": Decimal("34990.00"),
        "description": "Industry-leading active noise canceling wireless over-ear headphones with 30-hour battery life.",
        "is_featured": True,
        "specifications": {
            "discount": 23,
            "rating": 4.7,
            "reviews": 2350,
            "stock": 20,
            "noise_canceling": "Dual Processor Auto NC Optimizer",
            "battery_life": "30 Hours",
            "color": "Black",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8KIepBhtGqHb-s_YlF0BYosE0OAkBGS_eSJF-HF8LRg&s=10",
            ],
        },
    },
    {
        "category_slug": "electronics",
        "subcategory_slug": "laptops",
        "sku": "ELE-APL-MBA-M2",
        "name": "Apple MacBook Air M2 Chip",
        "slug": "apple-macbook-air-m2-chip",
        "brand": "Apple",
        "price": Decimal("89900.00"),
        "compare_at_price": Decimal("99900.00"),
        "description": "Impossibly thin design with brilliant 13.6-inch Liquid Retina display and all-day 18-hour battery.",
        "is_featured": True,
        "specifications": {
            "discount": 10,
            "rating": 4.8,
            "reviews": 1820,
            "stock": 14,
            "processor": "Apple M2 8-core CPU",
            "ram": "8GB Unified Memory",
            "storage": "256GB SSD",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrQ1O3baOT4uRFP6hv_SPrdRL1SRslpbWkLY_9HjWdhQ&s=10",
            ],
        },
    },
    {
        "category_slug": "electronics",
        "subcategory_slug": "audio-speakers",
        "sku": "ELE-JBL-FLP6-BLU",
        "name": "JBL Flip 6 Portable Bluetooth Speaker",
        "slug": "jbl-flip-6-portable-bluetooth-speaker",
        "brand": "JBL",
        "price": Decimal("9999.00"),
        "compare_at_price": Decimal("13999.00"),
        "description": "Waterproof and dustproof portable Bluetooth speaker with bold audio and 12 hours playtime.",
        "is_featured": False,
        "specifications": {
            "discount": 28,
            "rating": 4.5,
            "reviews": 3100,
            "stock": 45,
            "waterproof": "IP67 Waterproof & Dustproof",
            "battery_life": "12 Hours",
            "color": "Ocean Blue",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRADT4xvsBUH5l5s7bybX19G8qvI4M1zFmoQkZwaS17tg&s=10",
            ],
        },
    },

    # -------------------------------------------------------------
    # 3. FASHION (5 Products)
    # -------------------------------------------------------------
    {
        "category_slug": "fashion",
        "subcategory_slug": "mens-shoes",
        "sku": "FAS-NIK-AMAX-01",
        "name": "Nike Air Max",
        "slug": "nike-air-max",
        "brand": "Nike",
        "price": Decimal("5999.00"),
        "compare_at_price": Decimal("7999.00"),
        "description": "Comfortable and stylish running shoes for everyday use.",
        "is_featured": True,
        "specifications": {
            "discount": 25,
            "rating": 4.4,
            "reviews": 760,
            "stock": 12,
            "gender": "Men",
            "sole_material": "Air Max Cushioning Rubber",
            "closure": "Lace-Up",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLOutL4UBAFc9zrD_cxbMUqsVjXep4ROdoyNMTRSVvEw&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjXnRjk5RsbQV5y29QO9yP2MWwopUCxUh7-UHPgOuVTg&s=10",
            ],
        },
    },
    {
        "category_slug": "fashion",
        "subcategory_slug": "mens-clothing",
        "sku": "FAS-LEV-JEAN-511",
        "name": "Levi's Men's Jeans",
        "slug": "levis-mens-jeans",
        "brand": "Levi's",
        "price": Decimal("2499.00"),
        "compare_at_price": Decimal("3999.00"),
        "description": "Regular fit denim jeans suitable for casual everyday use.",
        "is_featured": True,
        "specifications": {
            "discount": 38,
            "rating": 4.3,
            "reviews": 430,
            "stock": 30,
            "fit": "Regular Fit",
            "fabric": "99% Cotton, 1% Elastane",
            "waist_rise": "Mid Rise",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQoOD8T4HUEsIkSDVOmKsTr5_BpFf3370erDS5gy3aUQ&s",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgJW7dOttY0lg1gKz4w7cQmb0c1pZhxHPumPkes8G2YA&s=10",
            ],
        },
    },
    {
        "category_slug": "fashion",
        "subcategory_slug": "mens-clothing",
        "sku": "FAS-PUM-TSHIRT-01",
        "name": "Puma T-Shirt",
        "slug": "puma-t-shirt",
        "brand": "Puma",
        "price": Decimal("999.00"),
        "compare_at_price": Decimal("1799.00"),
        "description": "Comfortable cotton regular-fit T-shirt.",
        "is_featured": False,
        "specifications": {
            "discount": 44,
            "rating": 4.2,
            "reviews": 890,
            "stock": 35,
            "material": "100% Cotton",
            "sleeve": "Short Sleeve",
            "neck": "Crew Neck",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBvcYxl4QD3PQfvt6TZhh8oKOFH783WmifG7No0in2ww&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVOG-iK0wFox1axtpmM09y1og4Y_kGbjrOh5vyqXHdUw&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-UNovnNT8JXb8NG15Ye9pqQbM19tD2mQmahAGecixIw&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXCfRc9_tM8k420TDYHaozwIsgPeQu5w0nQAmbG7253Q&s=10",
            ],
        },
    },
    {
        "category_slug": "fashion",
        "subcategory_slug": "mens-shoes",
        "sku": "FAS-ADI-UBL-01",
        "name": "Adidas Ultraboost Light Running Shoes",
        "slug": "adidas-ultraboost-light-running-shoes",
        "brand": "Adidas",
        "price": Decimal("11999.00"),
        "compare_at_price": Decimal("17999.00"),
        "description": "Lightest Ultraboost ever made with energy-returning Light BOOST cushioning and Primeknit upper.",
        "is_featured": True,
        "specifications": {
            "discount": 33,
            "rating": 4.6,
            "reviews": 510,
            "stock": 16,
            "cushioning": "Light BOOST midsole",
            "outsole": "Continental Better Rubber",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLOutL4UBAFc9zrD_cxbMUqsVjXep4ROdoyNMTRSVvEw&s=10",
            ],
        },
    },
    {
        "category_slug": "fashion",
        "subcategory_slug": "mens-clothing",
        "sku": "FAS-ZAR-SHT-LIN",
        "name": "Zara Men's Slim Fit Linen Shirt",
        "slug": "zara-mens-slim-fit-linen-shirt",
        "brand": "Zara",
        "price": Decimal("2990.00"),
        "compare_at_price": Decimal("3990.00"),
        "description": "Breathable 100% pure linen casual button-down shirt with a modern tailored cut.",
        "is_featured": False,
        "specifications": {
            "discount": 25,
            "rating": 4.3,
            "reviews": 320,
            "stock": 28,
            "fabric": "100% Pure Linen",
            "fit": "Slim Fit",
            "color": "Soft White",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBvcYxl4QD3PQfvt6TZhh8oKOFH783WmifG7No0in2ww&s=10",
            ],
        },
    },

    # -------------------------------------------------------------
    # 4. HOME & KITCHEN (5 Products)
    # -------------------------------------------------------------
    {
        "category_slug": "home-kitchen",
        "subcategory_slug": "kitchen-appliances",
        "sku": "HOK-PRE-KET-15L",
        "name": "Prestige Electric Kettle",
        "slug": "prestige-electric-kettle",
        "brand": "Prestige",
        "price": Decimal("1299.00"),
        "compare_at_price": Decimal("1999.00"),
        "description": "Stainless steel electric kettle with automatic shut-off.",
        "is_featured": True,
        "specifications": {
            "discount": 35,
            "rating": 4.1,
            "reviews": 2100,
            "stock": 40,
            "capacity": "1.5 Litres",
            "power": "1500 Watts",
            "material": "Stainless Steel",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmILCN2lmTK8WN5bV9o-MWeWumQTHNtyjZb1S97r6BDw&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTiC_vClXNlI_1WSkvmLdYyJbNQmtXE8kSRPVc6Fb_YA&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRL4GhKQnU4NJ0KXuMgQTCk4w1InLggAVDbbYNekElvIA&s=10",
            ],
        },
    },
    {
        "category_slug": "home-kitchen",
        "subcategory_slug": "kitchen-dining",
        "sku": "HOK-MLT-BOT-1000",
        "name": "Milton Water Bottle",
        "slug": "milton-water-bottle",
        "brand": "Milton",
        "price": Decimal("599.00"),
        "compare_at_price": Decimal("899.00"),
        "description": "Durable stainless steel water bottle for everyday use.",
        "is_featured": True,
        "specifications": {
            "discount": 33,
            "rating": 4.5,
            "reviews": 1800,
            "stock": 60,
            "capacity": "1000 ml",
            "insulation": "Single Wall Stainless Steel",
            "leak_proof": True,
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQart6BRqiIXClwLnojPyI3BX90dcZBm_Apl0TIAwaSoQ&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6-_TUgx7xpLzx-fUk4JnTUced3P5Z3vLmDRlfitmYQg&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8BTwJKRAq6hj9AMi5oKy6r6gDDXUeBFvCplMngxADgg&s=10",
            ],
        },
    },
    {
        "category_slug": "home-kitchen",
        "subcategory_slug": "kitchen-appliances",
        "sku": "HOK-PHI-AF-9252",
        "name": "Philips Digital Air Fryer HD9252",
        "slug": "philips-digital-air-fryer-hd9252",
        "brand": "Philips",
        "price": Decimal("7999.00"),
        "compare_at_price": Decimal("11995.00"),
        "description": "Rapid Air technology with digital touchscreen and 7 preset cooking modes for 90% less fat cooking.",
        "is_featured": True,
        "specifications": {
            "discount": 33,
            "rating": 4.5,
            "reviews": 1420,
            "stock": 25,
            "capacity": "4.1 Litres",
            "power": "1400 Watts",
            "presets": "7 Preset Programs",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmILCN2lmTK8WN5bV9o-MWeWumQTHNtyjZb1S97r6BDw&s=10",
            ],
        },
    },
    {
        "category_slug": "home-kitchen",
        "subcategory_slug": "cookware",
        "sku": "HOK-HAW-PC-3L",
        "name": "Hawkins Stainless Steel Pressure Cooker 3L",
        "slug": "hawkins-stainless-steel-pressure-cooker-3l",
        "brand": "Hawkins",
        "price": Decimal("2450.00"),
        "compare_at_price": Decimal("2950.00"),
        "description": "Food-grade stainless steel pressure cooker with thick sandwich bottom for even heating on gas and induction.",
        "is_featured": False,
        "specifications": {
            "discount": 17,
            "rating": 4.6,
            "reviews": 3890,
            "stock": 50,
            "capacity": "3 Litres",
            "base_type": "Induction & Gas Compatible",
            "warranty": "5 Years",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQart6BRqiIXClwLnojPyI3BX90dcZBm_Apl0TIAwaSoQ&s=10",
            ],
        },
    },
    {
        "category_slug": "home-kitchen",
        "subcategory_slug": "kitchen-appliances",
        "sku": "HOK-WND-NTR-400",
        "name": "Wonderchef Nutri-blend Mixer Grinder 400W",
        "slug": "wonderchef-nutri-blend-mixer-grinder",
        "brand": "Wonderchef",
        "price": Decimal("2799.00"),
        "compare_at_price": Decimal("5000.00"),
        "description": "Compact high-speed mixer-grinder with surgical grade blades for nutrient extraction, smoothies, and masalas.",
        "is_featured": False,
        "specifications": {
            "discount": 44,
            "rating": 4.3,
            "reviews": 2780,
            "stock": 35,
            "motor_power": "400 Watts 22000 RPM",
            "jars": "2 Unbreakable Polycarbonate Jars",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRL4GhKQnU4NJ0KXuMgQTCk4w1InLggAVDbbYNekElvIA&s=10",
            ],
        },
    },

    # -------------------------------------------------------------
    # 5. BEAUTY (5 Products)
    # -------------------------------------------------------------
    {
        "category_slug": "beauty",
        "subcategory_slug": "skin-care",
        "sku": "BEA-LAK-CR-PEACH",
        "name": "Lakme Face Cream",
        "slug": "lakme-face-cream",
        "brand": "Lakme",
        "price": Decimal("399.00"),
        "compare_at_price": Decimal("499.00"),
        "description": "Daily moisturizing face cream suitable for regular use.",
        "is_featured": True,
        "specifications": {
            "discount": 20,
            "rating": 4.3,
            "reviews": 3200,
            "stock": 75,
            "net_weight": "100g",
            "skin_type": "All Skin Types",
            "benefits": "Deep Hydration and Radiance",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCNXAfO-4U_x1f57jC-0qfoCrxD3uI3JhD4sGH7_2Vag&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7BKCzs0s6UpJ5kg0yrLNWeKPXpriJOFSUTFvnIVVZVA&s=10",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLox7r3CyRVgUbCnttUQ9QSvN5GMNhr6Io-UqsoVzKUg&s=10",
            ],
        },
    },
    {
        "category_slug": "beauty",
        "subcategory_slug": "makeup",
        "sku": "BEA-MAY-LIP-SED",
        "name": "Maybelline Super Stay Matte Ink Lipstick",
        "slug": "maybelline-super-stay-matte-ink-lipstick",
        "brand": "Maybelline",
        "price": Decimal("549.00"),
        "compare_at_price": Decimal("699.00"),
        "description": "Long-lasting flawless matte liquid lipstick with up to 16HR wear that won't smudge or transfer.",
        "is_featured": True,
        "specifications": {
            "discount": 21,
            "rating": 4.4,
            "reviews": 4600,
            "stock": 80,
            "finish": "Flawless Matte",
            "wear_time": "Up to 16 Hours",
            "shade": "65 Seductress",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7BKCzs0s6UpJ5kg0yrLNWeKPXpriJOFSUTFvnIVVZVA&s=10",
            ],
        },
    },
    {
        "category_slug": "beauty",
        "subcategory_slug": "skin-care",
        "sku": "BEA-LOR-SRM-HA",
        "name": "L'Oréal Paris Revitalift 1.5% Hyaluronic Acid Serum",
        "slug": "loreal-paris-revitalift-hyaluronic-acid-serum",
        "brand": "L'Oréal",
        "price": Decimal("699.00"),
        "compare_at_price": Decimal("999.00"),
        "description": "Lightweight face serum with 1.5% pure Hyaluronic Acid for intensely hydrated, radiant, youthful skin.",
        "is_featured": True,
        "specifications": {
            "discount": 30,
            "rating": 4.5,
            "reviews": 5120,
            "stock": 65,
            "volume": "30ml",
            "key_ingredient": "1.5% Pure Hyaluronic Acid",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCNXAfO-4U_x1f57jC-0qfoCrxD3uI3JhD4sGH7_2Vag&s=10",
            ],
        },
    },
    {
        "category_slug": "beauty",
        "subcategory_slug": "skin-care",
        "sku": "BEA-NIV-SFT-200",
        "name": "Nivea Soft Light Moisturizing Cream 200ml",
        "slug": "nivea-soft-light-moisturizing-cream",
        "brand": "Nivea",
        "price": Decimal("299.00"),
        "compare_at_price": Decimal("450.00"),
        "description": "Refreshing moisturizing cream with Jojoba Oil and Vitamin E for soft, smooth, healthy skin.",
        "is_featured": False,
        "specifications": {
            "discount": 33,
            "rating": 4.5,
            "reviews": 6400,
            "stock": 90,
            "volume": "200ml",
            "ingredients": "Jojoba Oil & Vitamin E",
            "texture": "Non-Greasy Fast Absorbing",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLox7r3CyRVgUbCnttUQ9QSvN5GMNhr6Io-UqsoVzKUg&s=10",
            ],
        },
    },
    {
        "category_slug": "beauty",
        "subcategory_slug": "skin-care",
        "sku": "BEA-ORD-NIA-30",
        "name": "The Ordinary Niacinamide 10% + Zinc 1% Serum",
        "slug": "the-ordinary-niacinamide-10-zinc-1",
        "brand": "The Ordinary",
        "price": Decimal("600.00"),
        "compare_at_price": Decimal("750.00"),
        "description": "High-strength vitamin and mineral blemish formula to reduce blemishes, balance sebum activity, and smooth texture.",
        "is_featured": False,
        "specifications": {
            "discount": 20,
            "rating": 4.6,
            "reviews": 7800,
            "stock": 55,
            "volume": "30ml",
            "actives": "10% Niacinamide + 1% Zinc PCA",
            "skin_concern": "Blemishes, Enlarged Pores, Oiliness",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7BKCzs0s6UpJ5kg0yrLNWeKPXpriJOFSUTFvnIVVZVA&s=10",
            ],
        },
    },
]


def seed_database():
    db = SessionLocal()
    try:
        logger.info("Starting database seeding...")

        # 1. Seed Categories & SubCategories
        category_map = {}
        subcategory_map = {}

        for cat_data in CATEGORIES_DATA:
            category = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not category:
                category = Category(
                    name=cat_data["name"],
                    slug=cat_data["slug"],
                    description=cat_data.get("description"),
                    image_url=cat_data.get("image_url"),
                    is_active=True,
                )
                db.add(category)
                db.flush()
                logger.info(f"Created category: {category.name} (id={category.id})")
            else:
                logger.info(f"Category already exists: {category.name} (id={category.id})")

            category_map[cat_data["slug"]] = category

            # Seed subcategories
            for sub_data in cat_data.get("subcategories", []):
                subcategory = (
                    db.query(SubCategory)
                    .filter(
                        SubCategory.slug == sub_data["slug"],
                        SubCategory.category_id == category.id,
                    )
                    .first()
                )
                if not subcategory:
                    subcategory = SubCategory(
                        category_id=category.id,
                        name=sub_data["name"],
                        slug=sub_data["slug"],
                        description=sub_data.get("description"),
                        is_active=True,
                    )
                    db.add(subcategory)
                    db.flush()
                    logger.info(f"  Created subcategory: {subcategory.name} (id={subcategory.id})")
                else:
                    logger.info(f"  Subcategory already exists: {subcategory.name}")

                subcategory_map[(cat_data["slug"], sub_data["slug"])] = subcategory

        # 2. Seed Products
        inserted_count = 0
        updated_count = 0

        for p_data in PRODUCTS_DATA:
            cat_slug = p_data["category_slug"]
            sub_slug = p_data["subcategory_slug"]

            category = category_map[cat_slug]
            subcategory = subcategory_map[(cat_slug, sub_slug)]

            # Check existing by SKU or Slug
            existing_product = (
                db.query(Product)
                .filter((Product.sku == p_data["sku"]) | (Product.slug == p_data["slug"]))
                .first()
            )

            if existing_product:
                existing_product.category_id = category.id
                existing_product.sub_category_id = subcategory.id
                existing_product.sku = p_data["sku"]
                existing_product.name = p_data["name"]
                existing_product.slug = p_data["slug"]
                existing_product.brand = p_data.get("brand")
                existing_product.price = p_data["price"]
                existing_product.compare_at_price = p_data.get("compare_at_price")
                existing_product.description = p_data.get("description")
                existing_product.specifications = p_data.get("specifications")
                existing_product.is_featured = p_data.get("is_featured", False)
                existing_product.status = "active"
                updated_count += 1
                logger.info(f"Updated product: {existing_product.name} (SKU: {existing_product.sku})")
            else:
                product = Product(
                    category_id=category.id,
                    sub_category_id=subcategory.id,
                    sku=p_data["sku"],
                    name=p_data["name"],
                    slug=p_data["slug"],
                    brand=p_data.get("brand"),
                    price=p_data["price"],
                    compare_at_price=p_data.get("compare_at_price"),
                    description=p_data.get("description"),
                    specifications=p_data.get("specifications"),
                    is_featured=p_data.get("is_featured", False),
                    status="active",
                )
                db.add(product)
                inserted_count += 1
                logger.info(f"Inserted product: {product.name} (SKU: {product.sku})")

        db.commit()
        logger.info(
            f"Seeding completed successfully! Inserted: {inserted_count}, Updated: {updated_count}"
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Error during seeding: {e}", exc_info=True)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
