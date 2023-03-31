"""Defines command line entrypoints to the this library."""
import asyncio
import sys
import functools
import logging
import coloredlogs
from . import load
from . import migration
from . import logger


def _call_with_sys_argv(function):
    @functools.wraps(function)
    def call_with_sys_argv():
        coloredlogs.install(level='INFO', logger=logger)
        logger.setLevel(logging.INFO)
        function(*sys.argv[1:])
    return call_with_sys_argv


@_call_with_sys_argv
def convert_replay(path):
    """Convert the game provided through sys.argv."""
    load._CarballToNumpyConverter(
        load.get_carball_game(path)
    ).get_numpy_array()


@_call_with_sys_argv
def fill_cache_with_tracker_rank(filepath):
    """Fill a player info cache in a directory of replays."""
    loop = asyncio.get_event_loop()
    task = migration.populate_player_cache_from_directory_using_tracker_network(filepath)
    loop.run_until_complete(task)


@_call_with_sys_argv
def _iter_cache(filepath):
    import json
    from . import player_cache as cache
    missing_data = 0
    present_data = 0
    for player_key, player_data in cache.PlayerCache.new_with_cache_directory(filepath):
        if isinstance(player_data, dict):
            print(json.dumps(player_data))
        pass
        '''
        if player_data is cache.PlayerNotFoundOnTrackerNetwork:
            missing_data += 1
        else:
            present_data += 1
            '''

    #print(f"missing data: {missing_data}, present_data: {present_data}")


@_call_with_sys_argv
def _copy_games(source, dest):
    task = migration.copy_games_if_metadata_available_and_conditions_met(source, dest)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
