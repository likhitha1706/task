from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_login import current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:18me1a0580@localhost/student_marks_details'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "likhitha"

db = SQLAlchemy(app)

conn = psycopg2.connect(database = "student_marks_details", user= 'postgres', password = '18me1a0580', host = '127.0.0.1', port= '5432')
conn.autocommit = True
cursor = conn.cursor()
sub=0
length1=0
length2=0
res=""
subjects =""
list1=0

class Details(db.Model):
    __tablename__ = "student_details"

    id = db.Column(db.Integer,primary_key = True)
    student_name = db.Column(db.String(50))
    roll_no = db.Column(db.String(50))
    department = db.Column(db.String(50))
    year = db.Column(db.String(50))
    semester = db.Column(db.String(50))
    section = db.Column(db.String(50))
    child = db.relationship('Marks', backref='student_details')

   

class Marks(db.Model):
    __tablename__ = "marks_details"

    id = db.Column(db.Integer,primary_key = True)
    student_id = db.Column(db.Integer,db.ForeignKey('student_details.id'))
    subject_1 = db.Column(db.Integer())
    subject_2 = db.Column(db.Integer())
    subject_3 = db.Column(db.Integer())
    subject_4 = db.Column(db.Integer())
    percentage = db.Column(db.Float)

    def __repr__(self):
        return "{} {} {} {} {}".format(self.subject_1,self.subject_2,self.subject_3,self.subject_4,self.percentage)



    
@app.route("/",methods= ["GET"])
def marks():
    return render_template('home.html')



@app.route('/add/student', methods=["POST", "GET"])
def add_student():
    if request.method=="POST":
        if request.form['details']=='submit':
            Student_name = request.form['one']
            Roll_no = request.form['two']
            Department = request.form['branch']
            Year = request.form['year']
            Semester = request.form['sem']
            Section = request.form['six']
            
            details=Details(student_name=Student_name,roll_no=Roll_no.upper(),department=Department,year=Year,semester=Semester,section=Section.upper())

            db.session.add(details)
            db.session.commit()
            
            flash("Student added Successfully") 
        return redirect('/')
    return render_template('student.html')




@app.route('/add/marks', methods=["POST", "GET"])   
def add_marks():
    sub=0
    Roll_no=0
    no=''
    if request.method=="POST":
        if request.form['Search']=='Search':
            Roll_no = request.form['one']
            no=Roll_no.upper()
            # cursor.execute("select * from student_details where roll_no =%s",[Roll_no.upper()])
            # res = cursor.fetchall()
            
            d=Details.query.filter_by(roll_no=Roll_no.upper()).first()
            Department = d.department
            Year = d.year
            Semester= d.semester
            result=Department+Year+Semester
            dict={'cse1I':['M1','PHYSICS','ENGISH-1','DRAWING'],'cse1II':['MECHANICS','ES','CHEMISTRY','CP'],'cse2I':['FLAT','DS','DLD','M2'],'cse2II':['R','CD','OS','CG'],'cse3I':['OOAD','UML','DBMS','PYTHON'],'cse3II':['JAVA','C','CO','ADS'],'cse4I':['PEHV','UP','LINUX','SE'],'cse4II':['VERBAL','APTITUDE','ML','AWS'],'ece1I':['M1','PHYSICS','ENGISH-1','DRAWING'],'ece1II':['MECHANICS','ES','CHEMISTRY','CP'],'ece2I':['FLAT','DS','DLD','M2'],'ece2II':['R','CD','OS','CG'],'ece3I':['OOAD','UML','DBMS','PYTHON'],'ece3II':['JAVA','C','CO','ADS'],'ece4I':['PEHV','UP','LINUX','SE'],'ece4II':['VERBAL','APTITUDE','ML','AWS']}
            sub=dict[result]
            print(sub)

            return render_template('subjects.html',sub=sub,Roll_no = no )

        else:
           
            # return "hello"
            Subject_1 = request.form['sub1']
            Subject_2 = request.form['sub2']
            Subject_3 = request.form['sub3']
            Subject_4 = request.form['sub4']

            cal = int(Subject_1)+int(Subject_2)+int(Subject_3)+int(Subject_4)
            Percentage = (cal/400)*100

            #print(Roll_no)

            Roll_no = request.form['num']

            details=Details.query.filter_by(roll_no=Roll_no.upper()).first()
            print(details.id)
            subjects=Marks(student_id=details.id,subject_1 = int(Subject_1),subject_2 =int(Subject_2),subject_3=int(Subject_3),subject_4=int(Subject_4),percentage = Percentage)
            db.session.add(subjects)
            db.session.commit()

            flash("Marks added Successfully") 
            return redirect('/')
        
    return render_template('subjects.html',sub=sub,Roll_no = no)

