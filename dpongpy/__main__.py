import dpongpy.model
import argparse


def arg_parser():
    ap = argparse.ArgumentParser()
    # ap.add_argument("--help", action="store_true", help="Show this help message and exit")
    mode = ap.add_argument_group("mode")
    mode.add_argument("--mode", choices=['local', 'centralised'], help="Run the game in local or centralised mode")
    mode.add_argument("--role", required=False, choices=['coordinator', 'terminal'], help="Run the game with a central coordinator, in either coordinator or terminal role")
    networking = ap.add_argument_group("networking")
    networking.add_argument("--host", help="Host to connect to", type=str, default="localhost")
    networking.add_argument("--port", help="Port to connect to", type=int, default=None)
    game = ap.add_argument_group("game")
    game.add_argument("--side", choices=[dir.name.lower() for dir in dpongpy.model.Direction.values()], help="Side to play on", action="append", default=[])
    game.add_argument("--debug", help="Enable debug mode", action="store_true")
    game.add_argument("--size", help="Size of the game window", type=int, nargs=2, default=[900, 600])
    game.add_argument("--fps", help="Frames per second", type=int, default=60)
    return ap


def args_to_settings(args):
    settings = dpongpy.Settings()
    settings.host = args.host
    settings.port = args.port
    settings.debug = args.debug
    settings.size = tuple(args.size)
    settings.fps = args.fps
    settings.initial_paddles = [dpongpy.model.Direction[dir.upper()] for dir in args.side]
    return settings


parser = arg_parser()
args = parser.parse_args()
settings = args_to_settings(args)
# if args.help:
#     parser.print_help()
#     exit(0)
if args.mode == 'local':
    if not settings.initial_paddles:
        settings.initial_paddles = [dpongpy.model.Direction.LEFT, dpongpy.model.Direction.RIGHT]
    dpongpy.main(settings)
    exit(0)
if args.mode == 'centralised':
    import dpongpy.remote.centralised
    if args.role == 'coordinator':
        dpongpy.remote.centralised.main_coordinator(settings)
        exit(0)
    if args.role == 'terminal':
        dpongpy.remote.centralised.main_terminal(settings)
        exit(0)
    print(f"Invalid role: {args.role}. Must be either 'coordinator' or 'terminal'")
parser.print_help()
exit(1)
