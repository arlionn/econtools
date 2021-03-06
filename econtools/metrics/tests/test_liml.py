from os import path

import pandas as pd

from econtools.metrics.util.testing import RegCompare

from econtools.metrics.core import ivreg
from econtools.metrics.tests.data.src_liml import (liml_std, liml_robust,
                                                   liml_cluster)
from econtools.metrics.tests.data.src_tsls import tsls_cluster


class LimlCompare(RegCompare):

    def __init__(self):
        super(LimlCompare, self).__init__()
        self.precision['coeff'] = 2
        self.precision['vce'] = 6
        self.precision['se'] = 1
        self.precision['CI_low'] = 1
        self.precision['CI_high'] = 1
        self.precision['F'] = 7
        self.precision['pF'] = 8
        self.precision['kappa'] = 10

    def test_r2(self):
        pass

    def test_r2_a(self):
        pass

    def test_mss(self):
        pass

    def test_ssr(self):
        # Stata SSR for IV is weird, skip
        pass

    def test_kappa(self):
        stat = 'kappa'
        self.stat_assert(stat)


class TestLIML_std(LimlCompare):

    def __init__(self):
        super(TestLIML_std, self).__init__()

    @classmethod
    def setup_class(cls):
        """Stata reg output from `sysuse auto; reg price mpg`"""
        test_path = path.split(path.relpath(__file__))[0]
        auto_path = path.join(test_path, 'data', 'auto.dta')
        autodata = pd.read_stata(auto_path)
        y = 'price'
        x_end = ['mpg', 'length']
        z = ['trunk', 'weight', 'headroom']
        x_exog = []
        nosingles = True
        cls.result = ivreg(autodata, y, x_end, z, x_exog,
                           addcons=True,
                           iv_method='liml',
                           nosingles=nosingles)
        cls.expected = liml_std


class TestLIML_robust(LimlCompare):

    def __init__(self):
        super(TestLIML_robust, self).__init__()
        self.precision['se'] = 0
        self.precision['CI_low'] = 0
        self.precision['CI_high'] = -1

    @classmethod
    def setup_class(cls):
        """Stata reg output from `sysuse auto; reg price mpg`"""
        test_path = path.split(path.relpath(__file__))[0]
        auto_path = path.join(test_path, 'data', 'auto.dta')
        autodata = pd.read_stata(auto_path)
        y = 'price'
        x_end = ['mpg', 'length']
        z = ['trunk', 'weight', 'headroom']
        x_exog = []
        nosingles = True
        cls.result = ivreg(autodata, y, x_end, z, x_exog,
                           addcons=True,
                           iv_method='liml',
                           vce_type='robust',
                           nosingles=nosingles)
        cls.expected = liml_robust


class TestLIML_cluster(LimlCompare):

    def __init__(self):
        super(TestLIML_cluster, self).__init__()
        self.precision['se'] = 0
        self.precision['CI_low'] = 0
        self.precision['CI_high'] = 0

    @classmethod
    def setup_class(cls):
        """Stata reg output from `sysuse auto; reg price mpg`"""
        test_path = path.split(path.relpath(__file__))[0]
        auto_path = path.join(test_path, 'data', 'auto.dta')
        autodata = pd.read_stata(auto_path)
        y = 'price'
        x_end = ['mpg', 'length']
        z = ['trunk', 'weight', 'headroom']
        x_exog = []
        nosingles = True
        cls.result = ivreg(autodata, y, x_end, z, x_exog,
                           addcons=True,
                           iv_method='liml',
                           cluster='gear_ratio',
                           nosingles=nosingles)
        cls.expected = liml_cluster


class TestLIML_tsls(LimlCompare):

    def __init__(self):
        super(TestLIML_tsls, self).__init__()
        # self.precision['se'] = 0
        # self.precision['CI_low'] = 0
        # self.precision['CI_high'] = 0

    def test_kappa(self):
        pass

    @classmethod
    def setup_class(cls):
        """Stata reg output from `sysuse auto; reg price mpg`"""
        test_path = path.split(path.relpath(__file__))[0]
        auto_path = path.join(test_path, 'data', 'auto.dta')
        autodata = pd.read_stata(auto_path)
        y = 'price'
        x_end = ['mpg', 'length']
        z = ['weight', 'trunk']
        x_exog = []
        nosingles = True
        cls.result = ivreg(autodata, y, x_end, z, x_exog, addcons=True,
                           iv_method='liml',
                           cluster='gear_ratio',
                           nosingles=nosingles)
        cls.expected = tsls_cluster


if __name__ == '__main__':
    import sys
    from nose import runmodule
    argv = [__file__, '-vs'] + sys.argv[1:]
    runmodule(argv=argv, exit=False)
