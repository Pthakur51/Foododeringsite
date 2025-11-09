import sqlite3

def insert_menu_items():
    conn = sqlite3.connect('database/foodie.db')
    cursor = conn.cursor()

    sample_data = [
        # Existing 5 items
        ('Margherita Pizza', 'Classic cheese and tomato pizza', 299.0, 'pizza.jpg', 'Pizza'),
        ('Veg Burger', 'Crispy veggie patty with lettuce and sauce', 149.0, 'burger.jpg', 'Burger'),
        ('Chicken Biryani', 'Spicy rice with chicken', 249.0, 'biryani.jpg', 'Indian'),
        ('Pasta Alfredo', 'Creamy white sauce pasta', 199.0, 'pasta.jpg', 'Pasta'),
        ('Paneer Tikka', 'Grilled paneer with spices', 229.0, 'paneer.jpg', 'Indian'),

        # New 5 items
        ('Pasta Primavera', 'Delicious pasta with vegetables and creamy sauce', 249.0, 'primavera.jpg', 'Pasta'),
        ('Cheese Burger', 'Beef burger with cheese, lettuce, and tomato', 179.0, 'cheeseburger.jpg', 'Burger'),
        ('Veg Tacos', 'Tacos with fresh vegetables, beans, and salsa', 129.0, 'tacos.jpg', 'Mexican'),
        ('Chocolate Lava Cake', 'Chocolate cake with molten center and ice cream', 189.0, 'lava_cake.jpg', 'Dessert'),
        ('Paneer Butter Masala', 'Paneer in creamy tomato gravy', 229.0, 'butter_masala.jpg', 'Indian')
    ]

    cursor.executemany("INSERT INTO menu (name, description, price, image, category) VALUES (?, ?, ?, ?, ?)", sample_data)

    conn.commit()
    conn.close()
    print("All menu items inserted.")

if __name__ == '__main__':
    insert_menu_items()
