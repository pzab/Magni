"""
..
    Copyright (c) 2016-2017, Magni developers.
    All rights reserved.
    See LICENSE.rst for further information.

Module providing utilities for the Approximate Message Passing (AMP) algorithm.

Routine listings
----------------
theta_mm(theta)
    Return the minimax optimal value of the AMP theta tunable parameter.

"""

import bisect


def theta_mm(delta):
    """
    Return the minimax optimal value of the AMP theta tunable parameter.

    A simple lookup table is used to determine the minimax optimal value of the
    AMP theta tunable parameter as specified in [1]_. Specifically, the formula
    in the top left column on page 6 is used without the 1/sqrt(delta) factor
    (as specfified in the SI Appendix) and with kappa=2.

    Parameters
    ----------
    delta : float
        The undersampling ratio.

    Returns
    -------
    theta_mm : float
        The minimax optimal value of the theta parameter.

    References
    ----------
    .. [1] D. L. Donoho, A. Maleki, and A. Montanari, "Message-passing
        algorithms for compressed sensing", *Proceedings of the National
        Academy of Sciences of the United States of America*, vol. 106, no. 45,
        p. 18914-18919, Nov. 2009.

    Examples
    --------
    For example, get the optimal parameters for a few undersampling ratios

    >>> from magni.cs.reconstruction.amp.util import theta_mm
    >>> theta_mm(0.1)
    1.736
    >>> theta_mm(0.2121)
    1.378
    >>> theta_mm(0.001)
    3.312
    >>> theta_mm(0.999)
    0.032
    >>> theta_mm(0.0001)
    3.312
    >>> theta_mm(0.99999)
    0.032

    """

    theta_mm = {0.001: 3.312, 0.002: 3.115, 0.003: 2.995, 0.004: 2.908,
                0.005: 2.839, 0.006: 2.781, 0.007: 2.731, 0.008: 2.688,
                0.009: 2.649, 0.010: 2.614, 0.011: 2.582, 0.012: 2.553,
                0.013: 2.526, 0.014: 2.500, 0.015: 2.476, 0.016: 2.454,
                0.017: 2.432, 0.018: 2.412, 0.019: 2.393, 0.020: 2.374,
                0.021: 2.357, 0.022: 2.340, 0.023: 2.324, 0.024: 2.308,
                0.025: 2.293, 0.026: 2.279, 0.027: 2.265, 0.028: 2.251,
                0.029: 2.238, 0.030: 2.226, 0.031: 2.213, 0.032: 2.201,
                0.033: 2.190, 0.034: 2.178, 0.035: 2.167, 0.036: 2.156,
                0.037: 2.146, 0.038: 2.136, 0.039: 2.125, 0.040: 2.116,
                0.041: 2.106, 0.042: 2.097, 0.043: 2.087, 0.044: 2.078,
                0.045: 2.069, 0.046: 2.061, 0.047: 2.052, 0.048: 2.044,
                0.049: 2.036, 0.050: 2.028, 0.051: 2.020, 0.052: 2.012,
                0.053: 2.004, 0.054: 1.997, 0.055: 1.989, 0.056: 1.982,
                0.057: 1.975, 0.058: 1.967, 0.059: 1.960, 0.060: 1.954,
                0.061: 1.947, 0.062: 1.940, 0.063: 1.933, 0.064: 1.927,
                0.065: 1.920, 0.066: 1.914, 0.067: 1.908, 0.068: 1.902,
                0.069: 1.896, 0.070: 1.890, 0.071: 1.884, 0.072: 1.878,
                0.073: 1.872, 0.074: 1.866, 0.075: 1.860, 0.076: 1.855,
                0.077: 1.849, 0.078: 1.844, 0.079: 1.838, 0.080: 1.833,
                0.081: 1.828, 0.082: 1.822, 0.083: 1.817, 0.084: 1.812,
                0.085: 1.807, 0.086: 1.802, 0.087: 1.797, 0.088: 1.792,
                0.089: 1.787, 0.090: 1.782, 0.091: 1.777, 0.092: 1.772,
                0.093: 1.768, 0.094: 1.763, 0.095: 1.758, 0.096: 1.754,
                0.097: 1.749, 0.098: 1.745, 0.099: 1.740, 0.100: 1.736,
                0.101: 1.731, 0.102: 1.727, 0.103: 1.723, 0.104: 1.718,
                0.105: 1.714, 0.106: 1.710, 0.107: 1.705, 0.108: 1.701,
                0.109: 1.697, 0.110: 1.693, 0.111: 1.689, 0.112: 1.685,
                0.113: 1.681, 0.114: 1.677, 0.115: 1.673, 0.116: 1.669,
                0.117: 1.665, 0.118: 1.661, 0.119: 1.657, 0.120: 1.654,
                0.121: 1.650, 0.122: 1.646, 0.123: 1.642, 0.124: 1.638,
                0.125: 1.635, 0.126: 1.631, 0.127: 1.627, 0.128: 1.624,
                0.129: 1.620, 0.130: 1.617, 0.131: 1.613, 0.132: 1.610,
                0.133: 1.606, 0.134: 1.603, 0.135: 1.599, 0.136: 1.596,
                0.137: 1.592, 0.138: 1.589, 0.139: 1.585, 0.140: 1.582,
                0.141: 1.579, 0.142: 1.575, 0.143: 1.572, 0.144: 1.569,
                0.145: 1.565, 0.146: 1.562, 0.147: 1.559, 0.148: 1.556,
                0.149: 1.553, 0.150: 1.549, 0.151: 1.546, 0.152: 1.543,
                0.153: 1.540, 0.154: 1.537, 0.155: 1.534, 0.156: 1.531,
                0.157: 1.528, 0.158: 1.524, 0.159: 1.521, 0.160: 1.518,
                0.161: 1.515, 0.162: 1.512, 0.163: 1.509, 0.164: 1.506,
                0.165: 1.504, 0.166: 1.501, 0.167: 1.498, 0.168: 1.495,
                0.169: 1.492, 0.170: 1.489, 0.171: 1.486, 0.172: 1.483,
                0.173: 1.480, 0.174: 1.478, 0.175: 1.475, 0.176: 1.472,
                0.177: 1.469, 0.178: 1.466, 0.179: 1.464, 0.180: 1.461,
                0.181: 1.458, 0.182: 1.455, 0.183: 1.453, 0.184: 1.450,
                0.185: 1.447, 0.186: 1.445, 0.187: 1.442, 0.188: 1.439,
                0.189: 1.437, 0.190: 1.434, 0.191: 1.431, 0.192: 1.429,
                0.193: 1.426, 0.194: 1.424, 0.195: 1.421, 0.196: 1.418,
                0.197: 1.416, 0.198: 1.413, 0.199: 1.411, 0.200: 1.408,
                0.201: 1.406, 0.202: 1.403, 0.203: 1.401, 0.204: 1.398,
                0.205: 1.396, 0.206: 1.393, 0.207: 1.391, 0.208: 1.388,
                0.209: 1.386, 0.210: 1.383, 0.211: 1.381, 0.212: 1.378,
                0.213: 1.376, 0.214: 1.374, 0.215: 1.371, 0.216: 1.369,
                0.217: 1.367, 0.218: 1.364, 0.219: 1.362, 0.220: 1.359,
                0.221: 1.357, 0.222: 1.355, 0.223: 1.352, 0.224: 1.350,
                0.225: 1.348, 0.226: 1.345, 0.227: 1.343, 0.228: 1.341,
                0.229: 1.339, 0.230: 1.336, 0.231: 1.334, 0.232: 1.332,
                0.233: 1.330, 0.234: 1.327, 0.235: 1.325, 0.236: 1.323,
                0.237: 1.321, 0.238: 1.318, 0.239: 1.316, 0.240: 1.314,
                0.241: 1.312, 0.242: 1.310, 0.243: 1.307, 0.244: 1.305,
                0.245: 1.303, 0.246: 1.301, 0.247: 1.299, 0.248: 1.297,
                0.249: 1.294, 0.250: 1.292, 0.251: 1.290, 0.252: 1.288,
                0.253: 1.286, 0.254: 1.284, 0.255: 1.282, 0.256: 1.280,
                0.257: 1.277, 0.258: 1.275, 0.259: 1.273, 0.260: 1.271,
                0.261: 1.269, 0.262: 1.267, 0.263: 1.265, 0.264: 1.263,
                0.265: 1.261, 0.266: 1.259, 0.267: 1.257, 0.268: 1.255,
                0.269: 1.253, 0.270: 1.251, 0.271: 1.249, 0.272: 1.247,
                0.273: 1.245, 0.274: 1.243, 0.275: 1.241, 0.276: 1.239,
                0.277: 1.237, 0.278: 1.235, 0.279: 1.233, 0.280: 1.231,
                0.281: 1.229, 0.282: 1.227, 0.283: 1.225, 0.284: 1.223,
                0.285: 1.221, 0.286: 1.219, 0.287: 1.217, 0.288: 1.215,
                0.289: 1.213, 0.290: 1.211, 0.291: 1.209, 0.292: 1.208,
                0.293: 1.206, 0.294: 1.204, 0.295: 1.202, 0.296: 1.200,
                0.297: 1.198, 0.298: 1.196, 0.299: 1.194, 0.300: 1.192,
                0.301: 1.191, 0.302: 1.189, 0.303: 1.187, 0.304: 1.185,
                0.305: 1.183, 0.306: 1.181, 0.307: 1.179, 0.308: 1.178,
                0.309: 1.176, 0.310: 1.174, 0.311: 1.172, 0.312: 1.170,
                0.313: 1.168, 0.314: 1.167, 0.315: 1.165, 0.316: 1.163,
                0.317: 1.161, 0.318: 1.159, 0.319: 1.158, 0.320: 1.156,
                0.321: 1.154, 0.322: 1.152, 0.323: 1.150, 0.324: 1.149,
                0.325: 1.147, 0.326: 1.145, 0.327: 1.143, 0.328: 1.142,
                0.329: 1.140, 0.330: 1.138, 0.331: 1.136, 0.332: 1.135,
                0.333: 1.133, 0.334: 1.131, 0.335: 1.129, 0.336: 1.128,
                0.337: 1.126, 0.338: 1.124, 0.339: 1.122, 0.340: 1.121,
                0.341: 1.119, 0.342: 1.117, 0.343: 1.116, 0.344: 1.114,
                0.345: 1.112, 0.346: 1.110, 0.347: 1.109, 0.348: 1.107,
                0.349: 1.105, 0.350: 1.104, 0.351: 1.102, 0.352: 1.100,
                0.353: 1.099, 0.354: 1.097, 0.355: 1.095, 0.356: 1.094,
                0.357: 1.092, 0.358: 1.090, 0.359: 1.089, 0.360: 1.087,
                0.361: 1.085, 0.362: 1.084, 0.363: 1.082, 0.364: 1.080,
                0.365: 1.079, 0.366: 1.077, 0.367: 1.075, 0.368: 1.074,
                0.369: 1.072, 0.370: 1.070, 0.371: 1.069, 0.372: 1.067,
                0.373: 1.066, 0.374: 1.064, 0.375: 1.062, 0.376: 1.061,
                0.377: 1.059, 0.378: 1.058, 0.379: 1.056, 0.380: 1.054,
                0.381: 1.053, 0.382: 1.051, 0.383: 1.050, 0.384: 1.048,
                0.385: 1.046, 0.386: 1.045, 0.387: 1.043, 0.388: 1.042,
                0.389: 1.040, 0.390: 1.038, 0.391: 1.037, 0.392: 1.035,
                0.393: 1.034, 0.394: 1.032, 0.395: 1.031, 0.396: 1.029,
                0.397: 1.027, 0.398: 1.026, 0.399: 1.024, 0.400: 1.023,
                0.401: 1.021, 0.402: 1.020, 0.403: 1.018, 0.404: 1.017,
                0.405: 1.015, 0.406: 1.013, 0.407: 1.012, 0.408: 1.010,
                0.409: 1.009, 0.410: 1.007, 0.411: 1.006, 0.412: 1.004,
                0.413: 1.003, 0.414: 1.001, 0.415: 1.000, 0.416: 0.998,
                0.417: 0.997, 0.418: 0.995, 0.419: 0.994, 0.420: 0.992,
                0.421: 0.991, 0.422: 0.989, 0.423: 0.988, 0.424: 0.986,
                0.425: 0.985, 0.426: 0.983, 0.427: 0.982, 0.428: 0.980,
                0.429: 0.979, 0.430: 0.977, 0.431: 0.976, 0.432: 0.974,
                0.433: 0.973, 0.434: 0.971, 0.435: 0.970, 0.436: 0.968,
                0.437: 0.967, 0.438: 0.965, 0.439: 0.964, 0.440: 0.962,
                0.441: 0.961, 0.442: 0.959, 0.443: 0.958, 0.444: 0.956,
                0.445: 0.955, 0.446: 0.954, 0.447: 0.952, 0.448: 0.951,
                0.449: 0.949, 0.450: 0.948, 0.451: 0.946, 0.452: 0.945,
                0.453: 0.943, 0.454: 0.942, 0.455: 0.940, 0.456: 0.939,
                0.457: 0.938, 0.458: 0.936, 0.459: 0.935, 0.460: 0.933,
                0.461: 0.932, 0.462: 0.930, 0.463: 0.929, 0.464: 0.928,
                0.465: 0.926, 0.466: 0.925, 0.467: 0.923, 0.468: 0.922,
                0.469: 0.920, 0.470: 0.919, 0.471: 0.918, 0.472: 0.916,
                0.473: 0.915, 0.474: 0.913, 0.475: 0.912, 0.476: 0.910,
                0.477: 0.909, 0.478: 0.908, 0.479: 0.906, 0.480: 0.905,
                0.481: 0.903, 0.482: 0.902, 0.483: 0.901, 0.484: 0.899,
                0.485: 0.898, 0.486: 0.896, 0.487: 0.895, 0.488: 0.894,
                0.489: 0.892, 0.490: 0.891, 0.491: 0.889, 0.492: 0.888,
                0.493: 0.887, 0.494: 0.885, 0.495: 0.884, 0.496: 0.882,
                0.497: 0.881, 0.498: 0.880, 0.499: 0.878, 0.500: 0.877,
                0.501: 0.876, 0.502: 0.874, 0.503: 0.873, 0.504: 0.871,
                0.505: 0.870, 0.506: 0.869, 0.507: 0.867, 0.508: 0.866,
                0.509: 0.865, 0.510: 0.863, 0.511: 0.862, 0.512: 0.860,
                0.513: 0.859, 0.514: 0.858, 0.515: 0.856, 0.516: 0.855,
                0.517: 0.854, 0.518: 0.852, 0.519: 0.851, 0.520: 0.849,
                0.521: 0.848, 0.522: 0.847, 0.523: 0.845, 0.524: 0.844,
                0.525: 0.843, 0.526: 0.841, 0.527: 0.840, 0.528: 0.839,
                0.529: 0.837, 0.530: 0.836, 0.531: 0.835, 0.532: 0.833,
                0.533: 0.832, 0.534: 0.831, 0.535: 0.829, 0.536: 0.828,
                0.537: 0.827, 0.538: 0.825, 0.539: 0.824, 0.540: 0.822,
                0.541: 0.821, 0.542: 0.820, 0.543: 0.818, 0.544: 0.817,
                0.545: 0.816, 0.546: 0.814, 0.547: 0.813, 0.548: 0.812,
                0.549: 0.810, 0.550: 0.809, 0.551: 0.808, 0.552: 0.806,
                0.553: 0.805, 0.554: 0.804, 0.555: 0.802, 0.556: 0.801,
                0.557: 0.800, 0.558: 0.799, 0.559: 0.797, 0.560: 0.796,
                0.561: 0.795, 0.562: 0.793, 0.563: 0.792, 0.564: 0.791,
                0.565: 0.789, 0.566: 0.788, 0.567: 0.787, 0.568: 0.785,
                0.569: 0.784, 0.570: 0.783, 0.571: 0.781, 0.572: 0.780,
                0.573: 0.779, 0.574: 0.777, 0.575: 0.776, 0.576: 0.775,
                0.577: 0.773, 0.578: 0.772, 0.579: 0.771, 0.580: 0.770,
                0.581: 0.768, 0.582: 0.767, 0.583: 0.766, 0.584: 0.764,
                0.585: 0.763, 0.586: 0.762, 0.587: 0.760, 0.588: 0.759,
                0.589: 0.758, 0.590: 0.756, 0.591: 0.755, 0.592: 0.754,
                0.593: 0.753, 0.594: 0.751, 0.595: 0.750, 0.596: 0.749,
                0.597: 0.747, 0.598: 0.746, 0.599: 0.745, 0.600: 0.743,
                0.601: 0.742, 0.602: 0.741, 0.603: 0.740, 0.604: 0.738,
                0.605: 0.737, 0.606: 0.736, 0.607: 0.734, 0.608: 0.733,
                0.609: 0.732, 0.610: 0.730, 0.611: 0.729, 0.612: 0.728,
                0.613: 0.727, 0.614: 0.725, 0.615: 0.724, 0.616: 0.723,
                0.617: 0.721, 0.618: 0.720, 0.619: 0.719, 0.620: 0.717,
                0.621: 0.716, 0.622: 0.715, 0.623: 0.714, 0.624: 0.712,
                0.625: 0.711, 0.626: 0.710, 0.627: 0.708, 0.628: 0.707,
                0.629: 0.706, 0.630: 0.705, 0.631: 0.703, 0.632: 0.702,
                0.633: 0.701, 0.634: 0.699, 0.635: 0.698, 0.636: 0.697,
                0.637: 0.696, 0.638: 0.694, 0.639: 0.693, 0.640: 0.692,
                0.641: 0.690, 0.642: 0.689, 0.643: 0.688, 0.644: 0.687,
                0.645: 0.685, 0.646: 0.684, 0.647: 0.683, 0.648: 0.681,
                0.649: 0.680, 0.650: 0.679, 0.651: 0.677, 0.652: 0.676,
                0.653: 0.675, 0.654: 0.674, 0.655: 0.672, 0.656: 0.671,
                0.657: 0.670, 0.658: 0.668, 0.659: 0.667, 0.660: 0.666,
                0.661: 0.665, 0.662: 0.663, 0.663: 0.662, 0.664: 0.661,
                0.665: 0.659, 0.666: 0.658, 0.667: 0.657, 0.668: 0.656,
                0.669: 0.654, 0.670: 0.653, 0.671: 0.652, 0.672: 0.650,
                0.673: 0.649, 0.674: 0.648, 0.675: 0.647, 0.676: 0.645,
                0.677: 0.644, 0.678: 0.643, 0.679: 0.641, 0.680: 0.640,
                0.681: 0.639, 0.682: 0.638, 0.683: 0.636, 0.684: 0.635,
                0.685: 0.634, 0.686: 0.632, 0.687: 0.631, 0.688: 0.630,
                0.689: 0.629, 0.690: 0.627, 0.691: 0.626, 0.692: 0.625,
                0.693: 0.623, 0.694: 0.622, 0.695: 0.621, 0.696: 0.619,
                0.697: 0.618, 0.698: 0.617, 0.699: 0.616, 0.700: 0.614,
                0.701: 0.613, 0.702: 0.612, 0.703: 0.610, 0.704: 0.609,
                0.705: 0.608, 0.706: 0.606, 0.707: 0.605, 0.708: 0.604,
                0.709: 0.603, 0.710: 0.601, 0.711: 0.600, 0.712: 0.599,
                0.713: 0.597, 0.714: 0.596, 0.715: 0.595, 0.716: 0.593,
                0.717: 0.592, 0.718: 0.591, 0.719: 0.590, 0.720: 0.588,
                0.721: 0.587, 0.722: 0.586, 0.723: 0.584, 0.724: 0.583,
                0.725: 0.582, 0.726: 0.580, 0.727: 0.579, 0.728: 0.578,
                0.729: 0.577, 0.730: 0.575, 0.731: 0.574, 0.732: 0.573,
                0.733: 0.571, 0.734: 0.570, 0.735: 0.569, 0.736: 0.567,
                0.737: 0.566, 0.738: 0.565, 0.739: 0.563, 0.740: 0.562,
                0.741: 0.561, 0.742: 0.559, 0.743: 0.558, 0.744: 0.557,
                0.745: 0.555, 0.746: 0.554, 0.747: 0.553, 0.748: 0.551,
                0.749: 0.550, 0.750: 0.549, 0.751: 0.547, 0.752: 0.546,
                0.753: 0.545, 0.754: 0.543, 0.755: 0.542, 0.756: 0.541,
                0.757: 0.539, 0.758: 0.538, 0.759: 0.537, 0.760: 0.535,
                0.761: 0.534, 0.762: 0.533, 0.763: 0.531, 0.764: 0.530,
                0.765: 0.529, 0.766: 0.527, 0.767: 0.526, 0.768: 0.525,
                0.769: 0.523, 0.770: 0.522, 0.771: 0.521, 0.772: 0.519,
                0.773: 0.518, 0.774: 0.517, 0.775: 0.515, 0.776: 0.514,
                0.777: 0.513, 0.778: 0.511, 0.779: 0.510, 0.780: 0.508,
                0.781: 0.507, 0.782: 0.506, 0.783: 0.504, 0.784: 0.503,
                0.785: 0.502, 0.786: 0.500, 0.787: 0.499, 0.788: 0.498,
                0.789: 0.496, 0.790: 0.495, 0.791: 0.493, 0.792: 0.492,
                0.793: 0.491, 0.794: 0.489, 0.795: 0.488, 0.796: 0.487,
                0.797: 0.485, 0.798: 0.484, 0.799: 0.482, 0.800: 0.481,
                0.801: 0.480, 0.802: 0.478, 0.803: 0.477, 0.804: 0.475,
                0.805: 0.474, 0.806: 0.473, 0.807: 0.471, 0.808: 0.470,
                0.809: 0.468, 0.810: 0.467, 0.811: 0.466, 0.812: 0.464,
                0.813: 0.463, 0.814: 0.461, 0.815: 0.460, 0.816: 0.458,
                0.817: 0.457, 0.818: 0.456, 0.819: 0.454, 0.820: 0.453,
                0.821: 0.451, 0.822: 0.450, 0.823: 0.448, 0.824: 0.447,
                0.825: 0.445, 0.826: 0.444, 0.827: 0.443, 0.828: 0.441,
                0.829: 0.440, 0.830: 0.438, 0.831: 0.437, 0.832: 0.435,
                0.833: 0.434, 0.834: 0.432, 0.835: 0.431, 0.836: 0.429,
                0.837: 0.428, 0.838: 0.426, 0.839: 0.425, 0.840: 0.424,
                0.841: 0.422, 0.842: 0.421, 0.843: 0.419, 0.844: 0.418,
                0.845: 0.416, 0.846: 0.415, 0.847: 0.413, 0.848: 0.412,
                0.849: 0.410, 0.850: 0.408, 0.851: 0.407, 0.852: 0.405,
                0.853: 0.404, 0.854: 0.402, 0.855: 0.401, 0.856: 0.399,
                0.857: 0.398, 0.858: 0.396, 0.859: 0.395, 0.860: 0.393,
                0.861: 0.392, 0.862: 0.390, 0.863: 0.388, 0.864: 0.387,
                0.865: 0.385, 0.866: 0.384, 0.867: 0.382, 0.868: 0.381,
                0.869: 0.379, 0.870: 0.377, 0.871: 0.376, 0.872: 0.374,
                0.873: 0.373, 0.874: 0.371, 0.875: 0.369, 0.876: 0.368,
                0.877: 0.366, 0.878: 0.365, 0.879: 0.363, 0.880: 0.361,
                0.881: 0.360, 0.882: 0.358, 0.883: 0.356, 0.884: 0.355,
                0.885: 0.353, 0.886: 0.351, 0.887: 0.350, 0.888: 0.348,
                0.889: 0.346, 0.890: 0.345, 0.891: 0.343, 0.892: 0.341,
                0.893: 0.340, 0.894: 0.338, 0.895: 0.336, 0.896: 0.334,
                0.897: 0.333, 0.898: 0.331, 0.899: 0.329, 0.900: 0.327,
                0.901: 0.326, 0.902: 0.324, 0.903: 0.322, 0.904: 0.320,
                0.905: 0.319, 0.906: 0.317, 0.907: 0.315, 0.908: 0.313,
                0.909: 0.311, 0.910: 0.309, 0.911: 0.308, 0.912: 0.306,
                0.913: 0.304, 0.914: 0.302, 0.915: 0.300, 0.916: 0.298,
                0.917: 0.296, 0.918: 0.295, 0.919: 0.293, 0.920: 0.291,
                0.921: 0.289, 0.922: 0.287, 0.923: 0.285, 0.924: 0.283,
                0.925: 0.281, 0.926: 0.279, 0.927: 0.277, 0.928: 0.275,
                0.929: 0.273, 0.930: 0.271, 0.931: 0.269, 0.932: 0.267,
                0.933: 0.265, 0.934: 0.263, 0.935: 0.261, 0.936: 0.259,
                0.937: 0.256, 0.938: 0.254, 0.939: 0.252, 0.940: 0.250,
                0.941: 0.248, 0.942: 0.246, 0.943: 0.243, 0.944: 0.241,
                0.945: 0.239, 0.946: 0.237, 0.947: 0.234, 0.948: 0.232,
                0.949: 0.230, 0.950: 0.227, 0.951: 0.225, 0.952: 0.223,
                0.953: 0.220, 0.954: 0.218, 0.955: 0.215, 0.956: 0.213,
                0.957: 0.210, 0.958: 0.208, 0.959: 0.205, 0.960: 0.203,
                0.961: 0.200, 0.962: 0.197, 0.963: 0.195, 0.964: 0.192,
                0.965: 0.189, 0.966: 0.187, 0.967: 0.184, 0.968: 0.181,
                0.969: 0.178, 0.970: 0.175, 0.971: 0.172, 0.972: 0.169,
                0.973: 0.166, 0.974: 0.163, 0.975: 0.159, 0.976: 0.156,
                0.977: 0.153, 0.978: 0.149, 0.979: 0.146, 0.980: 0.142,
                0.981: 0.139, 0.982: 0.135, 0.983: 0.131, 0.984: 0.127,
                0.985: 0.123, 0.986: 0.119, 0.987: 0.115, 0.988: 0.110,
                0.989: 0.105, 0.990: 0.100, 0.991: 0.095, 0.992: 0.090,
                0.993: 0.084, 0.994: 0.078, 0.995: 0.071, 0.996: 0.063,
                0.997: 0.055, 0.998: 0.045, 0.999: 0.032}

    if delta < 0.001:
        return theta_mm[0.001]
    elif delta > 0.999:
        return theta_mm[0.999]
    else:
        keys_list = sorted(list(theta_mm.keys()))
        ix = bisect.bisect(keys_list, delta) - 1

        return theta_mm[keys_list[ix]]
