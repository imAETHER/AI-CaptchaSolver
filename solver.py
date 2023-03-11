import requests
import torch
from PIL import Image
from colorama import init, Fore
init()

# Model
print(Fore.CYAN + 'Loading model')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/best.pt')
print(Fore.GREEN + 'Model loaded')

# Removes the everything but the actual characters
def process(img, hex_color, tolerance = 20):
  image_data = img.load()
  height, width = img.size
  r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) #hex to rgb
  r_min, r_max = max(0, r - tolerance), min(255, r + tolerance)
  g_min, g_max = max(0, g - tolerance), min(255, g + tolerance)
  b_min, b_max = max(0, b - tolerance), min(255, b + tolerance)
  for loop1 in range(height):
    for loop2 in range(width):
      try:
        pixel_r, pixel_g, pixel_b, _ = image_data[loop1, loop2]
      except ValueError:
        pixel_r, pixel_g, pixel_b = image_data[loop1, loop2]
      if not (r_min <= pixel_r <= r_max and g_min <= pixel_g <= g_max and b_min <= pixel_b <= b_max):
        image_data[loop1, loop2] = 0, 0, 0, 0
  return img

def solveCaptcha(url, color = None) -> str:
  try:
    img = Image.open(requests.get(url, stream=True).raw)
    if color is not None:
      img = process(img, color)

    result = model(img)

    a = result.pandas().xyxy[0].sort_values('xmin')
    while len(a) > 6: #TODO: custom value for longer/shorter captchas
      lines = a.confidence
      linev = min(a.confidence)
      for line in lines.keys():
        if lines[line] == linev:
          a = a.drop(line)

    result = ""
    for _, key in a.name.items():
      result = result + key
    
    print(Fore.CYAN + f"[i | Solve] Captcha: {result}")
    return result
  except:
    print(Fore.RED + 'Failed to solve a captcha!')
    return None
