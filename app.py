import numpy as np

import sqlalchemy
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
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
### Routes

#Home page.
    # Include a list of all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<b>Available Routes</b><br/>"
        f"<br/>"
        f"List of the dataset's most recent year's precipitation by date:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"<br/>"
        f"List of all stations which took measurements:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"<br/>"
        f"List of the dataset's most recent year's temperature by date:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"<br/>"
        f"List of the dataset's content, based on a user-supplied start date:<br/>"
        f"/api/v1.0/[start]"
        f"<br/>"
        f"<br/>"
        f"List of the dataset's content, based on a user-supplied start and end date:<br/>"
        f"/api/v1.0/[start]/[end]"
    )



# Should convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    # Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation"""

    # Create the session
    session = Session(engine)

    # Query the data
    results = session.query(Measurement.date, func.sum(Measurement.prcp))\
    .filter(Measurement.station == Station.station)\
    .filter(Measurement.date >= "2016-08-23")\
    .group_by(Measurement.station)\
    .order_by(func.sum(Measurement.prcp))\
    .all()

    # Convert the tuples into a normal list
    finalResults = list(np.ravel(results))

    # Return the results in a legible JSON format
    return jsonify(finalResults)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station():
    """Stations"""

    # Create the Session
    session = Session(engine)

    # Query the data
    results = session.query(Measurement.station)\
    .group_by(Measurement.station)\
    .all()

    # Convert the tuples into a normal list
    finalResults = list(np.ravel(results))

    return jsonify(finalResults)

# Query for the dates and temperature observations from a year from the last data point.
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    """TOBS"""

    # Create the Session
    session = Session(engine)

    # Query the data
    results = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date >= "2016-08-23")\
    .order_by(Measurement.date)\
    .all()

    # Convert the tuples into a normal list
    finalResults = list(np.ravel(results))

    return jsonify(finalResults)



# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def start(start):
    """Start"""

    # Create the Session
    session = Session(engine)

    # Query the data
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start)\
    .all()

    # Convert the tuples into a normal list
    finalResults = list(np.ravel(results))

    return jsonify(finalResults)

@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    """Start & End"""

    # Create the Session
    session = Session(engine)

    # Query the data
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start)\
    .filter(Measurement.date <= end)\
    .all()

    # Convert the tuples into a normal list
    finalResults = list(np.ravel(results))

    return jsonify(finalResults)


if __name__ == '__main__':
    app.run(debug=False)