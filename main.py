from ntpath import join
import uuid, os, time
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
from cgitb import html
from tkinter import N
from openpyxl import Workbook, load_workbook
from flask import Flask, render_template, request, flash, redirect, send_file, send_from_directory, abort, url_for


UPLOAD_FOLDER = 'C:/Users/rosa_tiago/Documents/Python Codes/joinpdf/files/'
ALLOWED_EXTENSIONS = {'pdf'}
app = Flask(__name__)
app.secret_key ="hello"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getFiles(name):
    nomes = []
    for x in os.listdir(UPLOAD_FOLDER):
        if x.startswith(name):
            nomes.append(x)
    return(nomes)

def joinpdf(namesList):
    
    writer = PdfWriter()
    
    for pdf in namesList:
        reader = PdfReader(UPLOAD_FOLDER+pdf)
        writer.addpages(reader.pages)

    writer.write(UPLOAD_FOLDER+'resultado.pdf')
    return redirect(url_for('download'))
        
@app.route("/download")   
def download():
    try:
        return send_from_directory(
            directory=app.config['UPLOAD_FOLDER'],path='resultado.pdf',as_attachment=True
            )
    except FileNotFoundError:
        abort(404)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/join", methods = ['POST'])
def getPdf():
    uid = str(uuid.uuid4())
    
    writer = PdfWriter()
    
    
    uploadedFiles = request.files.getlist('files')
    listaNomes = []
    n = 0
    
    for file in uploadedFiles:
        listaNomes.append(file.filename)
        file_name, file_extension = os.path.splitext(file.filename)
        if not allowed_file(file.filename):
            flash('Apenas arquivos do tipo pdf são permitidos !')
            return redirect('/')
        fileName = str(uid)+str(int(round(time.time())))+'-'+str(n)+file_extension
        
        reader = PdfReader(file)
        writer.addpages(reader.pages)
        writer.write(UPLOAD_FOLDER+fileName)
        
        n+=1
    nomes = getFiles(uid)
    joinpdf(nomes)
    return render_template('resultado.html', uid = str(uid),nome = listaNomes, len = len(listaNomes))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)