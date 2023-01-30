import string
import random
import qrcode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def generate_ticket_id():
    length=5
    letters = list(string.ascii_uppercase + string.digits)
    random.shuffle(letters)
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_ticket(ticket_id, client_name):
    img = qrcode.make(ticket_id)
    im1 = Image.open('qr_background.jpg')
    img=img.resize((600,600))
    back_im = im1.copy()
    back_im.paste(img,(240,700))
    font = ImageFont.truetype('fonts/Arial Unicode.ttf', 50)
    I1 = ImageDraw.Draw(back_im)
    I1.text((540, 1400), ticket_id,font=font, fill=(255, 255, 255), anchor="ma")
    I1.text((540, 1500), client_name,font=font, fill=(255, 255, 255), anchor="ma")
    back_im.save("tickets/"+str(ticket_id)+'.png', quality=75)

