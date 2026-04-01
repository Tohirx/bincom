from bs4 import BeautifulSoup
from collections import Counter
import statistics
import psycopg2


html = """<table>
	
	<thead>
		<th>DAY</th><th>COLOURS</th>
	</thead>
	<tbody>
	<tr>
		<td>MONDAY</td>
		<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
	</tr>
	<tr>
		<td>TUESDAY</td>
		<td>ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLUE, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE</td>
	</tr>
	<tr>
		<td>WEDNESDAY</td>
		<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE</td>
	</tr>
	<tr>
		<td>THURSDAY</td>
		<td>BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
	</tr>
	<tr>
		<td>FRIDAY</td>
		<td>GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE</td>
	</tr>

	</tbody>
</table>"""

# Parse the html
soup = BeautifulSoup(html, "html.parser")

# Extract the rows
rows = soup.find("tbody").find_all("tr")

# for each row, access cell 1 to find the colours.
# for each colour in cell 1, extract the text, and split it around the comma delimeter
# append each colour to colours
# extend the all_colours list with new colours

all_colours = []
for row in rows:
    cell = row.find_all("td")
    colours = []
    for c in cell[1].text.split(","):
        colours.append(c.strip())

    all_colours.extend(colours)


# Frequency count 
colour_counts = Counter(all_colours)


# Q1: Mean colour
# Assign numeric values to each unique colour alphabetically, compute mean index
sorted_colours = sorted(set(all_colours))
colour_to_num = {colour: i for i, colour in enumerate(sorted_colours)}
num_to_colour = {i: colour for colour, i in colour_to_num.items()}
 
numeric_values = [colour_to_num[c] for c in all_colours]
mean_value = statistics.mean(numeric_values)
mean_index = round(mean_value)
mean_colour = num_to_colour[mean_index]
 
print(f"Q1 - Mean colour (by alphabetical numeric mapping):")
print(f"     Numeric mean = {mean_value:.2f}  =  '{mean_colour}'\n")
 
# Q2: Most worn colour (mode)
most_common_colour, most_common_count = colour_counts.most_common(1)[0]
print(f"Q2 - Most worn colour throughout the week:")
print(f"     '{most_common_colour}' worn {most_common_count} times\n")
 
# Q3: Median colour
sorted_numeric = sorted(numeric_values)
median_value = statistics.median(sorted_numeric)
median_index = int(median_value)
median_colour = num_to_colour[median_index]
 
print(f"Q3 - Median colour (by alphabetical numeric mapping):")
print(f"     Median numeric value = {median_value}  =  '{median_colour}'\n")
 
# BONUS Q4: Variance of colours
variance = statistics.variance(numeric_values)
print(f"Q4 (Bonus) - Variance of colour values:")
print(f"     Variance = {variance:.4f}\n")
 
# BONUS Q5: Probability of RED
red_count = colour_counts.get("RED", 0)
total = len(all_colours)
probability_red = red_count / total
 
print(f"Q5 (Bonus) - Probability that a randomly chosen colour is RED:")
print(f"     RED appears {red_count} times out of {total} total")
print(f"     P(RED) = {red_count}/{total} = {probability_red:.4f} ({probability_red*100:.2f}%)")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="your_database",
    user="your_username",
    password="your_password",
    port="5432"
)

cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS colour_frequencies (
        id        SERIAL PRIMARY KEY,
        colour    VARCHAR(50) UNIQUE NOT NULL,
        frequency INTEGER NOT NULL
    )
""")

# Insert colours and frequencies
for colour, count in colour_counts.items():
    cursor.execute("""
        INSERT INTO colour_frequencies (colour, frequency)
        VALUES (%s, %s)
        ON CONFLICT (colour) DO UPDATE
            SET frequency = EXCLUDED.frequency
    """, (colour, count))

# Commit and close
conn.commit()
cursor.close()
conn.close()
