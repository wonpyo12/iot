from flask import Flask,render_template
try:
    from urllib.request import urlopen 
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError,URLError

deviceIp = "192.168.0.71"
portnum = "80"

base_url = "http://"+ deviceIp + ":" + portnum
events_url= base_url + "/events"

app = Flask(__name__,template_folder=".")

@app.route('/events')
def getevents() :
    u = urlopen(events_url)
    data = ""
    try:
        data = u.read()
    except HTTPError as e:
        print("HTTP error: %d" % e.code)
    except URLError as e:
        print("Network error: %s" % e.reaspm.args[1])
    return data
@app.route('/')
def dht22chart():
    return render_template("dhtchart.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)