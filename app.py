from  flask  import  Flask,render_template,request
import mysql.connector
connection=mysql.connector.connect(host='localhost',user='root',password='password',database='restaurant')
cursor=connection.cursor()

#username : password
data_b ={'aaa':'aaa'}

app = Flask(__name__,static_folder='static/css')  

def disp_table(dist):
	query1 = "SELECT * FROM {}".format(dist)
	cursor.execute(query1)
	data=cursor.fetchall()
	return render_template('/{}.html'.format(dist),sqldata=data)

def vegg(dist):
	dat = request.form['veg']
	if dat =='vegetarian':
		query1 = "SELECT * FROM {} where veg like 'veg%' ".format(dist)
		cursor.execute(query1)
		data=cursor.fetchall()
		return render_template('/{}.html'.format(dist),sqldata=data,veg_or_non=" (Veg)")
	
	elif dat =='non-vegetarian':
		query1 = "SELECT * FROM {} where veg like 'non%'".format(dist)
		cursor.execute(query1)
		data=cursor.fetchall()
		return render_template('/{}.html'.format(dist),sqldata=data,veg_or_non=" (Non-Veg)")
	
	else:
		return disp_table(dist)



@app.route('/') 
def home():
	return render_template('/index.html')

@app.route('/login',methods=['GET','POST'])
def login():
	user = request.form['username']
	pwd = request.form['password']
	if user not in data_b:
		return render_template('/login.html',message='Invalid Username')
	elif data_b[user]!=pwd:
		return render_template('/login.html',message='Invalid Password')
	else:
		return render_template('/input.html')

@app.route('/read',methods=['GET','POST'])
def read():
	if request.method=='POST':
		district=request.form.get('district')
		r_id = request.form.get('R_id')
		name=request.form.get('name')
		address=request.form.get('address')
		phno=request.form.get('phno')
		w_time=request.form.get('w_time')
		parking=request.form.get('parking')
		dine_in=request.form.get('dine_in')
		veg=request.form.get('veg')
		data=(r_id,name,address,phno,w_time,parking,dine_in,veg)
		if '' not in data:
			try:
				query ="INSERT INTO {} VALUES(%s,%s,%s,%s,%s,%s,%s,%s)".format(district)
				cursor.execute(query,data)
				connection.commit()
				return render_template('/input.html')
			except:
				return render_template('/input.html',message='Enter valid data')
		else:
			return render_template('/input.html',message='Enter valid data')


@app.route('/loginn') 
def loginn():
	return render_template('/login.html')

@app.route('/ernakulam')
def ernakulam():
	return disp_table("ernakulam")

@app.route('/thrissur')
def thrissur():
	return disp_table("thrissur")

@app.route('/palakkad')
def palakkad():
	return disp_table("palakkad")

@app.route('/ernakulam_filter',methods=['GET','POST'])
def ernakulam_veg():
	return vegg('ernakulam')

@app.route('/palakkad_filter',methods=['GET','POST'])
def palakkad_veg():
	return vegg('palakkad')

@app.route('/thrissur_filter',methods=['GET','POST'])
def thrissur_veg():
	return vegg('thrissur')

if __name__ == '__main__':
	app.run()	
