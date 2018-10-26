import random
# -*- coding: utf-8 -*-
import sys, time, math, pygame, os
import numpy as np

avg = []
var = []
stdev = []

for x in range(100):
	random_rank = []
	for i in range(96):
		random_rank.append(random.randint(0,100))
	avg.append(np.mean(random_rank))
	var.append(np.var(random_rank))
	stdev.append(np.std(random_rank))

print(np.mean(avg))
print(np.mean(stdev))
print(np.mean(var))