

# filepaths
fp_in = r"C:/Users/volochkov/Documents/OneDrive/Документы/UI showcase/gir"
fp_out = "C:/Users/volochkov/Documents/OneDrive/Документы/UI showcase/gir.gif"

import glob
from PIL import Image
def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    frame_one = frames[0]
    frame_one.save(fp_out, format="GIF", append_images=frames,
               save_all=True, duration=800, loop=0)
    
if __name__ == "__main__":
    make_gif(fp_in)