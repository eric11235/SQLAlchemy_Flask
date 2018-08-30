import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False") # need this check_same_thread, otherwise get a SQLalchemy error
    # on all page calls after the first page call that uses this engine...something about a can't share a session across threads
    # Found on Stackoverflow..."Using SQLAlchemy session from Flask raises "SQLite objects....' error message

# engine = create_engine('sqlite:////var/www/homepage/blog.db?check_same_thread=False'

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date 'YYYY-MM-DD'<br/>"
        f"/api/v1.0/start_date 'YYYY-MM-DD'/end_date 'YYYY-MM-DD'<br/>"
    )


@app.route("/api/v1.0/precipitation")
def temps():
    """Return a list of dates and temperature observations between 2016-08-23 and 2017-08-23"""
   
    # Query for the dates & temperature observations from the last year 2016-08-23 thru 2017-08-23

    avg_temp_year_list = []
    avg_temp_year_list = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').\
        order_by((Measurement.date).asc()).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
   
    temp_dict = {}
    avg_temp_year_dict = {}
    for i in avg_temp_year_list:
        temp_dict = dict([i])
        avg_temp_year_dict.update(temp_dict)    
    
    # JSONIFY the dictionary and return results

    return jsonify(avg_temp_year_dict)


@app.route("/api/v1.0/stations")
def stations_func():
    """Return a list of stations"""
    # Query all stations
    all_stations = []
    all_stations = session.query(Station.station).all()

    # This query returns a list of tuples...although each tuple only has one element
    # Convert this list of tuples to a 'flat' list using the ravel method
    
    stations_list = []
    stations_list = list(np.ravel(all_stations))

    # JSONIFY and return results

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def temps2():
    """Return a list of temperature observations between 2015-08-23 and 2016-08-23"""
   
    # Query for the dates & temperature observations from the previous year 2015-08-23 thru 2016-08-23

    avg_temp_year_list = []
    avg_temp_year_list = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2015-08-23').\
        filter(Measurement.date <= '2016-08-23').\
        order_by((Measurement.date).asc()).all() 
    
    # JSONIFY the list and return results

    return jsonify(avg_temp_year_list)


@app.route("/api/v1.0/<start>")

# Define a function to query Tmin, Tavg, Tmax using just a start date (i.e. no end date provided by user)

def calc_temp_no_end_date(start):
    """Obtain user input for start date and end date and return Tmin, Tavg, Tmax"""

# Obtain user input for start date

#    start_date = input('Enter the start date (format YYYY-MM-DD): ') 

# Query for Tmin, Tavg and Tmax for the date provided and jsonify the results

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")

# Define a function to query Tmin, Tavg, Tmax using both a start date and an end date

def calc_temps(start, end):
    """Obtain user input for start date and end date and return Tmin, Tavg, Tmax"""

# Obtain user input for start date and end date (Note: end date is optional)

#    start = input('Enter the start date (format YYYY-MM-DD): ') 
#    end = input('Enter the end date (format YYYY-MM-DD) (optional): ') 

# Query for Tmin, Tavg and Tmax for the date provided and jsonify the results
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)