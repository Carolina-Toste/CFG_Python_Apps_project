import requests  # import library used to send HTTP requests

APP_ID = 'bc0d8d5e'  # my APP_ID
APP_KEY = '7dbf3165f2ce9ab03264acfa7c9994f7'  # my APP_KEY


def get_allergies():  # Define function that lists predefined allergies
    # Return predefined allergies to user that are present in edamam API
    return [
        "Gluten",
        "Dairy",
        "Eggs",
        "Soy",
        "Wheat",
        "Fish",
        "Shellfish",
        "Tree Nuts",
        "Peanuts"
    ]


# recipe_search constructs the API request URL with the specified ingredient and allergy
def recipe_search(ingredient, allergy):
    # If there's an allergy, append "-free" to it
    if allergy:
        allergy += "-Free"

    # Construct the API request URL with the specified ingredient and allergy
    url = f'https://api.edamam.com/search?q={ingredient}&app_id={APP_ID}&app_key={APP_KEY}&allergy={allergy}'

    result = requests.get(url)

    # Check if the API request was successful (status code 200)
    if result.status_code != 200:
        print(f"Failed to retrieve recipes. API returned status code: {result.status_code}")
        return []

    data = result.json()

    # Filter recipes based on healthLabels if an allergy is specified
    if allergy:
        filtered_hits = [hit for hit in data.get('hits', []) if allergy in hit['recipe']['healthLabels']]
        return filtered_hits
    else:
        return data.get('hits', [])


# run function prompts the user for the ingredient and whether they have allergies
def run():
    ingredient = input('What ingredient would you like to search for? ')
    allergy_input = input('Do you have any allergies? (yes/no): ')

    if allergy_input.lower() == 'yes':
        # Fetch and display allergies from get_allergies function
        allergies = get_allergies()
        print("Allergies:")
        for idx, allergy in enumerate(allergies, start=1):
            print(f"{idx}. {allergy}")

        choice = input("Enter the number for your allergy or 'none' for no specific allergy: ")

        if choice.lower() == 'none':
            allergy = None
        elif choice.isdigit() and 1 <= int(choice) <= len(allergies):
            allergy = allergies[int(choice) - 1]
        else:
            print("Invalid choice. Exiting.")
            return
    else:
        allergy = None

    if allergy:
        print(f"Here is a list of recipes with {ingredient} that are {allergy} free:")
    else:
        print(f"Here's a list of recipes with {ingredient}:")

    results = recipe_search(ingredient, allergy)  # call recipe_search function to get the recipe results

    if not results:
        print(f"No recipes found for {ingredient}. Please try another ingredient.")
    else:
        for i, result in enumerate(results, start=1):  # if there are results call print_recipe function
            recipe = result['recipe']
            print_recipe(recipe)


def print_recipe(recipe):  # print_recipe function takes recipe and prints
    print(recipe['label'])  # print recipe name
    print(recipe['uri'])  # print recipe link
    print(recipe['mealType'])  # print the type of meal - eg. lunch/dinner , brunch
    print(recipe['healthLabels'])  # print Health Labels - Peanut Free, etc
    print()

    # then saves it to a recipes.txt #with ensures file is closed after writing;
    with open('recipes.txt', 'a+') as recipes_file:  # 'a+' is append and read mode.
        recipes_file.write(f"Recipe Name: {recipe['label']}\n")
        recipes_file.write(f"Recipe Link: {recipe['uri']}\n")
        recipes_file.write(f"Meal Type: {recipe['mealType']}\n")
        recipes_file.write(f"Health Labels: {', '.join(recipe['healthLabels'])}\n\n")


if __name__ == "__main__":  # Checks if script is being run as the main program and if it is, calls the function run()
    run()
