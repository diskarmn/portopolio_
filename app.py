import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask,request,session,url_for,redirect,jsonify,render_template
import jwt  #token bukti akun verifikasi
import hashlib #mengacak kata menjadi kode random
from datetime import datetime,timedelta #alat waktu flask nanti digunakan mengatur kedaluarsa token
from pymongo import MongoClient

app=Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db=client[DB_NAME]
# client=MongoClient('mongodb://diskarmn:Diska123@ac-sjiapka-shard-00-00.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-01.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-02.3lnlkgx.mongodb.net:27017/?ssl=true&replicaSet=atlas-vnije0-shard-0&authSource=admin&retryWrites=true&w=majority')
# db=client.pedulihivporto
SECRET_KEY = 'kunci_token' #agar token bisa masuk


    
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/home")
def home():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive,
                 SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("home.html",
            nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin",
            msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin",
            msg="There was an issue logging you in"))
@app.route("/dohome")
def dohome():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("dohome.html", nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))

@app.route("/pedukasi")
def pedukasi():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("pedukasi.html", nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route("/doedukasi")
def doedukasi():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("doedukasi.html", nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/detailproduk',methods=['GET'])
def detailproduk():
    return render_template('detailproduk.html') 
@app.route('/edukasi',methods=['GET'])
def edukasi():
    return render_template('edukasi.html') 
@app.route('/hivaids',methods=['GET'])
def hivaids():
    semua=list(db.hivaids.find({},{'_id':False}))
    return render_template('hiv.html',semua=semua) 
@app.route('/pengobatan',methods=['GET'])
def pengobatan():
    semua=list(db.pengobatan.find({},{'_id':False}))
    return render_template('pengobatan.html',semua=semua) 
@app.route('/viralload',methods=['GET'])
def viralload():
    semua=list(db.viralload.find({},{'_id':False}))
    return render_template('viralload.html',semua=semua) 
@app.route('/penyakit',methods=['GET'])
def penyakit():
    semua=list(db.penyakit.find({},{'_id':False}))
    return render_template('penyakit.html',semua=semua) 
@app.route('/pilihanlogin',methods=['GET'])
def pilihanlogin():
    msg=request.args.get('msg')
    return render_template('pilihanlogin.html',mgs=msg)    
@app.route('/login',methods=['GET'])
def login():
    msg=request.args.get('msg')
    return render_template('login.html',mgs=msg)
@app.route('/login2',methods=['GET'])
def login2():
    msg=request.args.get('msg')
    return render_template('login2.html',mgs=msg)
@app.route('/register',methods=['GET'])
def register():
    return render_template('register.html')
@app.route('/register2',methods=['GET'])
def register2():
    return render_template('register2.html')
#akses edukasi setelah login pasien
@app.route('/phivaids',methods=['GET'])
def phivaids():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.hivaids.find({},{'_id':False}))
        return render_template("phivaids.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/ppengobatan',methods=['GET'])
def ppengobatan():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.pengobatan.find({},{'_id':False}))
        return render_template("ppengobatan.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/pviralload',methods=['GET'])
def pviralload():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.viralload.find({},{'_id':False}))
        return render_template("pviralload.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/ppenyakit',methods=['GET'])
def ppenyakit():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.penyakit.find({},{'_id':False}))
        return render_template("ppenyakit.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))




#
@app.route('/dohivaids',methods=['GET'])
def dohivaids():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.hivaids.find({},{'_id':False}))
        return render_template("dohivaids.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/tampildohivaids',methods=['GET'])
def tampildohivaids():
    semua=list(db.hivaids.find({},{'_id':False}))
    return jsonify({'semua':semua})
@app.route('/hapusdohivaids',methods=['POST'])
def hapusdoivaids():
    nomordohivaids=request.form['nomorhiv']
    db.hivaids.delete_one(
        {'nomor':int(nomordohivaids)}) 
    return jsonify({'message':'success delete'})

@app.route('/dopengobatan',methods=['GET'])
def dopengobatan():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.pengobatan.find({},{'_id':False}))
        return render_template("dopengobatan.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/tampildopengobatan',methods=['GET'])
def tampildopengobatan():
    semua=list(db.pengobatan.find({},{'_id':False}))
    return jsonify({'semua':semua})
@app.route('/hapusdopengobatan',methods=['POST'])
def hapusdopengobatan():
    nomordopengobatan=request.form['nomorpengobatan']
    db.pengobatan.delete_one(
        {'nomor':int(nomordopengobatan)}) 
    return jsonify({'message':'success delete'})

@app.route('/doviralload',methods=['GET'])
def doviralload():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.viralload.find({},{'_id':False}))
        return render_template("doviralload.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/tampildoviralload',methods=['GET'])
def tampildoviralload():
    semua=list(db.viralload.find({},{'_id':False}))
    return jsonify({'semua':semua})
@app.route('/hapusdoviralload',methods=['POST'])
def hapusdoviralload():
    nomordoviralload=request.form['nomorviralload']
    db.viralload.delete_one(
        {'nomor':int(nomordoviralload)}) 
    return jsonify({'message':'success delete'})

@app.route('/dopenyakit',methods=['GET'])
def dopenyakit():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.penyakit.find({},{'_id':False}))
        return render_template("dopenyakit.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/tampildopenyakit',methods=['GET'])
def tampildopenyakit():
    semua=list(db.penyakit.find({},{'_id':False}))
    return jsonify({'semua':semua})
@app.route('/hapusdopenyakit',methods=['POST'])
def hapusdopenyakit():
    nomordopenyakit=request.form['nomorpenyakit']
    db.penyakit.delete_one(
        {'nomor':int(nomordopenyakit)}) 
    return jsonify({'message':'success delete'})


@app.route('/doproduk',methods=['GET'])
def doproduk():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.stock.find({},{'_id':False}))
        return render_template("doproduk.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))

@app.route('/produk',methods=['GET'])
def produk():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        semua=list(db.stock.find({},{'_id':False}))
        
        return render_template("produk.html", nickname=user_info["nick"],semua=semua)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))

