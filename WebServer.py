from flask import Flask, url_for, request, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'Parkanlage.db'

# init DB
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        return db

# close DB
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# execute Query
def query_db(query, args=(), one = False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv # return the first entry if "one" is set, else return all 



## Routing
@app.route("/")
@app.route("/index")
def index(): #index html
    return render_template('index.html',
        project_path=url_for("project_main"), 
        req_path=url_for("requirements"))
        # add params here

@app.route("/requirements") # requirements for the project
def requirements():
    return render_template('requirements.html')

@app.route("/project_main", methods= ['GET', 'POST']) # main page
def project_main():
        if request.method == 'POST':
                licenseplate = request.form['licenseplate']

                if 'drivein' in request.form:
                        # prüfe, ob Fahrer bereits existiert
                        if IsDriverRegistered(licenseplate):
                                # Hat Fahrer Dauerkarte
                                if IsDriverCardUser(licenseplate):

                                        print("Fahrer existiert")

                        else: # Fahrer ist neu
                                # Abfrage auf Dauerkarte y / n 
                                return project_drivein(licenseplate)
                        
                elif 'driveout' in request.form:
                        return project_driveout(licenseplate)

        return render_template('project_main.html')

@app.route("/project_drivein", methods= ['GET', 'POST']) # drive in page (not registered)
def project_drivein(licenseplate = None):
        if request.method == 'POST':
                if 'card' in request.form:
                        return "Dauerkarte"
                elif 'ticket' in request.form:
                        return "Einzelticket"

        return render_template('project_drivein.html')

@app.route("/project_driveout", methods= ['GET', 'POST']) # drive out pages + handling
def project_driveout(licenseplate = None):
        
        carduser = True
        
        if request.method == 'POST':
                if 'pay' in request.form:
                        return render_template("project_driveout_ticket_payed.html")

        if carduser:
                return render_template("project_driveout_card.html")
        else:
                return render_template("project_driveout_ticket.html", value_to_pay='123€')


# Helper functions

def IsPlaceFree(IDPlateCard):
        # declaration
        resultDB = ""
        parkCard = False
        quantityFreeSpacesCard = 0
        quantityFreeSpacesTicket = 0
        driverID = ""

        #Ist Kennzeichen in der Datenbank vorhanden?
        for vehicle in query_db('SELECT * FROM Fahrerauto WHERE Kennzeichen = ' + IDPlateCard):
                resultDB += vehicle['FahrerID']

        if resultDB == "":
                #Error
                print("Error")
        else:
                #Ist der Fahrzeughalter ein Dauerparker?
                driverID = resultDB
                resultDB = ""
                for driver in query_db('SELECT * FROM Fahrer WHERE ID = ' + driverID):
                        resultDB += driver['Dauerkarte']

                if resultDB == "":
                        print("Error")
                        #Error
                
                parkCard = (resultDB == "1")

                #Kalkuliere freie Parkplätze
                if parkCard:
                        for places in query_db('SELECT COUNT(Parker.Kennzeichen) AS Anzahl FROM Parker ' +
                                               'LEFT JOIN Fahrerauto ON Fahrerauto.Kennzeichen = Parker.Kennzeichen ' +
                                               'LEFT JOIN Fahrer ON Fahrer.ID = Fahrerauto.FahrerID ' +
                                               'WHERE Parker.Ausfahrt = NULL AND Fahrer.Dauerkarte = 1'):
                                resultDB = places['Anzahl']
                        
                        quantityFreeSpacesCard = 40 - int(resultDB)
        
                for places in query_db('SELECT COUNT(Parker.Kennzeichen) AS Anzahl FROM Parker ' +
                                        'LEFT JOIN Fahrerauto ON Fahrerauto.Kennzeichen = Parker.Kennzeichen ' +
                                        'LEFT JOIN Fahrer ON Fahrer.ID = Fahrerauto.FahrerID ' +
                                        'WHERE Parker.Ausfahrt = NULL AND Fahrer.Dauerkarte = 0'):
                        resultDB = places['Anzahl']
                
                quantityFreeSpacesTicket = 140 - int(resultDB)
                
                #Darf er parken?
                if parkCard:
                        return (quantityFreeSpacesCard + quantityFreeSpacesTicket) > 0
                else:
                        return quantityFreeSpacesTicket >= 4

def IsDriverCardUser(UserID):
        return True

def IsDriverRegistered(UserID):
        resultDB = ""
        for vehicle in query_db('SELECT * FROM Fahrerauto WHERE FahrerID = ' + UserID):
                resultDB += vehicle['FahrerID']

        if resultDB != "":
                return True
        else:
                return False

def CheckForFreePlace(Licenseplate, DriverIsCardUser):
        print("")

# Main start
if __name__ == '__main__':
    app.run(port=4698, debug=True)