# Copyright 2004 Toby Dickenson
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys, getopt, colorsys, imp, md5

class pydepgraphdot:

    def main(self,argv):
        opts,args = getopt.getopt(argv,'',['mono'])
        self.colored = 1
        for o,v in opts:
            if o=='--mono':
                self.colored = 0
        self.render()

    def fix(self,s):
        # Convert a module name to a syntactically correct node name
        return s.replace('.','_')

    def render(self):
        p,t = self.get_data()

        # normalise our input data
        for k,d in p.items():
            for v in d.keys():
                if not p.has_key(v):
                    p[v] = {}

        f = self.get_output_file()

        f.write('digraph G {\n')
        #f.write('concentrate = true;\n')
        #f.write('ordering = out;\n')
        f.write('ranksep=1.0;\n')
        f.write('node [style=filled,fontname=Helvetica,fontsize=10];\n')
        allkd = p.items()
        allkd.sort()
        for k,d in allkd:
            tk = t.get(k)
            if self.use(k,tk):
                allv = d.keys()
                allv.sort()
                for v in allv:
                    tv = t.get(v)
                    if self.use(v,tv) and not self.toocommon(v,tv):
                        f.write('%s -> %s' % ( self.fix(k),self.fix(v) ) )
                        self.write_attributes(f,self.edge_attributes(k,v))
                        f.write(';\n')
                f.write(self.fix(k))
                self.write_attributes(f,self.node_attributes(k,tk))
                f.write(';\n')
        f.write('}\n')

    def write_attributes(self,f,a):
        if a:
            f.write(' [')
            f.write(','.join(a))
            f.write(']')

    def node_attributes(self,k,type):
        a = []
        a.append('label="%s"' % self.label(k))
        if self.colored:
            a.append('fillcolor="%s"' % self.color(k,type))
        else:
            a.append('fillcolor=white')
        if self.toocommon(k,type):
            a.append('peripheries=2')
        return a

    def edge_attributes(self,k,v):
        a = []
        weight = self.weight(k,v)
        if weight!=1:
            a.append('weight=%d' % weight)
        length = self.alien(k,v)
        if length:
            a.append('minlen=%d' % length)
        return a

    def get_data(self):
        t = eval(sys.stdin.read())
        return t['depgraph'],t['types']

    def get_output_file(self):
        return sys.stdout

    def use(self,s,type):
        # Return true if this module is interesting and should be drawn. Return false
        # if it should be completely omitted. This is a default policy - please override.
        if s in ('os','sys','qt','time','__future__','types','re','string'):
            # nearly all modules use all of these... more or less. They add nothing to
            # our diagram.
            return 0
        if s.startswith('encodings.'):
            return 0
        if s=='__main__':
            return 1
        if self.toocommon(s,type):
            # A module where we dont want to draw references _to_. Dot doesnt handle these
            # well, so it is probably best to not draw them at all.
            return 0
        return 1

    def toocommon(self,s,type):
        # Return true if references to this module are uninteresting. Such references
        # do not get drawn. This is a default policy - please override.
        #
        if s=='__main__':
            # references *to* __main__ are never interesting. omitting them means
            # that main floats to the top of the page
            return 1
        if type==imp.PKG_DIRECTORY:
            # dont draw references to packages.
            return 1
        return 0

    def weight(self,a,b):
        # Return the weight of the dependency from a to b. Higher weights
        # usually have shorter straighter edges. Return 1 if it has normal weight.
        # A value of 4 is usually good for ensuring that a related pair of modules
        # are drawn next to each other. This is a default policy - please override.
        #
        if b.split('.')[-1].startswith('_'):
            # A module that starts with an underscore. You need a special reason to
            # import these (for example random imports _random), so draw them close
            # together
            return 4
        return 1

    def alien(self,a,b):
        # Return non-zero if references to this module are strange, and should be drawn
        # extra-long. the value defines the length, in rank. This is also good for putting some
        # vertical space between seperate subsystems. This is a default policy - please override.
        #
        return 0

    def label(self,s):
        # Convert a module name to a formatted node label. This is a default policy - please override.
        #
        return '\\.\\n'.join(s.split('.'))

    def color(self,s,type):
        # Return the node color for this module name. This is a default policy - please override.
        #
        # Calculate a color systematically based on the hash of the module name. Modules in the
        # same package have the same color. Unpackaged modules are grey
        t = self.normalise_module_name_for_hash_coloring(s,type)
        return self.color_from_name(t)

    def normalise_module_name_for_hash_coloring(self,s,type):
        if type==imp.PKG_DIRECTORY:
            return s
        else:
            i = s.rfind('.')
            if i<0:
                return ''
            else:
                return s[:i]

    def color_from_name(self,name):
        n = md5.md5(name).digest()
        hf = float(ord(n[0])+ord(n[1])*0xff)/0xffff
        sf = float(ord(n[2]))/0xff
        vf = float(ord(n[3]))/0xff
        r,g,b = colorsys.hsv_to_rgb(hf, 0.3+0.6*sf, 0.8+0.2*vf)
        return '#%02x%02x%02x' % (r*256,g*256,b*256)


