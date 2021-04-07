from flask import Flask, render_template,request,redirect, url_for
app = Flask(__name__)
import pandas as pd
import subprocess

# home page
@app.route("/")
@app.route("/<string:error>")
def start(error=''):
    title = "Container Information "

    sub = subprocess.Popen("docker ps -a --format 'table {{.Names}},{{.ID}},{{.Status}}'", shell=True, stdout=subprocess.PIPE).stdout.read() # run docker command for containers status
    sub = sub.decode('utf-8')
    sub = [ i.split(",")  for i in sub.split("\n")]
    df = pd.DataFrame(sub).dropna()
    df.rename(columns=df.iloc[0],  inplace=True) 
    df.drop(df.index[0], inplace=True)

    # constants
    nC_page = 20
    p = 0
    total_p = int(len(df) / nC_page)+1
    cur_p = 1
    st = int(p*nC_page)
    en = int((p+1)*nC_page)
    if error == '':
        return render_template("/index.html", title=title,
                                table=df.iloc[st:en].to_html(), tp=list(range(1, total_p + 1)), cp=cur_p, err='')
    elif error == 'No match found':
    	return render_template("/index.html", title=title,
                               table=df.iloc[st:en].to_html(), tp=list(range(1, total_p + 1)), cp=cur_p, err=error)
    else:
        return render_template("/index.html", title=title,
                               table=df.iloc[st:en].to_html(), tp=list(range(1, total_p + 1)), cp=cur_p, err='')

# navigation through pages
@app.route("/<int:p>")
def navi_page(p):
    title = "Containers status"

    sub = subprocess.Popen("docker ps -a --format 'table {{.Names}},{{.ID}},{{.Status}}'", shell=True, stdout=subprocess.PIPE).stdout.read() # run docker command for containers status
    sub = sub.decode('utf-8')
    sub = [ i.split(",")  for i in sub.split("\n")]
    
    # string result to pandas dataframe
    df = pd.DataFrame(sub).dropna()
    df.rename(columns=df.iloc[0],  inplace=True)
    df.drop(df.index[0], inplace=True)

    # constants
    nC_page = 20
    pp = p-1
    total_p = int(len(df) / nC_page)+1
    cur_p = p
    st = int(pp*nC_page)
    en = int((pp+1)*nC_page)

    return render_template("/index.html", title=title, table=df.iloc[st:en].to_html(), tp=list(range(1,total_p+1)), cp=cur_p)

# search for the given container name
@app.route("/selectedCont", methods=["POST"])
def search():
    title = "Search result"

    if request.method == "POST":
        que = request.form['sQuery']
        # run docker command for the particular container status
        sub = subprocess.Popen(
            "docker ps -a --filter 'name="+str(que) +"' --format 'table {{.Names}},{{.ID}},{{.Status}}'  ", shell=True,
            stdout=subprocess.PIPE).stdout.read()
        sub = sub.decode('utf-8')
        sub = [i.split(",") for i in sub.split("\n")]
        df = pd.DataFrame(sub).dropna()
        df.rename(columns=df.iloc[0], inplace=True)
        df.drop(df.index[0], inplace=True)

        if len(df) > 0:
            return render_template("/index.html", title=title, table=df.to_html())
        else:
            return redirect(url_for('start', error='No match found'))


@app.route("/home", methods= ["POST"])
def home():
    return redirect(url_for('start', error=''))


if __name__ == "__main__":
    app.run()
