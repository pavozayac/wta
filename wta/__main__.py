from argparse import ArgumentParser
import argparse
import plotly.express as px
from wta.analysis.clusters import ClusterAnalysisService

from wta.analysis.speeding_locations import SpeedingLocationService
from wta.analysis.speeds import SpeedAnnotationService
from wta.api.generic.access_service import ApiAccessService, EnvApiAccessService
from wta.api.locations.bus_location_service import ApiBusLocationService
from wta.api.routes.route_service import ApiRouteService

from wta.api.schedules.schedule_service import ApiScheduleService
from wta.api.stops.stop_loc_service import ApiStopLocationService, StopLocationService
from wta.downloaders.location_downloader import LocationDownloaderService
from wta.storage.full_schedule_repo import JSONScheduleRepository
from wta.storage.location_repo import JSONLocationRepository
from wta.storage.processing_repo import CsvRepo


parser = ArgumentParser(prog='wta', description='''
                        This program can collect data from the public API of the Warsaw city available online,
                        process it, analyse and produce visualizations.
                        ''')

parser.add_argument(
    '-f', '--filepath',
    nargs='?',
    help='Path for saving / using a file if -c or -p is used.',
    type=str)

parser.add_argument(
    '-lf', '--locfile',
    nargs='?',
    default=None,
    help='Path for using a bus locations file if -p is used.',
    type=str)

parser.add_argument('-c', '--collect', action='store_true',
                    help='Collect data from the public API.', default=False)

parser.add_argument(
    '-p',
    '--process',
    action='store_true',
    help='Process collected data.',
    default=False)
parser.add_argument(
    '-v',
    '--visualise',
    action='store_true',
    help='Generate visualisations.',
    default=False)

parser.add_argument(
    '--schedule',
    action='store_true',
    default=False,
    help='''Mode of operation: "schedule" or "locations" for --collect.''')

parser.add_argument(
    '--locations',
    action='store_true',
    default=False,
    help='''Mode of operation: "schedule" or "locations" for --collect.''')

parser.add_argument(
    '--speeding',
    action='store_true',
    default=False,
    help='''Mode of operation: "speeding" or "clusters" for --visualize.''')

parser.add_argument(
    '--clusters',
    action='store_true',
    default=False,
    help='''Mode of operation: "speeding" or "clusters" for --visualize.''')

parser.add_argument('--lines', nargs='+', type=list[str],
                    help='Number of ones whose scheduled stops are to be collected.',
                    )

args = parser.parse_args()

access_service = EnvApiAccessService()

if args.collect:
    if args.schedule:
        if args.lines is None:
            raise argparse.ArgumentError(args.lines,
                                         'This argument is required for the "schedule" mode.')

        routes = ApiRouteService(access_service).get_routes()
        routes = {k: v for k, v in routes.items() if k in args.lines}

        stops = ApiStopLocationService(access_service).get_stop_locations()

        schedule = ApiScheduleService(access_service).get_full_schedules(routes, stops)

        s_repo = JSONScheduleRepository(args.filepath)

        s_repo.save_schedule(schedule)
    elif args.locations:
        downloader = LocationDownloaderService(
            access_service,
            ApiBusLocationService(),
            JSONLocationRepository(args.filepath), file_name=args.filepath)

elif args.process:
    if args.locfile is None:
        raise argparse.ArgumentError(args.locfile,
                                     'This argument is required for the "process" mode.')

    annot = SpeedAnnotationService()
    repo = CsvRepo(args.filepath)
    speed_s = SpeedingLocationService(annot)
    speeding = speed_s.get_annotated_locations(
        JSONLocationRepository(args.locfile).get_locations())

    repo.save_csv(speeding)


elif args.visualise:
    speeding = CsvRepo(args.filepath).load_csv()

    if args.speeding:
        fig = px.scatter_mapbox(
            speeding,
            lat='Lat',
            lon='Lon',
            hover_data=['speed'],
            color='speed',
        )

        fig.update_layout(mapbox_style='open-street-map')

        fig.show()

    elif args.clusters:
        clusters, noise = ClusterAnalysisService.get_clusters(speeding, 0.01)

        fig2 = px.scatter_mapbox(
            clusters,
            lat='Lat',
            lon='Lon',
            color_discrete_sequence=[px.colors.label_rgb((255, 0, 0))]
        )

        fig2.update_layout(mapbox_style='open-street-map')

        fig2.show()