def main():
    F = {'depgraph': {'ConfigParser': {'re': 1},
              'QtUiSupport': {'ConfigParser': 1,
                              'PyQt4': 1,
                              'base64': 1,
                              'functools': 1,
                              'os': 1,
                              'overRidden': 1,
                              'pickle': 1,
                              'sys': 1,
                              'time': 1},
              'StringIO': {'errno': 1, 'sys': 1},
              'UserDict': {'copy': 1},
              '__main__': {'PyQt4': 1,
                           'PyQt4.QtCore': 1,
                           'PyQt4.QtGui': 1,
                           'QtUiSupport': 1,
                           '__future__': 1,
                           'extMap': 1,
                           'filecmp': 1,
                           'operator': 1,
                           'os': 1,
                           'overRidden': 1,
                           'pickle': 1,
                           'shutil': 1,
                           'sip': 1,
                           'socket': 1,
                           'subprocess': 1,
                           'sys': 1,
                           'time': 1,
                           'webbrowser': 1,
                           'xtools': 1},
              '_threading_local': {'threading': 1},
              'base64': {'binascii': 1,
                         'getopt': 1,
                         're': 1,
                         'struct': 1,
                         'sys': 1},
              'bdb': {'__main__': 1,
                      'linecache': 1,
                      'os': 1,
                      'repr': 1,
                      'sys': 1,
                      'types': 1},
              'bisect': {'_bisect': 1},
              'cmd': {'string': 1, 'sys': 1},
              'copy': {'copy_reg': 1, 'repr': 1, 'sys': 1, 'types': 1},
              'copy_reg': {'types': 1},
              'csv': {'StringIO': 1, '_csv': 1, 'cStringIO': 1, 're': 1},
              'difflib': {'difflib': 1, 'doctest': 1, 'heapq': 1, 're': 1},
              'dis': {'opcode': 1, 'sys': 1, 'types': 1},
              'doctest': {'StringIO': 1,
                          '__future__': 1,
                          'difflib': 1,
                          'inspect': 1,
                          'linecache': 1,
                          'new': 1,
                          'os': 1,
                          'pdb': 1,
                          're': 1,
                          'sys': 1,
                          'tempfile': 1,
                          'traceback': 1,
                          'unittest': 1,
                          'warnings': 1},
              'dummy_thread': {'traceback': 1, 'warnings': 1},
              'extMap': {'iniConfigReadWrite': 1, 'os': 1, 'sys': 1},
              'filecmp': {'getopt': 1,
                          'itertools': 1,
                          'os': 1,
                          'stat': 1,
                          'sys': 1,
                          'warnings': 1},
              'fnmatch': {'os': 1, 'posixpath': 1, 're': 1},
              'functools': {'_functools': 1},
              'getopt': {'os': 1, 'sys': 1},
              'getpass': {'msvcrt': 1, 'os': 1, 'sys': 1},
              'glob': {'fnmatch': 1, 'os': 1, 're': 1},
              'heapq': {'_heapq': 1,
                        'bisect': 1,
                        'itertools': 1,
                        'operator': 1},
              'iniConfigReadWrite': {'ConfigParser': 1, 'base64': 1, 'os': 1},
              'inspect': {'dis': 1,
                          'imp': 1,
                          'linecache': 1,
                          'operator': 1,
                          'os': 1,
                          're': 1,
                          'string': 1,
                          'sys': 1,
                          'tokenize': 1,
                          'types': 1},
              'linecache': {'os': 1, 'sys': 1},
              'macpath': {'os': 1, 'stat': 1},
              'new': {'types': 1},
              'ntpath': {'nt': 1, 'os': 1, 'stat': 1, 'string': 1, 'sys': 1},
              'os': {'UserDict': 1,
                     'copy_reg': 1,
                     'errno': 1,
                     'macpath': 1,
                     'nt': 1,
                     'ntpath': 1,
                     'os': 1,
                     'os2emxpath': 1,
                     'popen2': 1,
                     'posixpath': 1,
                     'sys': 1},
              'os2emxpath': {'os': 1, 'stat': 1, 'string': 1},
              'overRidden': {'PyQt4': 1},
              'pdb': {'bdb': 1,
                      'cmd': 1,
                      'linecache': 1,
                      'os': 1,
                      'pprint': 1,
                      're': 1,
                      'repr': 1,
                      'sys': 1,
                      'traceback': 1},
              'pickle': {'StringIO': 1,
                         'binascii': 1,
                         'cStringIO': 1,
                         'copy_reg': 1,
                         'doctest': 1,
                         'marshal': 1,
                         're': 1,
                         'struct': 1,
                         'sys': 1,
                         'types': 1},
              'popen2': {'os': 1, 'sys': 1},
              'posixpath': {'os': 1, 're': 1, 'stat': 1},
              'pprint': {'cStringIO': 1, 'sys': 1, 'time': 1},
              'random': {'_random': 1,
                         'binascii': 1,
                         'math': 1,
                         'os': 1,
                         'time': 1,
                         'types': 1,
                         'warnings': 1},
              're': {'copy_reg': 1,
                     'sre_compile': 1,
                     'sre_constants': 1,
                     'sre_parse': 1,
                     'sys': 1},
              'repr': {'__builtin__': 1, 'itertools': 1},
              'shlex': {'StringIO': 1,
                        'cStringIO': 1,
                        'collections': 1,
                        'sys': 1},
              'shutil': {'os': 1, 'stat': 1, 'sys': 1},
              'socket': {'_socket': 1,
                         '_ssl': 1,
                         'errno': 1,
                         'os': 1,
                         'sys': 1},
              'sre_compile': {'_sre': 1,
                              'array': 1,
                              'sre_constants': 1,
                              'sre_parse': 1,
                              'sys': 1},
              'sre_parse': {'sre_constants': 1, 'sys': 1},
              'string': {'re': 1, 'strop': 1},
              'struct': {'_struct': 1},
              'subprocess': {'_subprocess': 1,
                             'errno': 1,
                             'msvcrt': 1,
                             'os': 1,
                             'pickle': 1,
                             'select': 1,
                             'sys': 1,
                             'threading': 1,
                             'traceback': 1,
                             'types': 1},
              'tempfile': {'dummy_thread': 1,
                           'errno': 1,
                           'os': 1,
                           'random': 1,
                           'thread': 1},
              'threading': {'_threading_local': 1,
                            'collections': 1,
                            'random': 1,
                            'sys': 1,
                            'thread': 1,
                            'time': 1,
                            'traceback': 1},
              'token': {'re': 1, 'sys': 1},
              'tokenize': {'re': 1, 'string': 1, 'sys': 1, 'token': 1},
              'traceback': {'linecache': 1, 'sys': 1, 'types': 1},
              'types': {'_types': 1, 'sys': 1},
              'unittest': {'__builtin__': 1,
                           'getopt': 1,
                           'os': 1,
                           'sys': 1,
                           'time': 1,
                           'traceback': 1,
                           'types': 1},
              'warnings': {'linecache': 1, 're': 1, 'sys': 1, 'types': 1},
              'webbrowser': {'copy': 1,
                             'getopt': 1,
                             'glob': 1,
                             'os': 1,
                             'shlex': 1,
                             'socket': 1,
                             'stat': 1,
                             'subprocess': 1,
                             'sys': 1,
                             'tempfile': 1,
                             'time': 1},
              'xtools': {'ConfigParser': 1,
                         'PyQt4': 1,
                         'PyQt4.QtCore': 1,
                         'PyQt4.QtGui': 1,
                         'QtUiSupport': 1,
                         'csv': 1,
                         'datetime': 1,
                         'functools': 1,
                         'getpass': 1,
                         'os': 1,
                         'pickle': 1,
                         'popen2': 1,
                         're': 1,
                         'subprocess': 1,
                         'sys': 1,
                         'time': 1}},
 'types': {'ConfigParser': 1,
           'PyQt4': 5,
           'PyQt4.QtCore': 3,
           'PyQt4.QtGui': 3,
           'QtUiSupport': 1,
           'StringIO': 1,
           'UserDict': 1,
           '__builtin__': 6,
           '__future__': 1,
           '__main__': 1,
           '_bisect': 6,
           '_csv': 6,
           '_functools': 6,
           '_heapq': 6,
           '_random': 6,
           '_socket': 3,
           '_sre': 6,
           '_ssl': 3,
           '_struct': 6,
           '_subprocess': 6,
           '_threading_local': 1,
           '_types': 6,
           'array': 6,
           'base64': 1,
           'bdb': 1,
           'binascii': 6,
           'bisect': 1,
           'cStringIO': 6,
           'cmd': 1,
           'collections': 6,
           'copy': 1,
           'copy_reg': 1,
           'csv': 1,
           'datetime': 6,
           'difflib': 1,
           'dis': 1,
           'doctest': 1,
           'dummy_thread': 1,
           'errno': 6,
           'extMap': 1,
           'filecmp': 1,
           'fnmatch': 1,
           'functools': 1,
           'getopt': 1,
           'getpass': 1,
           'glob': 1,
           'heapq': 1,
           'imp': 6,
           'iniConfigReadWrite': 1,
           'inspect': 1,
           'itertools': 6,
           'linecache': 1,
           'macpath': 1,
           'marshal': 6,
           'math': 6,
           'msvcrt': 6,
           'new': 1,
           'nt': 6,
           'ntpath': 1,
           'opcode': 1,
           'operator': 6,
           'os': 1,
           'os2emxpath': 1,
           'overRidden': 1,
           'pdb': 1,
           'pickle': 1,
           'popen2': 1,
           'posixpath': 1,
           'pprint': 1,
           'random': 1,
           're': 1,
           'repr': 1,
           'select': 3,
           'shlex': 1,
           'shutil': 1,
           'sip': 3,
           'socket': 1,
           'sre_compile': 1,
           'sre_constants': 1,
           'sre_parse': 1,
           'stat': 1,
           'string': 1,
           'strop': 6,
           'struct': 1,
           'subprocess': 1,
           'sys': 6,
           'tempfile': 1,
           'thread': 6,
           'threading': 1,
           'time': 6,
           'token': 1,
           'tokenize': 1,
           'traceback': 1,
           'types': 1,
           'unittest': 1,
           'warnings': 1,
           'webbrowser': 1,
           'xtools': 1}}
    pydepgraphdot().main(str(F))

if __name__=='__main__':
    main()



