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
def home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start date (yyyy-mm-dd)]<br/> "
        f"/api/v1.0/[start date (yyyy-mm-dd)]/[end date (yyyy-mm-dd)]<br/>"
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
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp              
        precipitation.append(precip_dict)
        
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    sel = [station.station,station.name,station.latitude,station.longitude,station.elevation]
    result = session.query(*sel).all()
    session.close() 
    
    stations_data = []
    for stat,name,latitude,longitude,elevation  in result:
        station_info = {}
        station_info["station"] = stat
        station_info["name"] = name
        station_info["latitude"] = latitude
        station_info["longitude"] = longitude
        station_info["elevation"] = elevation            
        stations_data.append(station_info)
    
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
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs             
        tmp_obs.append(tobs_dict)
    
    return jsonify(tmp_obs)

@app.route("/api/v1.0/<start>")
def dynamic_start(start):
    session = Session(engine)

    sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
    result = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()          
    session.close()
    tobs_ds = []
    for tobs_min,tobs_max,tobs_avg  in result:
        result_ds = {}
        result_ds["tobs_min"] = tobs_min
        result_ds["tobs_max"] = tobs_max
        result_ds["tobs_avg"] = tobs_avg            
        tobs_ds.append(result_ds)
        
    return jsonify(tobs_ds)
@app.route("/api/v1.0/<start>/<end>")
def dynamic_start_end(start,end):
    session = Session(engine)
    sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
    result = session.query(*sel).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()        
    session.close()
    tobs_dse = []
    for tobs_min,tobs_max,tobs_avg  in result:
        result_dse = {}
        result_dse["tobs_min"] = tobs_min
        result_dse["tobs_max"] = tobs_max
        result_dse["tobs_avg"] = tobs_avg            
        tobs_dse.append(result_dse)
        
    return jsonify(tobs_dse)

if __name__ == "__main__":
    app.run(debug=True)