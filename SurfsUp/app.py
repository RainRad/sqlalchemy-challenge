import numpy as np
import sqlalchemy
import datetime as dt
import pandas
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify





#DB Link
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#Reflect DB
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station


#Flask code below
app = Flask(__name__)


@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/"
    )



@app.route("/api/v1.0/precipitation")
def alpha():
    #Create session
    session = Session(bind=engine) 

    #Query Data
    # Calculate the date one year from the last date in data set.
    year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [measurement.date,
        measurement.prcp]
    data = session.query(*sel).\
        filter(measurement.date <= '2017-08-23').\
        filter(measurement.date > '2016-08-23')
    
    #Create List of Dictionaries
    station_prcp_dictionary_data = []
    for station, prcp in data:
        station_dictionary = {}
        station_dictionary["station"] = station
        station_dictionary["prcp"] = prcp
        station_prcp_dictionary_data.append(station_dictionary)

    #Return Jason
    return jsonify(station_prcp_dictionary_data)


@app.route("/api/v1.0/stations")
def bravo():
    #Create session
    session = Session(bind=engine) 
    
    global station
    sel = [station.station,
        station.name]
    data = session.query(*sel)
    
    #Create List of Dictionaries
    station_dictionary_data = []
    for name, station in data:
        station_dictionary = {}
        station_dictionary["station"] = station
        station_dictionary["name"] = name
        station_dictionary_data.append(station_dictionary)

    #Return Jason
    return jsonify(station_dictionary_data)

@app.route("/api/v1.0/tobs")
def charlie():
    #Create session
    session = Session(bind=engine) 

    #Query Data
    # Calculate the date one year from the last date in data set.
    year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [measurement.date,
        measurement.prcp]
    data = session.query(*sel).\
        filter(measurement.date <= '2017-08-23').\
        filter(measurement.date > '2016-08-23').\
        filter(measurement.station == "USC00519281")

    #Create List of Dictionaries
    popular_station_data = []
    for date, tobs in data:
        station_dictionary = {}
        station_dictionary["station"] = "USC00519281"
        station_dictionary["date"] = date
        station_dictionary["tobs"] = tobs
        popular_station_data.append(station_dictionary)

    #Return Jason
    return jsonify(popular_station_data)
    

@app.route("/api/v1.0/<start>")
def delta(start):
    #Create session
    session = Session(bind=engine) 

    # Perform a query to retrieve the data and precipitation scores
    sel = [measurement.date,
        measurement.tobs]
    data = session.query(*sel).\
        filter(measurement.date > start)

    #Create List of Dictionaries
    start_data = []
    station_dictionary = {}
    station_dictionary["Minimum Temp"] =  session.query(func.min(measurement.tobs)).\
        filter(measurement.date > start)[0][0]
    station_dictionary["Max Temp"] = session.query(func.max(measurement.tobs)).\
        filter(measurement.date > start)[0][0]
    station_dictionary["Average Temp"] = session.query(func.avg(measurement.tobs)).\
        filter(measurement.date > start)[0][0]
    station_dictionary["Starting Date"] = start
    station_dictionary["Ending Date"] = "2017-08-23"
    start_data.append(station_dictionary)

    # #Return Jason
    return jsonify(start_data)

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/api/v1.0/<start>/<end>")
def echo(start, end):
    #Create session
    session = Session(bind=engine) 

    # Perform a query to retrieve the data and precipitation scores
    sel = [measurement.date,
        measurement.tobs]
    data = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end)

    #Create List of Dictionaries
    start_data = []
    station_dictionary = {}
    station_dictionary["Minimum Temp"] =  session.query(func.min(measurement.tobs)).\
        filter(measurement.date > start).filter(measurement.date <= end).all()[0][0]
    station_dictionary["Max Temp"] = session.query(func.max(measurement.tobs)).\
        filter(measurement.date > start).filter(measurement.date <= end)[0][0]
    station_dictionary["Average Temp"] = session.query(func.avg(measurement.tobs)).\
        filter(measurement.date > start).filter(measurement.date <= end)[0][0]
    station_dictionary["Starting Date"] = start
    station_dictionary["Ending Date"] = end
    station_dictionary["Ending Date"] = "2017-08-23"
    start_data.append(station_dictionary)

    # #Return Jason
    return jsonify(start_data)

if __name__ == "__main__":
    app.run(debug=True)