#tambahkontenhivaids
@app.route('/tambahhiv', methods=['POST'])
def tambahhiv():
    nomor=db.hivaids.count_documents({})
    urutan=nomor + 1
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  
    file = request.files['file_give']
    extension=file.filename.split('.')[-1]#jenis file
    gambar= f'static/{mytime}.{extension}'#nama file
    file.save(gambar)#save ke static
    judulhiv=request.form.get('judul')
    isihiv=request.form.get('isi')
    db.hivaids.insert_one({'nomor':urutan,
                            'judul':judulhiv,
                           'isi':isihiv,
                           'file':gambar})
    return jsonify({'message':'sukses menambah artikel'})
#tambah konten pengobatan
@app.route('/tambahpengobatan', methods=['POST'])
def tambahpegobatan():
    nomor=db.pengobatan.count_documents({})
    urutan=nomor + 1
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  
    file = request.files['file_give']
    extension=file.filename.split('.')[-1]#jenis file
    gambar= f'static/{mytime}.{extension}'#nama file
    file.save(gambar)#save ke static
    judulhiv=request.form.get('judul')
    isihiv=request.form.get('isi')
    db.pengobatan.insert_one({'nomor':urutan,
                            'judul':judulhiv,
                           'isi':isihiv,
                           'file':gambar})
    return jsonify({'message':'sukses menambah artikel'})
#tambah viral load
@app.route('/tambahviralload', methods=['POST'])
def tambahviralload():
    nomor=db.viralload.count_documents({})
    urutan=nomor + 1
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  
    file = request.files['file_give']
    extension=file.filename.split('.')[-1]#jenis file
    gambar= f'static/{mytime}.{extension}'#nama file
    file.save(gambar)#save ke static
    judulhiv=request.form.get('judul')
    isihiv=request.form.get('isi')
    db.viralload.insert_one({'nomor':urutan,
                            'judul':judulhiv,
                           'isi':isihiv,
                           'file':gambar})
    return jsonify({'message':'sukses menambah artikel'})
#tambah konten penyakit
@app.route('/tambahpenyakit', methods=['POST'])
def tambahpenyakit():
    nomor=db.penyakit.count_documents({})
    urutan=nomor + 1
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  
    file = request.files['file_give']
    extension=file.filename.split('.')[-1]#jenis file
    gambar= f'static/{mytime}.{extension}'#nama file
    file.save(gambar)#save ke static
    judulhiv=request.form.get('judul')
    isihiv=request.form.get('isi')
    db.penyakit.insert_one({'nomor':urutan,
                        'judul':judulhiv,
                           'isi':isihiv,
                           'file':gambar})
    return jsonify({'message':'sukses menambah artikel'})

#pembelian
@app.route('/beli', methods=['POST'])
def beli():
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  
    nomor=db.pelanggan.count_documents({})
    urutan=nomor + 1
    file = request.files['file_give']
    nama=request.form.get('nama')
    nohp=request.form.get('nohp')
    alamat=request.form.get('alamat')
    pesan=request.form.get('pesan')
    vit1=request.form.get('vit1')
    vit2=request.form.get('vit2')
    vit3=request.form.get('vit3')
    total=request.form.get('total')
    extension=file.filename.split('.')[-1]#jenis file
    namagambar= f'static/{mytime}.{extension}'#nama file
    file.save(namagambar)#save ke static
    db.pelanggan.insert_one({'nomor':urutan,'nama':nama,
    'nohp':nohp,'alamat':alamat,'pesan':pesan,'vit1':vit1,
    'vit2':vit2,'vit3':vit3,'total':total,'file':namagambar,'status':'belum terkirim'})
    stockvit1 = db.stock.find_one({}, {"_id": 0, "vit1": 1})["vit1"]
    stockvit2 = db.stock.find_one({}, {"_id": 0, "vit2": 1})["vit2"]
    stockvit3 = db.stock.find_one({}, {"_id": 0, "vit3": 1})["vit3"]
    db.stock.update_one({},{"$set": {"vit1": int(stockvit1) - int(vit1),
    "vit2": int(stockvit2) - int(vit2),"vit3": int(stockvit3) - int(vit3),}},)
    return jsonify({'message':'success','nama':nama,
    'nohp':nohp,'alamat':alamat,'pesan':pesan,'vit1':vit1,
    'vit2':vit2,'vit3':vit3,'total':total,'file':namagambar})

