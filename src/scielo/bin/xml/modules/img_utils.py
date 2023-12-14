# coding=utf-8

import os
from . import utils
from . import validation_status

try:
    from PIL import Image
    IMG_CONVERTER = True
except Exception as e:
    IMG_CONVERTER = False

from . import svg_conversion

IMDEBUGGING = False


def is_tiff(img_filename):
    return os.path.splitext(img_filename)[1] in ['.tiff', '.tif']


def tiff_image(img_filename):
    if is_tiff(img_filename):
        if os.path.isfile(img_filename):
            try:
                return Image.open(img_filename)
            except:
                return None


def hdimg_to_jpg(source_image_filename, jpg_filename):
    if IMG_CONVERTER:
        try:
            im = Image.open(source_image_filename)
            im.thumbnail(im.size)
            im.save(jpg_filename, "JPEG")
        except Exception as inst:
            utils.display_message('Unable to generate ' + jpg_filename)
            utils.display_message(inst)


def hdimages_to_jpeg(source_path, jpg_path, force_update=False):
    if IMG_CONVERTER:
        for item in os.listdir(source_path):
            image_filename = source_path + '/' + item
            if item.endswith('.tiff') or item.endswith('.eps') or item.endswith('.tif'):
                jpg_filename = source_path + '/' + item[0:item.rfind('.')] + '.jpg'
                doit = True if not os.path.isfile(jpg_filename) else force_update is True

                if doit:
                    hdimg_to_jpg(image_filename, jpg_filename)


def svg2png(images_path):
    svg_conversion.svg2png(images_path)


def png2tiff(images_path):
    svg_conversion.png2tiff(images_path)


def validate_tiff_image_file(img_filename, dpi=300):
    img = tiff_image(img_filename)
    if img is not None:
        if img.info is not None:
            if img.info.get('dpi') < dpi:
                return _('{file} has invalid dpi: {dpi}').format(file=os.path.basename(img_filename), dpi=img.info.get('dpi'))


def evaluate_tiff(img_filename, min_height=None, max_height=None):
    status_message = []
    tiff_im = utils.tiff_image(img_filename)
    if tiff_im is not None:
        errors = []
        dpi = None if tiff_im.info is None else tiff_im.info.get('dpi', [_('unknown')])[0]

        info = []
        info.append(u'{dpi} dpi'.format(dpi=dpi))
        info.append(_('height: {height} pixels. ').format(height=tiff_im.size[1]))
        info.append(_('width: {width} pixels. ').format(width=tiff_im.size[0]))

        status = None
        if min_height is not None:
            if tiff_im.size[1] < min_height:
                status = validation_status.STATUS_WARNING
        if max_height is not None:
            if tiff_im.size[1] > max_height:
                status = validation_status.STATUS_WARNING
        if status is not None:
            errors.append(_('Be sure that {img} has valid height. Recommended: min={min} and max={max}. The images must be proportional among themselves. ').format(img=os.path.basename(img_filename), min=min_height, max=max_height))
        if dpi is not None:
            if dpi < MIN_IMG_DPI:
                errors.append(_('Expected values: {expected}. ').format(expected=_('equal or greater than {value} dpi').format(value=MIN_IMG_DPI)))
                status = validation_status.STATUS_ERROR
        if len(errors) > 0:
            status_message.append((status, '; '.join(info) + ' | ' + '. '.join(errors)))
        else:
            status_message.append((validation_status.STATUS_INFO, '; '.join(info)))

    return status_message
