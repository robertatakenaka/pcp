# coding = utf-8

import os

from PIL import Image


#inkscape PATH/teste.svg --export-background=COLOR --export-area-drawing --export-area-snap --export-dpi=300 --export-png=PATH/leave2.png

def command():
    INKSCAPE_PATH = 'inkscape'
    commands_parts = [
        INKSCAPE_PATH,
        '{}',
        '--export-background=COLOR',
        '--export-area-drawing',
        '--export-area-snap',
        '--export-dpi=300',
        '--export-png={}'
    ]
    return ' '.join(commands_parts)


def svg2png(image_path, force=False):
    svg_files = [svg for svg in os.listdir(image_path) if svg.endswith('.svg')]

    if len(svg_files) == 0:
        print('\n'.join(sorted(os.listdir(image_path))))
        print('Nenhum arquivo .svg')
        return

    comm = command()
    for svg_file in svg_files:
        src = image_path + '/' + svg_file
        dest = image_path + '/' + svg_file.replace('.svg', '.png')

        if force is True or not os.path.isfile(dest):
            try:
                os.system(comm.format(src, dest))
                print(src + ' => ' + dest)
            except:
                print('Unable to run inkscape')


def png2tiff(image_path, force=False):
    png_files = [png for png in os.listdir(image_path) if png.endswith('.png')]

    if len(png_files) == 0:
        print('\n'.join(sorted(os.listdir(image_path))))
        print('Nenhum arquivo .png')
        return

    for png_file in png_files:
        src = image_path + '/' + png_file
        dest = image_path + '/' + png_file.replace('.png', '.tif')

        if force is True or not os.path.isfile(dest):
            try:
                Image.open(src).save(dest, "TIFF")
                print(src + ' => ' + dest)
            except IOError:
                print("cannot convert", src, dest)


def convert_svg2png(img_filename, destination=None, force=False):
    if os.path.isfile(img_filename) and img_filename.endswith('.svg'):
        if destination is None:
            destination = os.path.dirname(img_filename)
        if not os.path.isdir(destination):
            os.makedirs(destination)
        fname = os.path.basename(img_filename)
        dest_filename = destination + '/' + fname + '.png'
        if force or not os.path.isfile(dest_filename):
            try:
                comm = command()
                os.system(comm.format(img_filename, dest_filename))
                print(img_filename + ' => ' + dest_filename)
            except:
                print('Unable to run inkscape')


def convert_png2tiff(img_filename, destination=None, force=False):
    if os.path.isfile(img_filename) and img_filename.endswith('.png'):
        if destination is None:
            destination = os.path.dirname(img_filename)
        if not os.path.isdir(destination):
            os.makedirs(destination)
        fname = os.path.basename(img_filename)
        dest_filename = destination + '/' + fname + '.tif'
        if force or not (os.path.isfile(dest_filename) or os.path.isfile(dest_filename + 't')):
            try:
                Image.open(img_filename).save(dest_filename, "TIFF")
                print(img_filename + ' => ' + dest_filename)
            except IOError:
                print("cannot convert", img_filename, dest_filename)
