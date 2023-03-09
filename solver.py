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
def process(img, color = (255, 0, 0), tolerance = 10):
  image_data = img.load()
  height, width = img.size
  r_min, r_max = max(0, color[0] - tolerance), min(255, color[0] + tolerance)
  g_min, g_max = max(0, color[1] - tolerance), min(255, color[1] + tolerance)
  b_min, b_max = max(0, color[2] - tolerance), min(255, color[2] + tolerance)
  for loop1 in range(height):
    for loop2 in range(width):
      pixel = image_data[loop1, loop2]
      if len(pixel) == 4:
          r, g, b, _ = pixel
          if not (r_min <= r <= r_max and g_min <= g <= g_max and b_min <= b <= b_max):
            image_data[loop1, loop2] = 0, 0, 0, 0
      else:
          r, g, b = pixel
          if not (r_min <= r <= r_max and g_min <= g <= g_max and b_min <= b <= b_max):
            image_data[loop1, loop2] = 0, 0, 0
  return img

def checkUrl(url) -> bool:
  if url is None:
    return False

  if not url.startswith("https://cdn.discordapp.com"):
    return False

  request = requests.get(url)
  return request.status_code == 200

def solveCaptcha(url) -> str:
  try:
    img = Image.open(requests.get(url, stream=True).raw)
    img = process(img)

    result = model(img)

    a = result.pandas().xyxy[0].sort_values('xmin')
    while len(a) > 6: # TODO: custom value for longer/shorter captchas
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