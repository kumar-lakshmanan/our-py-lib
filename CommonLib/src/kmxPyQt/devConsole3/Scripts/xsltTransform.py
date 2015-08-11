import os
print(os.getcwd())
if __name__ == '__main__':
    import lxml.etree as ET
    xml_filename = 'Scripts\sample.xml'
    xsl_filename = 'Scripts\sample.xsl'
    dom = ET.parse(xml_filename)
    xslt = ET.parse(xsl_filename)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    print(ET.tostring(newdom, pretty_print=True))    