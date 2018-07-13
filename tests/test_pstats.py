from unittest import TestCase

from package_statistics import parse_data, format_list

class ParseTest(TestCase):
    def test_top10(self):
        top10 = parse_data(b"""bin/bsd-csh                                                 shells/csh
bin/bunzip2                                                 utils/bzip2
bin/busybox                                                 utils/busybox,shells/busybox-static
bin/bzcat                                                   utils/bzip2
bin/bzcmp                                                   utils/bzip2
bin/bzdiff                                                  utils/bzip2""".splitlines(), 10)
        self.assertEqual(top10,
                         [('bzip2', 4), ('csh', 1), ('busybox', 1), ('busybox-static', 1)])


    def test_top3(self):
        top3 = parse_data(b"""bin/bsd-csh                                                 shells/csh
bin/bunzip2                                                 utils/bzip2
bin/busybox                                                 utils/busybox
bin/bzcat                                                   utils/bzip2
bin/bzcmp                                                   utils/bzip2
bin/bzdiff                                                  utils/bzip2""".splitlines(), 3)
        self.assertEqual(top3,
                         [('bzip2', 4), ('csh', 1), ('busybox', 1)])


    def test_filename_spaces(self):
        top10 = parse_data(b"""bin/bsd-csh                                                 shells/csh
bin/bunzip2                                                 utils/bzip2
bin/busybox                                                 utils/busybox,shells/busybox-static
bin/bzcat                                                   utils/bzip2
bin/bzcmp                                                   utils/bzip2
bin/bzcmp and a file with spaces.sh                         utils/bzip2
bin/bzdiff                                                  utils/bzip2""".splitlines(), 10)
        self.assertEqual(top10,
                         [('bzip2', 5), ('csh', 1), ('busybox', 1), ('busybox-static', 1)])

class PrintTest(TestCase):
    def test_top3(self):
        op = format_list([('bzip2', 4), ('csh', 1), ('busybox', 1)])
        print(op)
        self.assertEqual(op,
                         '''  1. bzip2                             4
  2. csh                               1
  3. busybox                           1''')
