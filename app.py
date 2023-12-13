# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def home():         #landing page that shows route paths
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start date (yyyy-mm-dd)] Date must be between 2010-01-01 and 2017-08-23<br/> " #use details to show user how to query the right data
        f"/api/v1.0/[start date (yyyy-mm-dd)]/[end date (yyyy-mm-dd)] Date must be between 2010-01-01 and 2017-08-23<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    sel = [measurement.date, measurement.prcp]      
    result = session.query(*sel).\
        filter(measurement.date >= '2016-08-23').\
        all()
        
    session.close()       
    
    precipitation = []
    for date,prcp  in result:
        result_data= {}
        result_data["date"] = date
        result_data["prcp"] = prcp              
        precipitation.append(result_data)
        
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    sel = [station.station,station.name,station.latitude,station.longitude,station.elevation]
    result = session.query(*sel).all()
    session.close() 
    #Create a dictionary from the row data and append to a list
    stations_data = []
    for stat,name,latitude,longitude,elevation  in result:
        result_data = {}
        result_data["station"] = stat
        result_data["name"] = name
        result_data["latitude"] = latitude
        result_data["longitude"] = longitude
        result_data["elevation"] = elevation            
        stations_data.append(result_data)
    
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    result = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= "2016-08-23").all()
    session.close()
     
    tmp_obs = []
    for date,tobs  in result:
        result_data = {}
        result_data["date"] = date
        result_data["tobs"] = tobs             
        tmp_obs.append(result_data)
    
    return jsonify(tmp_obs)

@app.route("/api/v1.0/<start>")
def dynamic_start(start):
    
    if start > "2017-08-23" or  start < "2010-01-01":
        return("HEY YOU! The date entered is out of range! The date must be between 2010-01-01 and 2017-08-23")
    else: 
        session = Session(engine)
        sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
        result = session.query(*sel).\
            filter(measurement.date >= start).all()          
        session.close()

        tobs_ds = []
        for tobs_min,tobs_max,tobs_avg  in result:
            result_data = {}
            result_data["tobs_min"] = tobs_min
            result_data["tobs_max"] = tobs_max
            result_data["tobs_avg"] = tobs_avg            
            tobs_ds.append(result_data)
        
    return jsonify(tobs_ds)

@app.route("/api/v1.0/<start>/<end>")
def dynamic_start_end(start,end):
    if start > "2017-08-23" or  start < "2010-01-01":
        return("HEY YOU! The start date entered is out of range! The date must be between 2010-01-01 and 2017-08-23")
    elif end > "2017-08-23" or  end < "2010-01-01":
        return("HEY BUDDY! The end date entered is out of range! The date must be between 2010-01-01 and 2017-08-23")
    elif start > end:
        return("HEY PAL! The start date cannot be later than the end date")
    else:
        session = Session(engine)
        sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
        result = session.query(*sel).\
            filter(measurement.station == 'USC00519281').\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).all()        
        session.close()
        
        tobs_dse = []
        for tobs_min,tobs_max,tobs_avg  in result:
            result_data = {}
            result_data["tobs_min"] = tobs_min
            result_data["tobs_max"] = tobs_max
            result_data["tobs_avg"] = tobs_avg            
            tobs_dse.append(result_data)
            
        return jsonify(tobs_dse)
    
if __name__ == "__main__":
    app.run(debug=True)