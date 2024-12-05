# We are doing the 2nd project
# We have made so it allows users to search for recipes based on a main ingredient,
# optional course type, and cuisine type.
# It interacts with the Edamam API to fetch and display recipes that match the user’s criteria.



# 1. User Input:
# Prompts the user for a main ingredient.
# Allows optional input for course (Starter, Main Course, Desserts).
# Allows optional input for cuisine.

import requests
from pprint import pprint
# This version v5 incorporates Anna's cuisine choice code as well as making course and cuisine optional, and adds error message for unknown cuisineType

# asks user for ingredient, .strip strips any extra spaces before and after input text
# .lower converts any answers into lower case so they have a better chance of matching the acceptable inputs lists
ingredient = input("What's your main ingredient? ").strip().lower()
course = input("What course? Enter Starter/Main course/Desserts, or press return for none ").strip().lower()
cuisine = input("What cuisine? Press return for none ").strip().lower()


# 2. Input Validation:
# Checks if the entered course and cuisine are among the acceptable values.
# Provides error messages for invalid inputs.

# Course names too specific to allow completely free text field here
# Acceptable courses list avoids errors for now, not ideal would like better way
# Include an empty string in the allowed values for "no value selected", means is optional for user now
acceptable_courses = ["starter", "main course", "desserts", ""]
if course not in acceptable_courses:
    print("Unknown course, please press run and try again")
    exit()

# Defines acceptable cuisine inputs, so we can give an error message if cuisine not on it
# e.g. Thai is not on the Edamam list
acceptable_cuisines = [
    "american",
    "asian",
    "british",
    "caribbean",
    "central europe",
    "chinese",
    "eastern europe",
    "french",
    "indian",
    "italian",
    "japanese",
    "kosher",
    "mediterranean",
    "mexican",
    "middle eastern",
    "nordic",
    "south american",
    "south east asian",
    ""
    ]

# Outputs error message if cuisine not on Edamam CuisineType list, prompts user to choose another
# and provides list of acceptable answers
# Edamam list format is not the best, not consistent e.g. 'Chinese' but 'Eastern Europe' (not 'European'
if cuisine not in acceptable_cuisines:
    print("Cuisine type not on list, options are: ")
    # (I googled to find how to do this bit, not entirely sure what the * is doing, possibly looping through the list and printing as it goes? - Sophie"
    print(*acceptable_cuisines, sep = "\n")
    exit()



# 3. API Interaction:
# Constructs a URL to query the Edamam API using the user’s inputs.
# Fetches recipe data based on the constructed URL.

# Variables for Application ID and Application Key for Edamam API
# Insert your own ID and key in these strings
application_id = "08bacac5"
application_key = "75c27b69253bfcca20ec7350fd0356f7"

# Dictionary that defines search parameters for constructing the API call url
my_search_parameters = {
    "type" : "public",
    "q" : ingredient,
    "dishType" : course,
    "cuisineType": cuisine,
    "app_id" : application_id,
    "app_key" : application_key

}

# Function to construct a url based on user input and search parameters
# 'params' = telling the function it will be using parameters here (could have multiple sets)
# when call the function later, define which parameters it is calling, in this case 'my_search_parameters'
def get_url(params):
    base_url = "https://api.edamam.com/api/recipes/v2"
    dish_type = params["dishType"]
    dish_type_query = f"&dishType={dish_type}" if (dish_type != "") else ""
    cuisine_type = params["cuisineType"]
    cuisine_type_query = f"&cuisineType={cuisine_type}" if (cuisine_type != "") else ""
    return f"{base_url}?type={params["type"]}&q={params["q"]}{dish_type_query}{cuisine_type_query}&app_id={params["app_id"]}&app_key={params["app_key"]}"

# constructs url by calling the function above
# E.g. https://api.edamam.com/api/recipes/v2?type=public&q=chicken&dishType=Starter&app_id=abc&app_key=123
url = get_url(my_search_parameters)
# optional, to print the url and check how many results it returns etc.
# print(url)



# 4. Display Results:
# Outputs the recipe labels, ingredient lists, and URLs to the user.

# Get the returned recipes from the API response
response = requests.get(url)

# Checks that the url constructed is functional. Outputs error code if not.
if response.status_code >= 200 and response.status_code < 300:
    results = response.json()
    # optional, to search through results and work out which parts to pull out
    # pprint(results)
    hit_results = results['hits']
    for i in hit_results:
        print(i['recipe']['label'], "\n", i['recipe']['ingredientLines'],"\n",  i['recipe']['url'])
        print('---------------')
        print('          ')
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")