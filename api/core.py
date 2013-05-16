import StringIO
import os
import openxmllib
from openxmllib import contenttypes

from openxmllib.utils import xmlFile
from openxmllib.namespaces import ns_map
from lxml import etree

from .util import transform_to_image


class XMLDiff(object):
    def __init__(self, prev, head):
        self.prev = prev
        self.head = head

    def get_slides(self, file_path):

        doc = openxmllib.openXmlDocument(file_path)

        ct_file = os.path.join(doc._cache_dir, '[Content_Types].xml')
        raw_xml = xmlFile(ct_file, 'rb')
        doc.content_types = contenttypes.ContentTypes(raw_xml)

        slide_dict = {}

        for index, tree in enumerate(doc.content_types.getTreesFor(doc, contenttypes.CT_PRESENTATION_SLIDE)):
            slide_id = tree.xpath('//p14:creationId/@val', namespaces={'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'})[0]
            slide_dict[slide_id] = index

        return slide_dict

    def get_diff(self):
        """
        Returns a list of tuples containing the filepaths for
        old and new version
        of the changed slides as images

        e.g,
        [
            ("/old_slide_1.jpg", "/new_slide_1.jpg"),
            ("/old_slide_3.jpg, "/new_slide_3.jpg"),
            ("/old_slide_4.jpg", None),
            (None, "/new_slide_7.jpg")
        ]
        where slides 1 and 2 are the only ones that have changed
        slide 4 has been deleted
        slide 7 has been created
        """
        old_slides = self.get_slides(self.prev)
        print old_slides
        # new_slides = self.get_slides(self.head)
        # changed_slides = self.get_changed_slides(old_slides, new_slides)
        # return [(transform_to_image(x), transform_to_image(y))
        #         for x, y in changed_slides]
