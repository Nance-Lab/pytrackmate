import multiprocessing as mp
import time
import os
import glob as gb

def process_videos_parallel(args):
  '''
  Processes a single video in parallel.

  Parameters
  ----------
  args: tuple
      Includes the video to process, Trackmate function to use, and the
      arguments to use for the given Trackmate function, respectively.

  Raises
  ------
  ValueError
      If the given Trackmate function arguments do not work with the given Trackmate script
  '''
  
  video, trackmate_fn, trackmate_fn_args = args

  # see if the script is valid
  if not os.path.isfile(trackmate_fn):
    print("Invalid script provided")
    return

  try:
    os.system(f'{trackmate_fn} {video} {trackmate_fn_args}')
  except ValueError:
    print(f'Could not execute script with the given arguments')


def run_trackmate_parallel(path, trackmate_fn, trackmate_fn_args, num_threads=mp.cpu_count()):
  '''
  Enables parallel processing of multiple tif files by Trackmate.

  Parameters
  ----------
  path: str
      The path to the images to be processed
  trackmate_fn: str
      The name of the Trackmate script to use
  trackmate_fn_args: tuple
      The arguments the Trackmate function takes
  num_threads: int
      The number of threads/cores to use (default: max cores available).
      If the threads entered exceeds the number available, the max number of threads
      available will be used.
  
  Outputs
  ----------
  Tracking results from each tif file (i.e. a Tuple of csv files, where each element
  of the Tuple is the tracking data csv from a video.
  '''

  threads_avail = mp.cpu_count()
  if num_threads > threads_avail:
    print(f'Provided number of threads exceeds the number available. \
          Using max number available ({threads_avail}) instead.')
    num_threads = threads_avail

  pool = mp.Pool(num_threads)

  if not os.path.exists(path):
    print('Path not found')
    return

  # get all the videos in the provided path
  videos = gb.glob(path + "/*.tif")

  start_time = time.perf_counter()

  # create the arguments that `process_videos_parallel` will take
  args = [(video, trackmate_fn, trackmate_fn_args) for video in videos]
  
  pool.starmap(process_videos_parallel, args)

  # pool.apply_async(process_videos_parallel, args=(videos, trackmate_fn, trackmate_fn_args))
  # pool.apply(process_videos_parallel, args=trackmate_args)
  
  finish_time = time.perf_counter()
  print(f"Program finished in {finish_time-start_time} seconds.")

  pool.close()

