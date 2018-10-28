from lxml import etree
import ntpath


def generateAnnotationFile(fName, h, w, c, xMin, yMin, xMax, yMax):
    root = etree.Element('annotation')
    folder = etree.Element('folder')
    folder.text = 'Annotations'
    root.append(folder)
    fileName = etree.Element('fileName')
    fileName.text = ntpath.basename(fName)
    root.append(fileName)
    path = etree.Element('path')
    path.text = '../JPEGImages/{}'.format(ntpath.basename(fName))
    root.append(path)
    source = etree.Element('source')
    database = etree.Element('database')
    database.text = 'Unknown'
    source.append(database)
    root.append(source)
    size = etree.Element('size')
    width = etree.Element('width')
    width.text = str(w)
    size.append(width)
    height = etree.Element('height')
    height.text = str(h)
    size.append(height)
    depth = etree.Element('depth')
    depth.text = str(c)
    size.append(depth)
    root.append(size)
    segmented = etree.Element('segmented')
    segmented.text = str(0)
    root.append(segmented)
    object = etree.Element('object')
    name = etree.Element('name')
    name.text = 'ref_box'
    object.append(name)

    pose = etree.Element('pose')
    pose.text = 'Unspecified'
    object.append(pose)

    truncated = etree.Element('truncated')
    truncated.text = str(0)
    object.append(truncated)

    difficult = etree.Element('difficult')
    difficult.text = str(0)
    object.append(difficult)

    bndbox = etree.Element('bndbox')
    xmin = etree.Element('xmin')
    xmin.text = str(xMin)
    ymin = etree.Element('ymin')
    ymin.text = str(yMin)
    xmax = etree.Element('xmax')
    xmax.text = str(xMax)
    ymax = etree.Element('ymax')
    ymax.text = str(yMax)

    bndbox.append(xmin)
    bndbox.append(ymin)
    bndbox.append(xmax)
    bndbox.append(ymax)
    object.append(bndbox)
    root.append(object)

    s = etree.tostring(root, pretty_print=True)
    with open('./VOC2018/Annotations/{}xml'.format(ntpath.basename(fName)[:-3]), 'w') as f:
        f.write(s.decode(encoding="utf-8"))

    return