@app.route('/view/marks',methods=["POST","GET"])
def view_marks():

    sub=0
    length1=0j
    length2=0
    res=""
    subjects =""
    
   
    if request.method=="POST":
        if request.form['Search']=='Search':
            Roll_no = request.form['one']
            
            
            
            cursor.execute("select * from student_details where roll_no =%s",[Roll_no.upper()])
            res = cursor.fetchall()
            length1 = len(res) 
            print(res)

            # d=Details.query.filter_by(roll_no=Roll_no.upper()).first()

            id = res[0][0]
            Department =res[0][3]
            Year =res[0][4]
            Semester=res[0][5]
            result=Department+Year+Semester
            dict={'cse1I':['M1','PHYSICS','ENGISH-1','DRAWING'],'cse1II':['MECHANICS','ES','CHEMISTRY','CP'],'cse2I':['FLAT','DS','DLD','M2'],'cse2II':['R','CD','OS','CG'],'cse3I':['OOAD','UML','DBMS','PYTHON'],'cse3II':['JAVA','C','CO','ADS'],'cse4I':['PEHV','UP','LINUX','SE'],'cse4II':['VERBAL','APTITUDE','ML','AWS'],'ece1I':['M1','PHYSICS','ENGISH-1','DRAWING'],'ece1II':['MECHANICS','ES','CHEMISTRY','CP'],'ece2I':['FLAT','DS','DLD','M2'],'ece2II':['R','CD','OS','CG'],'ece3I':['OOAD','UML','DBMS','PYTHON'],'ece3II':['JAVA','C','CO','ADS'],'ece4I':['PEHV','UP','LINUX','SE'],'ece4II':['VERBAL','APTITUDE','ML','AWS']}
            sub=dict[result]

            cursor.execute("select * from marks_details where student_id =%s",[id])
            subjects = cursor.fetchall()
            
           
   
            # subjects=Marks.query.filter_by(student_id=id).first()
            # print(d)
            length2=len(subjects)
            # length1=len(d)

            print(subjects)

        return render_template('marks.html',subjects=subjects,length1=length1,length2=length2,sub=sub,res=res)
    return render_template('marks.html',subjects=subjects,length1=length1,length2=length2,sub=sub,res=res)        

@app.route('/delete/student',methods=["POST","GET"])
def delete_student():
    sub=0
    if request.method=="POST":
        if request.form['Search']=='Search':

            Roll_no = request.form['one']

            # details=Details.query.filter_by(roll_no =Roll_no.upper()).first()

            cursor.execute("select * from student_details where roll_no =%s",[Roll_no.upper()])
            res = cursor.fetchall()

            Department =res[0][3]
            Year =res[0][4]
            Semester=res[0][5]
            result=Department+Year+Semester
            dict={'cse1I':['M1','PHYSICS','ENGISH-1','DRAWING'],'cse1II':['MECHANICS','ES','CHEMISTRY','CP'],'cse2I':['FLAT','DS','DLD','M2'],'cse2II':['R','CD','OS','CG'],'cse3I':['OOAD','UML','DBMS','PYTHON'],'cse3II':['JAVA','C','CO','ADS'],'cse4I':['PEHV','UP','LINUX','SE'],'cse4II':['VERBAL','APTITUDE','ML','AWS'],'ece1I':['M1','PHYSICS','ENGISH-1','DRAWING'],'ece1II':['MECHANICS','ES','CHEMISTRY','CP'],'ece2I':['FLAT','DS','DLD','M2'],'ece2II':['R','CD','OS','CG'],'ece3I':['OOAD','UML','DBMS','PYTHON'],'ece3II':['JAVA','C','CO','ADS'],'ece4I':['PEHV','UP','LINUX','SE'],'ece4II':['VERBAL','APTITUDE','ML','AWS']}
            sub=dict[result]

            Marks.query.filter_by(student_id=res[0][0]).delete()
            Details.query.filter_by(roll_no =res[0][2]).delete()

            db.session.commit()

            flash("Student deleted Successfully") 
            
            return redirect('/')
    return render_template('delete.html',sub=sub)        

