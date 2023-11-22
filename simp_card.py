from PIL import Image, ImageDraw, ImageFilter
import os
import requests


url = 'https://cdn.discordapp.com/avatars/606966821022597141/15a91f3d73944839fd879063dc2005a6.webp?size=512'
r = requests.get(url, allow_redirects=False)

open('simp_user.png', 'wb').write(r.content)

im1 = Image.open('simp_card.png')
im2 = Image.open('simp_user.png')

mask_im = Image.new("L", im2.size, 0)
draw = ImageDraw.Draw(mask_im)
draw.ellipse((120, 10, 430, 430), fill=255)

mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))

back_im = im1.copy()
back_im.paste(im2, (-20, 375), mask_im_blur)

try:
    os.remove("simp_card_id.png")
except:
    pass

back_im.save('simp_card_id.png', quality=100)


