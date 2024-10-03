import csv
import pandas as pd

listA = []
listB = []
missingFromListB = []
missingFromListA = []

PathToCSVA = 'something.csv'
PathToCSVB = 'something_else.csv'

# Open CSV A and read first column into list
with open(PathToCSVA, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # remove this line if you don't have a header

    # check that the row is not empty or null
    for row in reader:
        if row:
            listA.append(row[0])

print(f"Reviewing file {PathToCSVA}")
print("Total numbers in list A " + str(len(listA)))

# Open CSV B and read first column into list
with open(PathToCSVB, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # remove this line if you don't have a header

    # check that the row is not empty or null
    for row in reader:
        if row[0] != '':
            listB.append(row[0])

print(f"Reviewing file {PathToCSVB}")
print("Total numbers in list B " + str(len(listB)))

# Loop through list A and check for numbers that are missing from list B
for record in listA:
    if record in listB:
        continue
    else:
        # removed following statement because it clutters console but can be added for additional ongoing info
        # print(record + ' is not in column B'  )
        missingFromListB.append(record)

# Loop through list B and check for numbers that are missing from list A
for record in listB:
    if record in listA:
        continue
    else:
        # removed following statement because it clutters console but can be added for additional ongoing info
        # print(record + ' is not in column A'  )
        missingFromListA.append(record)

print(f"There were {len(missingFromListB)} numbers in List A that are not in List B.")
df = pd.DataFrame(missingFromListB, columns=(['Phone Number']))
df.to_csv('MissingFromListB.csv', index=False, encoding='utf-8')

print(f"There were {len(missingFromListA)} numbers in List B that are not in List A.")
dff = pd.DataFrame(missingFromListA, columns=(['Phone Number']))
dff.to_csv('MissingFromListA.csv', index=False, encoding='utf-8')
