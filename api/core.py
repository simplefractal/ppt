from .util import transform_to_image


class XMLDiff(object):
    def __init__(self, old_file, new_file):
        self.prev = old_file
        self.head = new_file

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
        old_slides = self.get_old_slides()
        new_slides = self.get_new_slides()
        changed_slides = self.get_changed_slides(old_slides, new_slides)
        return [(transform_to_image(x), transform_to_image(y))
                for x, y in changed_slides]