@app.route('/all/marks',methods=["POST","GET"])
def all_marks():
    sub=0
    length1=0
    length2=0
    res=""
   
    list1=''




    if request.method=="POST":
        if request.form['allmarks']=='submit':

            Department = request.form['branch']
            Year = request.form['year']
            Semester = request.form['sem']


        
            cursor.execute("select * from student_details where department=%s and year=%s and semester=%s",(Department,Year,Semester))
            res = cursor.fetchall()
            length1 = len(res) 
            print(res)

            # d=Details.query.filter_by(roll_no=Roll_no.upper()).first()

            id = res[0][0]
            Department =res[0][3]
            Year =res[0][4]
            Semester=res[0][5]
            result=Department+Year+Semester
            dict={'cse1I':['M1','PHYSICS','ENGISH-1','DRAWING'],'cse1II':['MECHANICS','ES','CHEMISTRY','CP'],'cse2I':['FLAT','DS','DLD','M2'],'cse2II':['R','CD','OS','CG'],'cse3I':['OOAD','UML','DBMS','PYTHON'],'cse3II':['JAVA','C','CO','ADS'],'cse4I':['PEHV','UP','LINUX','SE'],'cse4II':['VERBAL','APTITUDE','ML','AWS'],'ece1I':['M1','PHYSICS','ENGISH-1','DRAWING'],'ece1II':['MECHANICS','ES','CHEMISTRY','CP'],'ece2I':['FLAT','DS','DLD','M2'],'ece2II':['R','CD','OS','CG'],'ece3I':['OOAD','UML','DBMS','PYTHON'],'ece3II':['JAVA','C','CO','ADS'],'ece4I':['PEHV','UP','LINUX','SE'],'ece4II':['VERBAL','APTITUDE','ML','AWS']}
            sub=dict[result]


            print(res[0][0])
            list1=[]
            list2=[]
            for i in range(0,len(res)):
                
                cursor.execute("select * from marks_details where student_id=%s ",[res[i][0]])
                k = cursor.fetchall()

                list1.append(k)
                cursor.execute("select * from marks_details where student_id=%s and subject_1<35 and subject_2<35 and subject_3<35 and subject_4<35 ",[res[i][0]])
                k1 = cursor.fetchall()
                list2.append(k1)
                print(k1)
            print(list1[0][0][2])
            print(k1)
            length3=len(k1)
            print(length3)
            length2 = len(list1)
            pass_rate=100-length3
            print(pass_rate)

           
            print(list1)

           




        return render_template('allmarks.html',sub = sub,res = res,length1 = length1,length2 = length2,list1 = list1,pass_rate = pass_rate,Department=Department,Year=Year,Semester=Semester)  

    return render_template('allmarks.html',sub = sub,res = res,length1 = length1,length2 = length2,list1 = list1)  

# @app.route('/consolidate/reports',methods=["POST","GET"])
# def consolidate_reports():
#     if request.method=="POST":





if __name__=="__main__":
    db.create_all()
    app.run(debug=True)



# rollno=request.form['']
# detai=Details.query.filter_by(rollno=)

# d=Marks.query.filter_by(student_id=details.id)