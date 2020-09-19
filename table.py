import mysql.connector
import webbrowser

conn = mysql.connector.connect(user='root', password='',
                              host='localhost',database='register')

if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")

select_data = """SELECT * FROM data"""
cursor = conn.cursor()
cursor.execute(select_data)
result = cursor.fetchall()

p = []

# tbl = "<tr><td>ID</td><td>Name</td><td>Email</td><td>Phone</td></tr>"
# p.append(tbl)

for row in result:
    a = "<tr><td>%s</td>"%row[1]
    p.append(a.strip().replace(',', ''))
    b = "<td>%s</td>"%row[2]
    p.append(b.strip().replace(',', ''))
    c = "<td>%s</td>"%row[3]
    p.append(c.strip().replace(',', ''))
    d = "<td>%s</td></tr>"%row[4]
    p.append(d.strip().replace(',', ''))
    


contents = '''<!DOCTYPE html>
<html>
<head>
<meta content="text/html; charset=ISO-8859-1"
http-equiv="content-type">
<title>Python Webbrowser</title>
</head>
<style>
table{
    color:red;
    width:1300px;
    text-align:center;
}
</style>
<thread>
<table border="2px solid black">
%s
</table>
</thread>
</html>
'''%(p)

filename = 'output.html'

def main(contents, filename):
    output = open(filename,"w")
    output.write(contents)
    output.close()

main(contents, filename)    
webbrowser.open(filename)

if(conn.is_connected()):
    cursor.close()
    conn.close()
    print("MySQL connection is closed.")   





    # a = pd.read_csv("C:/Users/dell/Desktop/project/test/corona-virus-cases.csv") 
    # a.to_csv("C:/Users/dell/Desktop/project/test/corona-virus-cases.csv", index=False)
    # keep_col = ['Countries','Total Cases','Todays Deaths','Total Recovered']
    # a = a[keep_col]

    # # to save as html file 
    # # named as "Table" 
    # a.to_html("C:/Users/dell/Desktop/project/test/templates/Table.htm") 
    # # assign it to a  
    # # variabldf.stylee (string) 
    # html_file = a.to_html()
    
#     #table
# @app.route('/Table')
# def Table():
#     return render_template('Table.htm') 