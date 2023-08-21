import os
from rembg.bg import remove
import numpy as np
import io
import cv2
from PIL import Image
import sys

def main(in_path, out_path):
	count = 0
	fails = []

	for f in os.listdir(in_path):
		try:
			count+=1
			if not os.path.exists(f'{out_path}/{f}'):
				print(f'{in_path}/{f}')
				img1 = cv2.imread(f'{in_path}/{f}')

				#replace 1024 on the next 2 lines with the resolution of the desired output
				f1 = 512 / img1.shape[1]
				f2 = 512 / img1.shape[0]
				fsz = min(f1, f2)  # resizing factor
				dim = (int(img1.shape[1] * fsz), int(img1.shape[0] * fsz))
				fl = cv2.resize(img1, dim)

				is_success, fl4 = cv2.imencode(".jpg", fl)
				fl3 = fl4.tobytes()

				result = remove(fl3)
				im5 = Image.open(io.BytesIO(result)).convert("RGBA")
				background = Image.new('RGBA', im5.size, (0,0,0))
				im52 = Image.alpha_composite(background, im5)
				img52 = im52.convert("RGB")
				im52 = im52.save(f'{out_path}/{f}')
				im = cv2.imread(f'{out_path}/{f}', cv2.IMREAD_UNCHANGED)
				mask = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY)[1]
				mask_filename = f"{os.path.splitext(f)[0]}_mask.png" 
				cv2.imwrite(os.path.join(out_path, mask_filename), mask)
				print(f'count:{count}  file: {f}')
			else:
				print(f'{f} exists, count: {count}')

		except Exception as e:
			print(sys.exc_info()[2])
			print(e)
			fails.append(f)
			failnames = np.array([fails])
			np.savetxt('failed_images.txt', failnames, delimiter='\n', fmt="%s")

if __name__ == '__main__':
	in_path = '/content/penguins/Test'
	out_path = '/content/penguins/sample_images'

	main(in_path, out_path)
