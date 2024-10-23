import env
import requests
ingredient = input("What's your main ingredient? ").strip().lower()
course = input("What course? Enter Starter/Main course/Desserts, or press return for none ").strip().lower()
cuisine = input("What cuisine? Press return for none ").strip().lower()

acceptable_courses = ["starter", "main course", "desserts", ""]
if course not in acceptable_courses:
    print("Unknown course, please press run and try again")
    exit()

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

if cuisine not in acceptable_cuisines:
    print("Cuisine type not on list, options are: ")
    print(*acceptable_cuisines, sep = "\n")
    exit()

application_id = env.application_id
application_key = env.application_key

my_search_parameters = {
    "type" : "public",
    "q" : ingredient,
    "dishType" : course,
    "cuisineType": cuisine,
    "app_id" : application_id,
    "app_key" : application_key

}

def get_url(params):
    base_url = "https://api.edamam.com/api/recipes/v2"
    dish_type = params["dishType"]
    dish_type_query = f"&dishType={dish_type}" if (dish_type != "") else ""
    cuisine_type = params["cuisineType"]
    cuisine_type_query = f"&cuisineType={cuisine_type}" if (cuisine_type != "") else ""
    return f"{base_url}?type={params["type"]}&q={params["q"]}{dish_type_query}{cuisine_type_query}&app_id={params["app_id"]}&app_key={params["app_key"]}"

url = get_url(my_search_parameters)

response = requests.get(url)

if response.status_code >= 200 and response.status_code < 300:
    results = response.json()
    hit_results = results['hits']
    for i in hit_results:
        print(i['recipe']['label'], "\n", i['recipe']['ingredientLines'],"\n",  i['recipe']['url'])
        print('---------------')
        print('          ')
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")