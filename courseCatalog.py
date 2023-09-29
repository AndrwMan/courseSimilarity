from bs4 import BeautifulSoup
import requests
from courseTaken import course_info 

'''
Specify websites to scrap
'''
# split string by space then recombine first two substrs w/ space
my_course_codes = [' '.join(course.split()[:2]) for course in course_info]
#debug: 
#print("course codes only", my_course_codes)

# programmatically generating the list of website URLs
#  by extracting the distinct dept codes & use as 
#  var in replacement field for format string
department_codes = set(course.split()[0] for course in my_course_codes)
website_urls = [f"https://catalog.ucsd.edu/courses/{code}.html" for code in department_codes]

# manual specifying url for depts catalogs to scrap
# website_urls = ["https://catalog.ucsd.edu/courses/CSE.html", 
# 				'https://catalog.ucsd.edu/courses/ECON.html',
# 				'https://catalog.ucsd.edu/courses/MATH.html',
# 				'https://catalog.ucsd.edu/courses/COGS.html',
# 				'https://catalog.ucsd.edu/courses/MGT.html',
# 				'https://catalog.ucsd.edu/courses/MAE.html',
# 				'https://catalog.ucsd.edu/courses/DOC.html']


'''
Scrap the HTML content 
'''
# cannot extend empty soup object -> 
#  AttributeError: 'NoneType' object has no attribute 'extend'
dummy_html = "<html><head></head><body></body></html>"
all_dept_soup = BeautifulSoup(dummy_html, 'html.parser')
#debug: 
#print(all_dept_soup.prettify())

# Iterate through URLs list & combine the soup objects
for website_url in website_urls:
    # Send an HTTP GET request
	response = requests.get(website_url)

    # Parse the HTML content (soup Object)
	curr_dept_soup = BeautifulSoup(response.text, 'html.parser')
	#debug: need correct encoding to support write of certain chars
	with open("./log.txt", 'a', encoding='utf-8') as file:
		print(curr_dept_soup, file=file)

    # Combine soup objects by extending the body contents
	all_dept_soup.body.extend(curr_dept_soup.body.contents)


# Extract course descriptions
course_descriptions = {}
course_name_elements = all_dept_soup.find_all('p', class_='course-name')
# Theoretically nothing wrong with code, but 
# the actual html structure has inconsisties that cause find_all to not find all
#course_description_elements = all_dept_soup.find_all('p', class_='course-descriptions')

# Use css selectors to find all elements that match criteria
#  Both approaches return ResultSet but .select() can also get description
#  from <p><span class="course-descriptions"> inconsistencies
#course_description_elements = all_dept_soup.select('p.course-descriptions, p span.course-descriptions')

#still there's a second type of inconsistency <p> w/o class="course-descriptions"
# since <p class="course-name"> are always correct 
# and ordered before <p class="course-descriptions"> 
# just select the next p tag which wil be description
course_description_elements = all_dept_soup.select('p.course-name + p')

for course_name_element, course_description_element in zip(course_name_elements, course_description_elements):
	course_name = course_name_element.text.strip()
	course_description = course_description_element.text.strip()
	course_descriptions[course_name] = course_description
	with open("./log2.txt", 'w', encoding='utf-8') as file:
		for c_name in course_descriptions:
			print(c_name, ':', course_descriptions[c_name], file=file)

#course name & description is off by 1 starting from here
#debug: 
#print('\t testing.........\n', course_descriptions['MATH 10A. Calculus I (4)'])

#debug:
#print(course_info)
#my_course_codes = [' '.join(course.split()[:2]) for course in course_info]
#print("course codes only", my_course_codes)

# Store courses descriptions for 
# taken courses that match catalog
matched_course_descriptions = {}

# Match taken courses to course descriptions
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