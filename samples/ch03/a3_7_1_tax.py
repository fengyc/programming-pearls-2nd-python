# -*- coding: utf-8 -*-
#
# 计税
#
# 计税时，采用的是分级累进的计算方式，不同的收入对应不同的税率，而超过某个税率时，可直接使用
# 速算扣除数的方式
#
# 采用数组保存每级终点，速算数（前 n 级的累计）、本级税率、上一级终点

tax_rates = [
    (2200, 0, 0, 0),
    (2700, 0, 0.14, 2200),
    (3200, 70, 0.15, 2700),
    (3700, 145, 0.16, 3200),
    (4200, 225, 0.17, 3700),
    # 其它...
    (999999999, 310, 0.70, 4200)
]


def calc_tax(income):
    for i in range(len(tax_rates)):
        if income > tax_rates[i][0]:
            continue
        return tax_rates[i][1] + tax_rates[i][2] * (income - tax_rates[i][3])


def test_calc_tax():
    assert calc_tax(2200) == 0
    assert calc_tax(2700) == 70
    assert calc_tax(4200) == 310
