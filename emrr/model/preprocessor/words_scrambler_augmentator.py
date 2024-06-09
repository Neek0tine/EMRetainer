import sys
from PIL import Image
import glob,random
import os
import random

listpics = glob.glob(r"src\randompics\*.png")


for n in range(0, 420):
  mergecandidates = random.sample(listpics, 5)
  print(mergecandidates)

  images = [Image.open(x) for x in  mergecandidates]
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)
  max_height = max(heights)

  new_im = Image.new('RGB', (total_width, max_height))

  x_offset = 5
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

  new_im.save(f'./src/augmented/test{n}.jpg')
  n += 1