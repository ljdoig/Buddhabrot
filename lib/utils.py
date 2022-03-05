import csv
import random
import cmath
import datetime as dt
import PIL.Image as pim
import numpy as np
from math import pi
import os.path
from tqdm import trange

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

OUTDIR = "../output"
CSVDIR = "../csvs"

# no need to change these values
# unlike with mandelbrot/julia sets, field of view doesn't make plotting quicker
ABSBOUND = 2
CENTRE = (-0.5, 0)
SCALE = 2

def trace_paths(tally, num_iters):
  zinit = cmath.rect(random.uniform(0, 3/2*ABSBOUND), random.uniform(0, 2*pi))
  z = 0
  path = []
  while abs(z) < ABSBOUND and len(path) < num_iters:
    z = z*z + zinit
    path.append((z.real, z.imag))
  if abs(z) >= ABSBOUND:
    num_xbins = np.shape(tally)[0]
    num_ybins = np.shape(tally)[1]
    for point in path:
      xprop = (point[0] - (CENTRE[0] - SCALE))/(2*SCALE)
      yprop = (point[1] - (CENTRE[1] - SCALE))/(2*SCALE)
      if (0 <= yprop and yprop < 1 and 0 <= xprop and xprop < 1):
        tally[int(num_xbins * xprop), int(num_ybins * yprop)] += 1
  return

def populate_tally(tally, num_iters, num_points):
  for _ in trange(num_points):
    
    trace_paths(tally, num_iters)
  return tally

def get_tally(res, num_iters, num_points, fresh=False, csvdir=CSVDIR):
  csv_basename = f"res{res}_maxiters{num_iters}.csv.gz"
  csv_filename = f"{csvdir}/{csv_basename}"
  if os.path.exists(csv_filename) and not fresh:
    print("Tally already exists, loading from csv")
    tally = np.loadtxt(csv_filename, delimiter = ",")
  else:
    print(f"Initialising tally with dimension {res}x{res}")
    tally = np.zeros((res,res))
  if num_points > 0:
    print(f"Adding {num_points} points to tally with iteration limit {num_iters}")
    tally = populate_tally(tally, num_iters, num_points)
    if not fresh:
      print("Saving tally to csv")
      np.savetxt(csv_filename, tally, delimiter=",")
  else:
    print("Tally ready", end = "\n\n")
  return tally

def get_tallies(res, num_iters_list, num_points, fresh=False, csvdir=CSVDIR):
  print("Getting 3 tallies, one each for RGB pixels", end = "\n\n")
  return tuple(
    get_tally(res, num_iters, num_points, fresh, csvdir) 
    for num_iters in num_iters_list
  )

def generate_greyscale_image(
  tally, saturation_multiplier, outdir=OUTDIR, quantile=0.99
  ):
  print("Generating gresycale image from tally")
  image = pim.new("L", np.shape(tally))
  tally_normaliser = np.quantile(tally.flatten(), quantile)
  if tally_normaliser > 0:
    for row in trange(np.shape(tally)[0]):
      for col in range(np.shape(tally)[1]):
        # between 0 and saturation_multiplier
        normalised_pixel = saturation_multiplier * (
          tally[row, col] / tally_normaliser
        )
        pixel = int(normalised_pixel * 255)
        # swap row and col so that the shape is upright
        image.putpixel((col, row), pixel)
  date_time = dt.datetime.now()
  date_time_str = date_time.strftime("%Y_%m_%d-%H_%M_%S")
  image.save(f"{outdir}/{date_time_str}.png")

def generate_colour_image(
  rgb_tallies, saturation_multiplier, outdir=OUTDIR, quantile=0.995
  ):
  # check all tallies have the same shape
  shapes = [np.shape(tally) for tally in rgb_tallies]
  assert(shapes.count(shapes[0]) == len(shapes))
  shape = shapes[0]
  
  print("Generating colour image from tallies")
  image = pim.new("RGB", shape)
  tally_normalisers = [
    np.quantile(tally.flatten(), quantile) for tally in rgb_tallies
  ]
  for row in trange(shape[0]):
    for col in range(shape[1]):
      # between 0 and saturation_multiplier
      normalised_pixel = tuple(
        saturation_multiplier * (tally[row, col] / tally_normaliser)
        for tally, tally_normaliser in zip(rgb_tallies, tally_normalisers)
      )
      pixel = tuple(int(normalised * 255) for normalised in normalised_pixel)
      # swap row and col so that the shape is upright
      image.putpixel((col, row), pixel)
  date_time = dt.datetime.now()
  date_time_str = date_time.strftime("%Y_%m_%d-%H_%M_%S")
  image.save(f"{outdir}/{date_time_str}.png")
