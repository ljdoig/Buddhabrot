from utils import *
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-r', '--resolution', type=int, default=800,
    help="Resolution of output image"
  )
  parser.add_argument(
    '-I', '--iterlimit', type=int, default=2000,
    help="Iteration limit used to generate tally"
  )
  parser.add_argument(
    '-s', '--saturation', type=float, default=1.5,
    help="Multiplier used to scale pixel intensity"
  )
  parser.add_argument(
    '-n', '--new-points', type=int, default=0,
    help="Number of points to sample and add results tally"
  )
  parser.add_argument(
    '--fresh', action='store_true', 
    help="Start tally from scratch"
  )
  parser.set_defaults(fresh=False)
  args = parser.parse_args()

  tally = get_tally(
    res=args.resolution, 
    num_iters=args.iterlimit, 
    num_points=args.new_points,
    fresh=args.fresh
  )
  generate_greyscale_image(
    tally, 
    saturation_multiplier=args.saturation
  )
