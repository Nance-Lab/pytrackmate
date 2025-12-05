import numpy as np
from nd2reader import ND2Reader
import skimage.io as sio
from pathlib import Path


def process_nd2_to_sixteenths(nd2_file):
    """Convert ND2 to TIF and split into 16 tiles (256x256 each)"""
    # Read ND2 file
    with ND2Reader(nd2_file) as images:
        img = np.array(images)
    
    # Pad to 1024x1024 if needed
    oshape = img.shape
    padded = np.zeros((oshape[0], 2044, 2048), dtype=img.dtype)
    padded[:, :oshape[1], :oshape[2]] = img
    
    # Get original file's directory and name
    nd2_path = Path(nd2_file)
    output_dir = nd2_path.parent
    output_name = nd2_path.stem
    
    # Save full TIF in original directory
    full_tif = output_dir / f"{output_name}.tif"
    sio.imsave(str(full_tif), padded)
    
    # Split into 16ths (4x4 grid of 256x256 tiles) and save in original directory
    tile_files = []
    for row in range(4):
        for col in range(4):
            tile = padded[:, row*256:(row+1)*256, col*256:(col+1)*256]
            filename = output_dir / f"{output_name}_{row}_{col}.tif"
            sio.imsave(str(filename), tile)
            tile_files.append(str(filename))
    
    return tile_files

# Usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        files = process_nd2_to_sixteenths(sys.argv[1])
        print(f"Created {len(files)} tiles: {', '.join(files)}")
    else:
        print("Usage: python script.py <file.nd2>")