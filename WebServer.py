from flask import Flask, url_for, request, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'Parkanlage.db'

# init DB
def get_db():
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
                        UserID = GetUserIDFromLicensePlate(licenseplate)
                        if UserID > -1:
                                print("User is registered")
                                return CheckForFreePlace(licenseplate, IsDriverCardUser(UserID))

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
                        # Insert into DB new Fahrer with Drivercard

                        return "Dauerkarte"
                        #return CheckForFreePlace(licenseplate, True)

                elif 'ticket' in request.form:
                        # Insert into DB new Fahrer with Drivercard

                        return "Einzelticket"
                        #return CheckForFreePlace(licenseplate, False)

        return render_template('project_drivein.html')

@app.route("/project_driveout", methods= ['GET', 'POST']) # drive out pages + handling
def project_driveout(licenseplate = None):
        
        if licenseplate is not None:
                UserID = GetUserIDFromLicensePlate(licenseplate)
                carduser = IsDriverCardUser(UserID)
        
                # Update DB Set Ausfahrtdatum = Date Now where Kennzeichen = licenseplate


                if carduser:
                        return render_template("project_driveout_card.html")
                else:
                        return render_template("project_driveout_ticket.html", value_to_pay='123€')

        if request.method == 'POST':
                if 'pay' in request.form:
                        print("Return the payed HTML")
                        return render_template("project_driveout_ticket_payed.html")

# Helper functions                

# Returns True if the User has a DriverCard
def IsDriverCardUser(UserID):
        resultDB = -1

        query = "SELECT * FROM FAHRER WHERE ID = " + str(UserID)
        for driver in query_db(query):
                resultDB = driver['Dauerkarte']

        if resultDB == 1:
                return True
        else:
                return False

# Returns UserID if one Exists, else -1
def GetUserIDFromLicensePlate(Licenseplate): 
        resultDB = -1

        query = "SELECT * FROM Fahrerauto WHERE Kennzeichen = \""+ Licenseplate + "\""
        for vehicle in query_db(query):
                resultDB = vehicle['FahrerID']

        return resultDB

# Returns True if a Place is free for the User, else False
def IsPlaceFree(DriverIsCardUser):
        
        for places in query_db('SELECT COUNT(Parker.Kennzeichen) AS Anzahl FROM Parker ' +
                                'LEFT JOIN Fahrerauto ON Fahrerauto.Kennzeichen = Parker.Kennzeichen ' +
                                'LEFT JOIN Fahrer ON Fahrer.ID = Fahrerauto.FahrerID ' +
                                'WHERE Parker.Ausfahrtdatum = NULL AND Fahrer.Dauerkarte = 1'):
                resultDB = places['Anzahl']
        
        quantityFreeSpacesCard = 40 - int(resultDB)
        print("FreeSpacesCard " + str(quantityFreeSpacesCard))

        for places in query_db('SELECT COUNT(Parker.Kennzeichen) AS Anzahl FROM Parker ' +
                                'LEFT JOIN Fahrerauto ON Fahrerauto.Kennzeichen = Parker.Kennzeichen ' +
                                'LEFT JOIN Fahrer ON Fahrer.ID = Fahrerauto.FahrerID ' +
                                'WHERE Parker.Ausfahrtdatum = NULL AND Fahrer.Dauerkarte = 0'):
                resultDB = places['Anzahl']
        
        quantityFreeSpacesTicket = 140 - int(resultDB)
        print("FreeSpacesTicket " + str(quantityFreeSpacesTicket))

        if DriverIsCardUser:
                return (quantityFreeSpacesCard + quantityFreeSpacesTicket) > 0
        else:
                return quantityFreeSpacesTicket >= 4

# Returns the HTML File for the User, Valid if a Place is free, Invalid if not
def CheckForFreePlace(Licenseplate, DriverIsCardUser):
        if IsPlaceFree(DriverIsCardUser):
                print("Place is free")
                # insert into DB CardUser, LicensePlate, Date now
                return render_template("project_drivein_valid.html")
        else:
                print("Place is not free")
                return render_template("project_drivein_invalid.html")
        

# Main start
if __name__ == '__main__':
    app.run(port=4698, debug=True)