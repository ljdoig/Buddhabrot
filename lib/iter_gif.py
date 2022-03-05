from utils import *
from pygifsicle import optimize
import imageio as iio
import os

date_time = dt.datetime.now()
date_time_str = date_time.strftime("%Y_%m_%d-%H_%M_%S")
gif_path = f"../gifs/{date_time_str}.gif"
frame_dir = f"../gifs/{date_time_str}_itergif_frames"
os.mkdir(frame_dir)

num_frames = 70

res = 1000
min_iters = 10
num_points = 1000000
saturation = 0.6

num_iters = min_iters
multiplier = 1.1
for i in range(num_frames):
  print(f"Frame: {i}")
  random.seed(0)
  num_iters = int(multiplier * num_iters) + 1
  tally = get_tally(res, num_iters, num_points, fresh=True)
  generate_greyscale_image(tally, saturation, outdir=frame_dir)
  print("\n")

with iio.get_writer(gif_path, mode='I') as writer:
  for image_filename in sorted(os.listdir(frame_dir)):
    writer.append_data(iio.imread(f"{frame_dir}/{image_filename}"))
  for image_filename in sorted(os.listdir(frame_dir), reverse=True):
    writer.append_data(iio.imread(f"{frame_dir}/{image_filename}"))

print("Optimizing")
optimize(gif_path)
