from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        return render_template("form.html")
    elif request.method == "POST":
        IDtype = request.form['ID'] 
        studentId = request.form['id_value']
        final_list = data(IDtype,studentId)

        if IDtype == "student_id" and final_list[0]:
            return render_template("student_data.html", s_list = final_list[1])
        elif IDtype == "course_id" and final_list[0]:
            path = "/static/"+ str(studentId) + ".png"
            return render_template("course_data.html", avg = final_list[1], max=final_list[2], a=path)
        else:
            return render_template("error.html")

def check(list,id):
        if id in list:
            return True
        else:
            return False

def data(Idtype,Idvalue):

    f = open("data.csv", "r")
    f_line = f.readline()
    line =[]
    s_list = []
    st_list,cr_list=[],[]
    s_total = 0
    c_total = 0
    max_value,avg,count,total = -1,0,0,0
    while f_line:
        line.append(f_line.split(", "))
        f_line = f.readline()
    f.close()
    del line[0]

    for i in line:
        if i[0] not in st_list:
            st_list.append(i[0])
        if i[1] not in cr_list:
            cr_list.append(i[1])    

    if Idtype == "student_id":
        flag = check(st_list,Idvalue)
        for ele in line:
            if int(ele[0]) == int(Idvalue):
                s_list.append(ele)
        return_value = (flag, s_list)
        return return_value

    elif Idtype == "course_id":
        flag = check(cr_list,Idvalue)
        for ele in line:
            if int(ele[1]) == int(Idvalue):
                s_list.append(int(ele[2]))
                if int(ele[2]) > max_value : 
                    max_value = int(ele[2])
                total += int(ele[2])
                count += 1
        if count != 0:
            avg = total/count
        
        p = str(Idvalue)
        sortedlist = sorted(s_list)
        plt.hist(sortedlist)
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig(f'static/{p}.png')
        plt.close()
        return_value = (flag, avg, max_value)
        return return_value
    

if __name__ == "__main__":
    app.debug = True
    app.run()
