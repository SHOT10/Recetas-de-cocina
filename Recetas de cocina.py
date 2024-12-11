import sqlite3
import sys

def create_database():
    connection = sqlite3.connect('recipes.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        ingredients TEXT NOT NULL,
        steps TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def add_recipe():
    name = input("Enter recipe name: ").strip()
    if not name:
        print("Recipe name cannot be empty.")
        return

    ingredients = input("Enter ingredients (comma-separated): ").strip()
    if not ingredients:
        print("Ingredients cannot be empty.")
        return

    steps = input("Enter steps (separated by periods): ").strip()
    if not steps:
        print("Steps cannot be empty.")
        return

    connection = sqlite3.connect('recipes.db')
    cursor = connection.cursor()

    try:
        cursor.execute('''INSERT INTO recipes (name, ingredients, steps) VALUES (?, ?, ?)''', (name, ingredients, steps))
        connection.commit()
        print("Recipe added successfully.")
    except sqlite3.IntegrityError:
        print("A recipe with that name already exists.")
    finally:
        connection.close()

def update_recipe():
    name = input("Enter the name of the recipe to update: ").strip()
    if not name:
        print("Recipe name cannot be empty.")
        return

    connection = sqlite3.connect('recipes.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM recipes WHERE name = ?''', (name,))
    recipe = cursor.fetchone()

    if recipe:
        new_name = input("Enter new recipe name (leave blank to keep current): ").strip()
        new_ingredients = input("Enter new ingredients (leave blank to keep current): ").strip()
        new_steps = input("Enter new steps (leave blank to keep current): ").strip()

        updated_name = new_name if new_name else recipe[1]
        updated_ingredients = new_ingredients if new_ingredients else recipe[2]
        updated_steps = new_steps if new_steps else recipe[3]

        cursor.execute('''UPDATE recipes SET name = ?, ingredients = ?, steps = ? WHERE id = ?''',
                       (updated_name, updated_ingredients, updated_steps, recipe[0]))
        connection.commit()
        print("Recipe updated successfully.")
    else:
        print("Recipe not found.")

    connection.close()

def delete_recipe():
    name = input("Enter the name of the recipe to delete: ").strip()
    if not name:
        print("Recipe name cannot be empty.")
        return

    connection = sqlite3.connect('recipes.db')
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM recipes WHERE name = ?''', (name,))
    connection.commit()

    if cursor.rowcount > 0:
        print("Recipe deleted successfully.")
    else:
        print("Recipe not found.")

    connection.close()

def list_recipes():
    connection = sqlite3.connect('recipes.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT name FROM recipes''')
    recipes = cursor.fetchall()

    if recipes:
        print("\nList of Recipes:")
        for recipe in recipes:
            print(f"- {recipe[0]}")
    else:
        print("No recipes found.")

    connection.close()

def view_recipe():
    name = input("Enter the name of the recipe to view: ").strip()
    if not name:
        print("Recipe name cannot be empty.")
        return

    connection = sqlite3.connect('recipes.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT ingredients, steps FROM recipes WHERE name = ?''', (name,))
    recipe = cursor.fetchone()

    if recipe:
        print("\nIngredients:")
        print(recipe[0])
        print("\nSteps:")
        print(recipe[1])
    else:
        print("Recipe not found.")

    connection.close()

def main():
    create_database()

    while True:
        print("\nRecipe Book")
        print("1. Add New Recipe")
        print("2. Update Recipe")
        print("3. Delete Recipe")
        print("4. List Recipes")
        print("5. View Recipe")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_recipe()
        elif choice == '2':
            update_recipe()
        elif choice == '3':
            delete_recipe()
        elif choice == '4':
            list_recipes()
        elif choice == '5':
            view_recipe()
        elif choice == '6':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()