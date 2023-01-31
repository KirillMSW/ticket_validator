import string
import random
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask
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
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(ticket_id)
    qr.make(fit=True)
    img = qr.make_image(image_factory=StyledPilImage,color_mask=HorizontalGradiantColorMask(back_color=(255,255,255),left_color=(116,44,154),right_color=(207,64,238)))
    # img.save("some_file.png")

    # img = qrcode.make(ticket_id)
    im1 = Image.open('qr_background7.jpg')
    img=img.resize((320,320))
    back_im = im1.copy()
    back_im.paste(img,(369,500))
    font = ImageFont.truetype('fonts/agencyfbcyrillic.ttf', 120)
    I1 = ImageDraw.Draw(back_im)
    I1.text((534, 1350), ticket_id,font=font, fill=(255, 255, 255), anchor="ma")
    I1.multiline_text((534, 1500), client_name,font=font, fill=(255, 255, 255), anchor="ma",align='center')
    back_im.save("tickets/"+str(ticket_id)+'.png', quality=75)

generate_ticket("QWERT","Счастливцева\nВиктория\nВладимировна")