#update stock
@app.route('/updatestock',methods=['POST'])
def updatestock():
    vit1=request.form['vit1']
    vit2=request.form['vit2']
    vit3=request.form['vit3']
    db.stock.update_one({},{"$set": {"vit1": vit1,
    "vit2": vit2,"vit3": vit3,}},)
    return jsonify({'message':'success'})
#tampil pesanan
@app.route('/tampilpesanan',methods=['GET'])
def tampilpesanan():
    pelanggan=list(db.pelanggan.find({},{'_id':False}))
    return jsonify({'pelanggan':pelanggan})
#update kirim pesanan
@app.route('/kirim',methods=['POST'])
def kirim():
    nomor=request.form['nomor']
    db.pelanggan.update_one(
        {'nomor':int(nomor)},
        {'$set':{'status':'terkirim'}})
    return jsonify({'message':'success'})
#hapus pesanan
@app.route('/hapus',methods=['POST'])
def hapus():
    nomor2=request.form['nomor2']
    db.pelanggan.delete_one(
        {'nomor':int(nomor2)}) 
    return jsonify({'message':'success delete'})

#konsultasi pasien
@app.route("/konsultasi",methods=['GET'])
def konsultasi():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("konsultasi.html", nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/konsultasipasien',methods=['POST'])
def konsultasipasien():
    nomor=db.konsultasi.count_documents({})
    urutan=nomor + 1
    nama=request.form['nama']
    pesan=request.form['pesan']
    db.konsultasi.insert_one({'nomor':urutan,'nama':nama,'pesan':pesan,'kepada':'dokter'})
    return jsonify({'message':'sukses mengirim pesan'})
#konsuldokter
@app.route("/dokonsultasi",methods=['GET'])
def dokonsultasi():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("dokonsultasi.html", nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("pilihanlogin", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("pilihanlogin", msg="There was an issue logging you in"))
@app.route('/konsultasidokter',methods=['POST'])
def konsultasidokter():
    nomor=db.konsultasi.count_documents({})
    urutan=nomor + 1
    kepada=request.form['kepada']
    pesan=request.form['pesan']
    db.konsultasi.insert_one({'nomor':urutan,'nama':"dokter",'pesan':pesan,'kepada':kepada})
    return jsonify({'message':'sukses mengirim pesan'})

@app.route('/tampilkonsul',methods=['GET'])
def tampilkonsul():
    semua=list(db.konsultasi.find({},{'_id':False}))
    return jsonify({'semua':semua})
@app.route('/hapusdokonsultasi',methods=['POST'])
def hapusdokonsultasi():
    nomordokonsultasi=request.form['nomorkonsultasi']
    db.konsultasi.delete_one(
        {'nomor':int(nomordokonsultasi)}) 
    return jsonify({'message':'success delete'})

#route api register
@app.route('/api/register',methods=['POST'])
def api_register():
    id_receive=request.form.get('id_give')
    pw_receive=request.form.get('pw_give')
    nickname_receive=request.form.get('nickname_give')

    pw_hash=hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() #mengenskripsi pw

    db.user.insert_one({
        'id':id_receive,
        'pw':pw_hash,
        'nick':nickname_receive})
    return  jsonify({'result':'success'})

#route api login
@app.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    result = db.user.find_one({"id": id_receive, "pw": pw_hash})

    if result is not None:
        if result['id'] == 'dokter':
            payload = {
                "id": id_receive,
                "exp": datetime.utcnow() + timedelta(days=1),}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return jsonify({"result": "dokter", "token": token})
        else:
            payload = {
                "id": id_receive,
                "exp": datetime.utcnow() + timedelta(days=1),}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return jsonify({"result": "success", "token": token})
    else:
        return jsonify({"result": "fail", "msg": "Either your email or your password is incorrect"})
    
@app.route('/api/nick',methods=['GET'])
def api_valid():
    token_receive=request.cookies.get('mytoken')
    try:
        payload=jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256'] )
        print (payload)
        user_info=db.user.find_one({'id':payload.get('id')},{'_id':0})
        return jsonify({'result':'success',
                        'nickname':user_info.get('nick')})
    except jwt.ExpiredSignatureError:
        msg='token exp'
        return jsonify({'result':'fail', 'msg':msg})
    except jwt.exceptions.DecodeError:
        msg='issue login/problem'
        return jsonify({'result':'fail', 'msg':msg})

# data={
#     'vit1':30,
#     'vit2':25,
#     'vit3':20
# }
# db.stock.insert_one(data)



if __name__=='__main__':
    app.run('0.0.0.0',port=5000,debug=True)
