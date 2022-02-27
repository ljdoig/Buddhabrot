from utils import *
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-r', '--resolution', type=int, default=800,
    help="Resolution of output image"
  )
  parser.add_argument(
    '-R', '--red-iterlimit', type=int, default=2000,
    help="Iteration limit used to generate red-pixel tally"
  )
  parser.add_argument(
    '-G', '--green-iterlimit', type=int, default=200,
    help="Iteration limit used to generate green-pixel tally"
  )
  parser.add_argument(
    '-B', '--blue-iterlimit', type=int, default=20,
    help="Iteration limit used to generate blue-pixel tally"
  )
  parser.add_argument(
    '-s', '--saturation', type=float, default=1.5,
    help="Multiplier used to scale pixel intensity"
  )
  parser.add_argument(
    '-n', '--new-points', type=int, default=0,
    help="Number of samples drawn to add to tally"
  )
  parser.add_argument(
    '--fresh', action='store_true', 
    help="Start tally from scratch"
  )
  parser.set_defaults(fresh=False)
  args = parser.parse_args()

  rgb_tallies = get_tallies(
    res=args.resolution, 
    num_iters_list=[
      args.red_iterlimit,
      args.green_iterlimit,
      args.blue_iterlimit
    ], 
    num_points=args.new_points,
    fresh=args.fresh
  )
  generate_colour_image(
    rgb_tallies, 
    saturation_multiplier=args.saturation
  )
