from bs4 import BeautifulSoup
import requests
from courseTaken import course_info 

# URL of the website with course descriptions
website_url = "https://catalog.ucsd.edu/courses/CSE.html"

# Send an HTTP GET request
response = requests.get(website_url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())

# Extract course descriptions
course_descriptions = {}
course_name_elements = soup.find_all('p', class_='course-name')
course_description_elements = soup.find_all('p', class_='course-descriptions')

for course_name_element, course_description_element in zip(course_name_elements, course_description_elements):
    course_name = course_name_element.text.strip()
    course_description = course_description_element.text.strip()
    course_descriptions[course_name] = course_description

# recall course_info is a list of course strings
print(course_info)
#my_course_codes = [course.split(".")[0].strip() for course in course_info]
#my_course_codes = [course.split('.')[0].strip().split(' ')[0] for course in course_info]
my_course_codes = [' '.join(course.split()[:2]) for course in course_info]
print("course codes only", my_course_codes)

# Match your courses with descriptions
matched_course_descriptions = {}

# Match course descriptions
#FIXME: substring getting matched giving more results
for course_code, description in course_descriptions.items():
	#print(course_code, '\n', description)
	#Check if any of taken course codes are in course_descriptions keys
	short_course_code = ' '.join(course_code.split()[:2]).rstrip('.')
	for my_course_code in my_course_codes:
		#print(short_course_code)
		if my_course_code == short_course_code:
			#when matched, append course_code:descriptions pairs
			matched_course_descriptions[course_code] = course_descriptions[course_code]

    
print(len(matched_course_descriptions))
for courseDescript in matched_course_descriptions:
	print(courseDescript)
	print(matched_course_descriptions[courseDescript])