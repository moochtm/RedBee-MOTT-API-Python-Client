from jinja2 import Template, Environment, Undefined
from lxml import etree
from slugify import slugify

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
NAMESPACE = '{http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1}'


class SilentUndefined(Undefined):
    '''
    Don't break pageloads because vars arent there!
    '''
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''


def create(data, template_file):
    template_text = template_file.read()
    env = Environment()
    env.undefined = SilentUndefined
    env.filters['slugify'] = slugify_text
    env.filters['remove_url_params'] = remove_url_params

    j2t = env.from_string(template_text)
    render = j2t.render(data=data)

    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    root = etree.fromstring(bytes(render, encoding='utf8'), parser=parser)

    # strip whitespace from text and tail
    for elem in root.iter('*'):
        if elem.text is not None:
            elem.text = elem.text.strip()
        if elem.tail is not None:
            elem.tail = elem.tail.strip()
        if elem.text is not None and not elem.text.strip():
            elem.text = None
        # remove attribute if empty
        for key in elem.keys():
            if not elem.get(key):
                elem.attrib.pop(key)

    # remove empty nodes
    while len(root.xpath(".//*[not(node())]")) > 0:
        for element in root.xpath(".//*[not(node())]"):
            element.getparent().remove(element)

    return etree.tostring(root, pretty_print=True).decode()


def slugify_text(text):
    return slugify(text)


def remove_url_params(url):
    return url[:url.find('?')]