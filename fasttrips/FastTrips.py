__copyright__ = "Copyright 2015 Contributing Entities"
__license__   = """
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import os
from operator import attrgetter
import transitfeed

from .Assignment import Assignment
from .Logger import FastTripsLogger, setupLogging
from .Passenger import Passenger
from .Route import Route
from .Stop import Stop
from .TAZ import TAZ
from .Trip import Trip

class FastTrips:
    """
    This is the model itself.  Should be simple and run pieces and store the big data structures.
    """

    #: Info log filename.  Writes brief information about program progression here.
    INFO_LOG  = "ft_info%s.log"

    #: Debug log filename.  Detailed output goes here, including trace information.
    DEBUG_LOG = "ft_debug%s.log"

    def __init__(self, input_network_dir, input_demand_dir, output_dir,
                 validate_gtfs=True, read_demand=True,
                 log_to_console=True, logname_append="", appendLog=False):
        """
        Constructor.

        Reads configuration and input files from *input_network_dir*.
        Writes output files to *output_dir*, including log files.

        :param input_network_dir: Location of network csv files to read
        :type input_network_dir:  string
        :param input_demand_dir:  Location of demand csv files to read
        :type input_demand_dir:   string
        :param output_dir:        Location to write output and log files.
        :type output_dir:         string
        :param validate_gtfs:     Validate the gtfs schedule?
        :type validate_gtfs:      bool
        :param read_demand:       Read passenger demand?  For parallelization, workers don't need to
                                  read demand since the main process will tell them what to do.
        :type read_demand:        bool
        :param log_to_console:    Log info to console as well as info log?
        :type log_to_console:     bool
        :param logname_append:    Modifier for info and debug log filenames.  So workers can write their own logs.
        :type logname_append:     string
        :param appendLog:         Append to info and debug logs?  When FastTrips assignment iterations (to
                                  handle capacity bumps), we'd like to append rather than overwrite.
        :type appendLog:          bool
        """
        #: :py:class:`collections.OrdederedDict` of :py:class:`fasttrips.Passenger` instances indexed by passenger's path ID
        self.passengers      = None

        #: :py:class:`dict` with :py:attr:`fasttrips.Route.route_id` key and :py:class:`fasttrips.Route` value
        self.routes          = None

        #: :py:class:`dict` with :py:attr:`fasttrips.Stop.stop_id` key and :py:class:`fasttrips.Stop` value
        self.stops           = None

        #: :py:class:`dict` with :py:attr:`fasttrips.TAZ.taz_id` key and :py:class:`fasttrips.TAZ` value
        self.tazs            = None

        #: :py:class:`dict` with :py:attr:`fasttrips.Trip.trip_id` key and :py:class:`fasttrips.Trip` value
        self.trips           = None

        #: string representing directory with input network data
        self.input_network_dir       = input_network_dir

        #: string representing directory with input demand data
        self.input_demand_dir       = input_demand_dir

        #: string representing directory in which to write our output
        self.output_dir      = output_dir

        #: transitfeed schedule instance.  See https://github.com/google/transitfeed
        self.gtfs_schedule   = None

        # Read the configuration
        Assignment.read_configuration(self.input_network_dir)

        # setup logging
        setupLogging(os.path.join(self.output_dir, FastTrips.INFO_LOG % logname_append),
                     os.path.join(self.output_dir, FastTrips.DEBUG_LOG % logname_append),
                     logToConsole=log_to_console, append=appendLog)

        self.read_input_files(validate_gtfs, read_demand)

    def read_input_files(self, validate_gtfs, read_demand):
        """
        Reads in the input files files from *input_network_dir* and initializes the relevant data structures.
        """
        # Read the gtfs files first
        FastTripsLogger.info("Reading GTFS schedule")
        loader             = transitfeed.Loader(self.input_network_dir)
        self.gtfs_schedule = loader.Load()

        if validate_gtfs:
            # Validate the GTFS
            FastTripsLogger.info("Validating GTFS schedule")
            self.gtfs_schedule.Validate()

        # Required: Trips, Routes, Stops, Stop Times, Agency, Calendar
        # Optional: Transfers, Shapes, Calendar Dates...

        # Read routes, agencies
        self.routes = Route(self.input_network_dir, self.gtfs_schedule, Assignment.TODAY)

        # Read Stops (gtfs-required) and transfers
        self.stops = Stop(self.input_network_dir, self.output_dir, self.gtfs_schedule)

        # Read trips, vehicles, calendar and stoptimes
        self.trips = Trip(self.input_network_dir, self.output_dir, self.gtfs_schedule, Assignment.TODAY, self.stops)

        # transfer_stops = 0
        # for stop_id,stop in self.stops.iteritems():
        #     if stop.is_transfer(): transfer_stops += 1
        # FastTripsLogger.info("Found %6d transfer stops" % transfer_stops)

        # read the TAZs into a TAZ instance
        self.tazs = TAZ(self.input_network_dir, Assignment.TODAY, self.stops)

        if read_demand:
            FastTripsLogger.info("-------- Reading demand --------")
            # Read the demand int passenger_id -> passenger instance
            self.passengers = Passenger(self.input_demand_dir, Assignment.TODAY, self.stops)
        else:
            self.passengers = None

    def run_assignment(self, output_dir):
        # Do it!
        Assignment.assign_paths(output_dir, self);