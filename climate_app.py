{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "891ab0d8-9995-4892-8d45-58984c07ad04",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import Flask\n",
    "from flask import Flask, jsonify"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "f9179ae0-d734-4f5c-928e-9c9cbd2fa3ce",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Dependencies and Setup\n",
    "import numpy as np\n",
    "import datetime as dt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "38e915b7-be96-4228-ba68-90f6c5e761c7",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Python SQL Toolkit and Object Relational Mapper\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "from sqlalchemy.pool import StaticPool"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "b21b4559-aea9-47f6-ba01-4d40ed4d5cec",
   "metadata": {},
   "outputs": [],
   "source": [
    "#################################################\n",
    "# Database Setup\n",
    "#################################################\n",
    "# Reference: https://stackoverflow.com/questions/33055039/using-sqlalchemy-scoped-session-in-theading-thread\n",
    "Engine = create_engine(\"sqlite:///hawaii.sqlite\", connect_args={\"check_same_thread\": False}, poolclass=StaticPool, echo=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "4be27d56-b985-4234-b41f-d364c8364f02",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Reflect Existing Database Into a New Model\n",
    "Base = automap_base()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "96102780-ee33-4425-8f89-b8ff045d4c44",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Reflect the Tables\n",
    "Base.prepare(engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "ebc8f9c1-356c-4672-8e86-d496a1126abd",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create Session (Link) From Python to the DB\n",
    "Session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fcc6276c-d9ca-4774-b4b2-e7983c8a1e80",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save References to Each Table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "442ef38c-bcb9-4480-8288-e49745fd6b36",
   "metadata": {},
   "outputs": [],
   "source": [
    "#################################################\n",
    "# Flask Setup\n",
    "#################################################\n",
    "app = Flask(__name__)\n",
    "\n",
    "#################################################\n",
    "# Flask Routes\n",
    "#################################################\n",
    "# Home Route\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "        return \"\"\"<html>\n",
    "<h1>Hawaii Climate App (Flask API)</h1>\n",
    "<img src=\"https://i.ytimg.com/vi/3ZiMvhIO-d4/maxresdefault.jpg\" alt=\"Hawaii Weather\"/>\n",
    "<p>Precipitation Analysis:</p>\n",
    "<ul>\n",
    "  <li><a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation</a></li>\n",
    "</ul>\n",
    "<p>Station Analysis:</p>\n",
    "<ul>\n",
    "  <li><a href=\"/api/v1.0/stations\">/api/v1.0/stations</a></li>\n",
    "</ul>\n",
    "<p>Temperature Analysis:</p>\n",
    "<ul>\n",
    "  <li><a href=\"/api/v1.0/tobs\">/api/v1.0/tobs</a></li>\n",
    "</ul>\n",
    "<p>Start Day Analysis:</p>\n",
    "<ul>\n",
    "  <li><a href=\"/api/v1.0/2017-03-14\">/api/v1.0/2017-03-14</a></li>\n",
    "</ul>\n",
    "<p>Start & End Day Analysis:</p>\n",
    "<ul>\n",
    "  <li><a href=\"/api/v1.0/2017-03-14/2017-03-28\">/api/v1.0/2017-03-14/2017-03-28</a></li>\n",
    "</ul>\n",
    "</html>\n",
    "\"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "7d6202f8-a0fb-4708-aa28-64cf427356bd",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Precipitation Route\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value\n",
    "        # Calculate the Date 1 Year Ago from the Last Data Point in the Database\n",
    "        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)\n",
    "        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values\n",
    "        prcp_data = session.query(Measurement.date, Measurement.prcp).\\\n",
    "                filter(Measurement.date >= one_year_ago).\\\n",
    "                order_by(Measurement.date).all()\n",
    "        # Convert List of Tuples Into a Dictionary\n",
    "        prcp_data_list = dict(prcp_data)\n",
    "        # Return JSON Representation of Dictionary\n",
    "        return jsonify(prcp_data_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "63e1a470-7003-480f-afec-b3ba70164131",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Station Route\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "        # Return a JSON List of Stations From the Dataset\n",
    "        stations_all = session.query(Station.station, Station.name).all()\n",
    "        # Convert List of Tuples Into Normal List\n",
    "        station_list = list(stations_all)\n",
    "        # Return JSON List of Stations from the Dataset\n",
    "        return jsonify(station_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "id": "476a0237-23b8-4ed2-86f1-778894307115",
   "metadata": {},
   "outputs": [],
   "source": [
    "# TOBs Route\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "        # Query for the Dates and Temperature Observations from a Year from the Last Data Point\n",
    "        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)\n",
    "        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values\n",
    "        tobs_data = session.query(Measurement.date, Measurement.tobs).\\\n",
    "                filter(Measurement.date >= one_year_ago).\\\n",
    "                order_by(Measurement.date).all()\n",
    "        # Convert List of Tuples Into Normal List\n",
    "        tobs_data_list = list(tobs_data)\n",
    "        # Return JSON List of Temperature Observations (tobs) for the Previous Year\n",
    "        return jsonify(tobs_data_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "id": "ef4d519a-6d3d-46eb-9cae-db6757d1fd1d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Start Day Route\n",
    "@app.route(\"/api/v1.0/<start>\")\n",
    "def start_day(start):\n",
    "        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "                filter(Measurement.date >= start).\\\n",
    "                group_by(Measurement.date).all()\n",
    "        # Convert List of Tuples Into Normal List\n",
    "        start_day_list = list(start_day)\n",
    "        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range\n",
    "        return jsonify(start_day_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "id": "c6b16369-27fb-4776-98f6-87509f883c49",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Start-End Day Route\n",
    "@app.route(\"/api/v1.0/<start>/<end>\")\n",
    "def start_end_day(start, end):\n",
    "        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "                filter(Measurement.date >= start).\\\n",
    "                filter(Measurement.date <= end).\\\n",
    "                group_by(Measurement.date).all()\n",
    "        # Convert List of Tuples Into Normal List\n",
    "        start_end_day_list = list(start_end_day)\n",
    "        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range\n",
    "        return jsonify(start_end_day_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "id": "abd0b638-f0e1-4b62-b76b-4cdbc5c26f45",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Restarting with windowsapi reloader\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    }
   ],
   "source": [
    "# Define Main Behavior\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
