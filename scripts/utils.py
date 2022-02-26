import csv
import random
import cmath
import datetime as dt
import PIL.Image as pim
import numpy as np
from math import pi
from os.path import exists
from tqdm import trange

OUTDIR = "./output/"
CSVDIR = "./csvs/"

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

def get_tally(res, num_iters, num_points):
  csv_basename = f"res{res}_maxiters{num_iters}.csv.gz"
  csv_filename = CSVDIR + csv_basename
  if exists(csv_filename):
    print("Tally already begun, loading from csv")
    tally = np.loadtxt(csv_filename, delimiter = ",")
  else:
    print(f"Initialising tally with dimension {res}x{res}")
    tally = np.zeros((res,res))
  print(f"Adding {num_points} points to tally")
  tally = populate_tally(tally, num_iters, num_points)
  np.savetxt(csv_filename, tally, delimiter=",")
  return tally

def generate_greyscale_image(tally, saturation_multiplier):
  print("Generating image from tally")
  image = pim.new("L", np.shape(tally))
  tally_max = np.amax(tally)
  for row in trange(np.shape(tally)[0]):
    for col in range(np.shape(tally)[1]):
      # between 0 and saturation_multiplier
      normalised_pixel = saturation_multiplier * (tally[row, col] / tally_max)
      pixel = int(normalised_pixel * 255)
      # swap row and col so that the shape is upright
      image.putpixel((col, row), pixel)
  date_time = dt.datetime.now()
  date_time_str = date_time.strftime("%Y_%m_%d-%H_%M_%S")
  image.save(f"{OUTDIR}{date_time_str}.png")

if __name__ == "__main__":
  res = 800
  num_iters = 1000
  num_extra_points = 0
  
  saturation_multiplier = 1.5

  tally = get_tally(res, num_iters, num_extra_points)
  generate_greyscale_image(tally, saturation_multiplier)