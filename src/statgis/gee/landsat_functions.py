"""
Function to process Landsat SR Images.
"""
import ee


def scaler(image: ee.Image) -> ee.Image:
    """
    Scale optical bands to surface reflectance values and thermal bands to Kelvin.

    Parameters
    ----------
    image : ee.Image
        Landsat SR image.

    Returns
    -------
    image : ee.Image
        Image with bands scaled.
    """
    optical = image.select("SR_B.").multiply(0.0000275).add(-0.2)
    thermal = image.select("ST_B.*").multiply(0.00341802).add(149)

    image = image.addBands(optical, None, True).addBands(thermal, None, True)

    return image


def cloud_mask(image: ee.Image, all_classifications:bool = True) -> ee.Image:
    """
    Mask pixels classifed as clouds from QA_PIXEL band.

    Parameters
    ----------
    image : ee.Image
        Image to mask.

    all_classifications : bool (optional)
        If `True` mask all values not classified as clear pixel.
        If `False` mask only pixels classified as cloud.

    Returns
    -------
    image : ee.Image
        Masked image.
    """
    qa = image.select("QA_PIXEL")

    cirrus = qa.bitwiseAnd((1 << 2)).eq(0)
    cloud = qa.bitwiseAnd((1 << 3)).eq(0)
    shadow = qa.bitwiseAnd((1 << 4)).eq(0)
    snow = qa.bitwiseAnd((1 << 5)).eq(0)

    if all_classifications:
        image = (
            image.updateMask(cirrus)
                 .updateMask(cloud)
                 .updateMask(shadow)
                 .updateMask(snow)
        )
    else:
        image = image.updateMask(cloud)

    return image