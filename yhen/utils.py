import qrcode
from io import BytesIO
import base64

def qrcode_create(data):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(data)
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	buffer = BytesIO()
	img.save(buffer)
	img_str = base64.b64encode(buffer.getvalue()).decode()
	return f"data:image/png;base64,{img_str}"

def date_notime(date):
	return date[:10]
