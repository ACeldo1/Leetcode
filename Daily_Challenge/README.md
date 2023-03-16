## Table of Contents
1. [{{ question_name }}](#{{ question_name_link }})
	- Link
	- Description
	- Test Cases
	- Related Topics
2. [Code](#Code)
	- Explanation
	- Code
3. [Notes](#Notes)

## {{ question_name }}
#### <a href="{{ link_to_problem }}"> Link to Problem</a>
## {{ date }}

### Description
Difficulty: <p style="background-color:{{ difficulty_color }}">{{ difficulty }}</p>

{{ description }}

Topic Tags: {% for topic in related_topics %}{{ topic[1].name }}{% if topic[0] != related_topics_len-1 %},{%endif%} {%endfor%}
	
### Code
	{{ explanation }}
	'''{{ code_block }}'''

### Notes
	* 