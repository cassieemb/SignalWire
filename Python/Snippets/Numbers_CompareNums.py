import csv
import pandas as pd

# List and print all numbers on account
columnB = []
columnA = []
missingFromColumnB = []
PathToCSV = 'Batch-4-Complete.csv'

# Open CSV file
with open(PathToCSV, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)

    # check that the row is not empty or null
    for row in reader:
        if row[0] != '':
            columnA.append(row[0])
        if row[1] != '':
            columnB.append(row[1])

print(f"Reviewing file {PathToCSV}")
print("Total Numbers in Column A is " + str(len(columnA)))
print("Total Numbers in Column B is " + str(len(columnB)))

# Loop through column a, add number to list if not in column b
for record in columnA:
    if record in columnB:
        continue
    else:
        # print(record + ' is not in column B'  )
        # removing because it clutters console but can be added for additional ongoing info
        missingFromColumnB.append(record)

print(f"There were {len(missingFromColumnB)} numbers in Column A that are not in Column B.")

df = pd.DataFrame(missingFromColumnB, columns=(['Phone Number']))
df.to_csv('MissingFromColumnB.csv', index=False, encoding='utf-8')

