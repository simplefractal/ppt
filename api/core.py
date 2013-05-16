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
        """
        '/some/path' -> {
            '1826322': (0, <lxml.etree._ElementTree object at 0x10884fd40>),
            '9126312': (1, <lxml.etree._ElementTree object at 0x10884fd40>)
        }
        """

        doc = openxmllib.openXmlDocument(file_path)

        ct_file = os.path.join(doc._cache_dir, '[Content_Types].xml')
        raw_xml = xmlFile(ct_file, 'rb')
        doc.content_types = contenttypes.ContentTypes(raw_xml)

        slide_dict = {}

        for index, tree in enumerate(doc.content_types.getTreesFor(doc, contenttypes.CT_PRESENTATION_SLIDE)):
            slide_id = tree.xpath('//p14:creationId/@val', namespaces={'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'})[0]
            slide_dict[slide_id] = (index, tree)

        return slide_dict

    def get_slide_changes(self, old_slides, new_slides):
        """
        -> {
            'modified': set([id1, id2]),
            'deleted': set([id3]),
            'created': set([id4, id5])
        }
        """

        change_dict = {}

        old_ids = set(old_slides.keys())
        new_ids = set(new_slides.keys())

        change_dict['deleted'] = old_ids.difference(new_ids)
        change_dict['created'] = new_ids.difference(old_ids)

        # Get modified slide ids
        candidates = old_ids.intersection(new_ids)
        modified = []
        for _id in candidates:
            _, old_xml = old_slides.get(_id)
            _, new_xml = new_slides.get(_id)

            # Compare string representation of xml tree
            if not etree.tostring(old_xml) == etree.tostring(new_xml):
                modified.append(_id)

        change_dict['modified'] = set(modified)

        return change_dict

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
        new_slides = self.get_slides(self.head)
        print "Old slides"
        print old_slides

        print "New slides"
        print new_slides

        slide_changes = self.get_slide_changes(old_slides, new_slides)
        print slide_changes
        # return [(transform_to_image(x), transform_to_image(y))
        #         for x, y in changed_slides]
