from utils import *
from pygifsicle import optimize
import imageio as iio
import os

date_time = dt.datetime.now()
date_time_str = date_time.strftime("%Y_%m_%d-%H_%M_%S")
gif_path = f"../gifs/{date_time_str}_res.gif"
frame_dir = f"../gifs/{date_time_str}_resgif_frames"
os.mkdir(frame_dir)

num_frames = 8
scale_factor = 2

min_res = 8
num_iters = 500
num_points = 500000
saturation = 0.5

max_res = min_res * scale_factor**(num_frames - 1)
print(f"Max resolution: {max_res}\n")

res = min_res
for i in range(num_frames):
  print(f"Frame: {i}")
  random.seed(0)
  tally = get_tally(res, num_iters, num_points, fresh=True)
  generate_greyscale_image(tally, saturation, outdir=frame_dir)
  res *= scale_factor
  print("\n")

def scale_up_res(image_path, to_res):
  old_image = pim.open(image_path)
  scaled_up = pim.new("L", (to_res, to_res))
  assert to_res % old_image.size[0] == 0
  factor = to_res // old_image.size[0]
  print(f"Scale factor: {factor}")
  if factor == 1:
    print("No need to scale")
    return
  # loop over pixels in old im and load them into corresponding region in new im
  for row in range(old_image.size[0]):
      for col in range(old_image.size[1]):
        pixel = old_image.getpixel((row, col))
        for i in range(factor * row, factor * (row + 1)):
          for j in range(factor * col, factor * (col + 1)):
            scaled_up.putpixel((i, j), pixel)
  # overwrite old image
  scaled_up.save(image_path)

with iio.get_writer(gif_path, mode='I', fps=1) as writer:
  for i, image_basename in enumerate(sorted(os.listdir(frame_dir))):
    print(f"Scaling up image {i}")
    scale_up_res(f"{frame_dir}/{image_basename}", to_res=max_res)
    writer.append_data(iio.imread(f"{frame_dir}/{image_basename}"))
    print("")
  for image_basename in sorted(os.listdir(frame_dir), reverse=True):
    writer.append_data(iio.imread(f"{frame_dir}/{image_basename}"))


print("Optimizing")
optimize(gif_path)
