#!/usr/bin/env python3
#
import unittest
import os
import femagtools.mcv
import logging
import logging.config


class McvWriterTest(unittest.TestCase):
    def test_read_mcv(self):
        testPath = os.path.split(__file__)[0]
        if not testPath:
            testPath = '.'
        filename = "data/TKS_NO_20.MCV"
        filename_out = "data/TKS_NO_20_out.MCV"
        reader = femagtools.mcv.Reader()
        reader.readMcv('{0}/{1}'.format(testPath, filename))
        r = reader.get_results()
        self.assertEqual(r['desc'],
                         u'PowerCore\xae NO 20 ;ThyssenKrupp Steel Eur')
        self.assertEqual(len(r['curve'][0]['bi']), 24)
        self.assertEqual(r['curve'][0]['bi'][0], 0.0)
        self.assertAlmostEqual(r['curve'][0]['bi'][-1], 1.836, 3)

        # test mcv writer
        writer = femagtools.mcv.Writer(r)
        # writer.setData(r)
        writeMcvFile = '{0}/{1}'.format(testPath, filename_out)
        writer.writeMcv(writeMcvFile)
        self.assertNotEqual(writer, None)

        # TEST
        reader2 = femagtools.mcv.Reader()
        reader2.readMcv(writeMcvFile)
        
        for attr in ['version_mc_curve', 'mc1_curves', 'mc1_title']:
            self.assertAlmostEqual(getattr(reader, attr),
                                   getattr(reader2, attr))
        for attr in ['mc1_remz', 'mc1_bsat', 'mc1_bref', 'mc1_fillfac',
                     'fo', 'Bo', 'ch', 'ch_freq', 'cw',
                     'cw_freq', 'b_coeff', 'rho', 'fe_sat_mag']:
            self.assertAlmostEqual(getattr(reader, attr),
                                   getattr(reader2, attr), 3)
        for attr in ['hi', 'bi']:
            self.assertAlmostEqual(reader.curve[0][attr],
                                   reader2.curve[0][attr], 3)

if __name__ == '__main__':
    unittest.main()
