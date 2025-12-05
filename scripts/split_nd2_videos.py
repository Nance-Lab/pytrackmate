import numpy as np
from nd2reader import ND2Reader
import skimage.io as sio
from pathlib import Path

def process_nd2_to_quadrants(nd2_file):
    """Convert ND2 to TIF and split into 4 quadrants (512x512 each)"""
    # Read ND2 file
    with ND2Reader(nd2_file) as images:
        img = np.array(images)
    
    # Pad to 1024x1024 if needed
    oshape = img.shape
    padded = np.zeros((oshape[0], 1024, 1024), dtype=img.dtype)
    padded[:, :oshape[1], :oshape[2]] = img
    
    # Get original file's directory and name
    nd2_path = Path(nd2_file)
    output_dir = nd2_path.parent
    output_name = nd2_path.stem
    
    # Save full TIF in original directory
    full_tif = output_dir / f"{output_name}.tif"
    sio.imsave(str(full_tif), padded)
    
    # Split into quadrants and save in original directory
    quadrant_files = []
    for row in range(2):
        for col in range(2):
            quadrant = padded[:, row*512:(row+1)*512, col*512:(col+1)*512]
            filename = output_dir / f"{output_name}_{row}_{col}.tif"
            sio.imsave(str(filename), quadrant)
            quadrant_files.append(str(filename))
    
    return quadrant_files

# Usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        files = process_nd2_to_quadrants(sys.argv[1])
        print(f"Created: {', '.join(files)}")
    else:
        print("Usage: python script.py <file.nd2>")