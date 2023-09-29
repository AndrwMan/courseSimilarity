#import PyPDF2		#pdf text extraction
import pdfplumber	#pdf text extraction
import re			#regular expressions

'''
Extract courses from pdf
'''
raw_pdf_file = './academicHistory_9-28-23.pdf'
pdf = pdfplumber.open(raw_pdf_file)

# Initialize a variable to store the extracted course information
course_info = []

# Extract text from the PDF
# Iterate through the pages and extract text
for page in pdf.pages:
	page_text = page.extract_text()
      
	#check raw output
	print(page_text)  

	#remove withdrawals, etc. 
	# \s+\d{1,2}\.\d{1,2}: matches for ex: "4.00" after twice
	# (?:F|D|W|NP): matches for letter grades, non-capturing group 
	bad_pattern = r'\b[A-Z]{3,4} \d{1,3}[A-Za-z]? [A-Za-z.:&/\s]+(?:\s+\d{1,2}\.\d{1,2}\s+)?(?:F|D|W|NP)\s+\d{1,2}\.\d{1,2}(?: [A-Za-z.:&/\s]+)?\n?'
	page_text = re.sub(bad_pattern, '', page_text)
      
	#Define raw string literal/regular expression pattern,
	# course codes start w/ 3-4 letters
	# then 1-3 digits (numbers) 
	# a single (optional) sequence indicator
	#  '.' for ex: CSE 151A Intro to Machine Learning
	# lastly course title which have atleast 1 char
	#  that is any combination of alphabets, '&', '.', ':'
	# '.' for ex: CSE 11 Accel. Intro to Programming
	# ':' for ex: ETHN 2 Intro:CirculationsofDifference
	# '/' for ex: MATH 171 Intro Num Optimiz/Linear Prog

	pattern = r'\b[A-Z]{3,4} \d{1,3}[A-Za-z]? [A-Za-z.:&/\s]+'
	
	# Find all matches in the page text
	matches = re.findall(pattern, page_text)
	
	# Add all of a page's matched course information to the list
	course_info.extend(matches)

# Close the PDF file
pdf.close()

#check course signatures
for course in course_info:
    print(course)
    

'''
CLI to prompt user to finetune course info
'''
#TODO: add gui to remove courses,
#CLI to remove courses,
# for current quarter may plan to drop but won't 
# reflect in transcript until officially dropped
def remove_course(course_code):
	#can probably just use global
	global course_info
	#Case sensitive match (to be sure of decision)
	updated_course_info = [course for course in course_info if not course.startswith(course_code)]
	removed_count = len(course_info) - len(updated_course_info)
	course_info = updated_course_info
	return removed_count

while True:
	# Print enrolled and finished courses
	print("\nEnrolled Courses:")
	for course in course_info:
		print(course)

	# Prompt the user to enter a course code to remove
	#  remove whitespace
	course_code = input("\nEnter a course code to remove (e.g., CSE 150B), or type 'q' to quit: ").strip()

	# Check if the user wants to quit
	if course_code.lower() == 'q':
		break

	# Remove the specified course by course code
	removed_count = remove_course(course_code)

	if removed_count > 0:	
		# Print the number of removed courses
		print(f"Removed {removed_count} courses with code '{course_code}'.")
	else:
		print(f"No matches found for '{course_code}'. Course not removed.")

# print the updated course_info after making all the changes
print("\nUpdated Course Information:")
for course in course_info:
    print(course)

'''
Store List in File (to be used by other scripts)
'''









