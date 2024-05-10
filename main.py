import sqlite3

#Part 1: Data creation, import, and insertion

#Create a new SQLite database
conn = sqlite3.connect('employee.db')
c = conn.cursor()

#Create Employee table
c.execute(
    '''CREATE TABLE Employee
    (EmployeeID INTEGER PRIMARY KEY, Name TEXT)'''
)

#Create Pay Table
c.execute(
    '''CREATE TABLE Pay
    (EmployeeID INTEGER, Year INTEGER, Earnings REAL, 
    FOREIGN KEY(EmployeeID) REFERENCES Employee(EmployeeID))'''
)

#Create SocialSecuirityMin table
c.execute(
    '''CREATE TABLE SocialSecurityMin
    (Year INTEGER PRIMARY KEY, Minimum REAL)'''
)

#Insert data into Employee table
with open('Employee.txt', 'r') as f:
    next(f) #Skip the header row
    for line in f:
        employeee_id, name = line.strip().split(',')
        c.execute("INSERT INTO Employee (EmployeeID, Name) VALUES (?, ?)", (employeee_id, name))

#Insert data into Pay table
with open('Pay.txt', 'r') as f:
    next(f) #Skip the header row
    for line in f:
        employeee_id, year, earnings = line.strip().split(',')
        c.execute("INSERT INTO Pay (EmployeeID, Year, Earnings) VALUES (?, ?, ?)", (employeee_id, year, earnings))    

#Insert data into SocialSecurityMin table
with open('SocialSecurityMin.txt', 'r') as f:
    next(f) #Skip the header row
    for line in f:
        year, minimum = line.strip().split(',')
        c.execute("INSERT INTO SocialSecurityMin (Year, Minimum) VALUES (?, ?)", (year, minimum))   

#Commit the changes
conn.commit()



#Part 2: Data Reporting 

# Join the three tables
query = """
SELECT e.Name, p.Year, p.Earnings, s.Minimum
FROM Employee e
JOIN Pay p ON e.EmployeeID = p.EmployeeID
JOIN SocialSecurityMin s ON p.Year = s.Year
"""

c.execute(query)

#Process the result set

header = "{:<20} {:<7} {:<10} {:<10}".format("Name", "Year", "Earnings", "Minimum", "Include")
print(header)
print("-" * len(header))

for row in c.fetchall():
    name, year, earnings, minimum = row
    include = "Yes" if earnings >= minimum else "No"
    line = "{:<20} {:<7} {:<10} {:<10}".format(name, year, earnings, minimum, include)
    print(line)

#Close the database connection
conn.close()
