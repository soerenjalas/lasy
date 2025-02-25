# -*- coding: utf-8 -*-

import pytest

from lasy.laser import Laser
from lasy.profiles import CombinedLongitudinalTransverseProfile, GaussianProfile
from lasy.profiles.longitudinal import GaussianLongitudinalProfile
from lasy.profiles.transverse import (
    LaguerreGaussianTransverseProfile,
    SuperGaussianTransverseProfile,
)


@pytest.fixture(scope="function")
def gaussian():
    # Cases with Gaussian laser
    wavelength = 0.8e-6
    pol = (1, 0)
    laser_energy = 1.0  # J
    t_peak = 0.0e-15  # s
    tau = 30.0e-15  # s
    w0 = 5.0e-6  # m
    profile = GaussianProfile(wavelength, pol, laser_energy, w0, tau, t_peak)

    return profile


def test_profile_gaussian_3d_cartesian(gaussian):
    # - 3D Cartesian case
    dim = "xyt"
    lo = (-10e-6, -10e-6, -60e-15)
    hi = (+10e-6, +10e-6, +60e-15)
    npoints = (100, 100, 100)

    laser = Laser(dim, lo, hi, npoints, gaussian)
    laser.write_to_file("gaussianlaser3d")
    laser.propagate(1e-6)
    laser.write_to_file("gaussianlaser3d")


def test_profile_gaussian_cylindrical(gaussian):
    # - Cylindrical case
    dim = "rt"
    lo = (0e-6, -60e-15)
    hi = (10e-6, +60e-15)
    npoints = (50, 100)

    laser = Laser(dim, lo, hi, npoints, gaussian)
    laser.write_to_file("gaussianlaserRZ")
    laser.propagate(1e-6)
    laser.write_to_file("gaussianlaserRZ")


def test_profile_laguerre_gauss():
    # Case with Laguerre-Gauss laser
    wavelength = 0.8e-6
    pol = (1, 0)
    laser_energy = 1.0  # J
    t_peak = 0.0e-15  # s
    tau = 30.0e-15  # s
    w0 = 5.0e-6  # m
    profile = CombinedLongitudinalTransverseProfile(
        wavelength,
        pol,
        laser_energy,
        GaussianLongitudinalProfile(wavelength, tau, t_peak),
        LaguerreGaussianTransverseProfile(w0, p=0, m=1),
    )

    # - Cylindrical case
    dim = "rt"
    lo = (0e-6, -60e-15)
    hi = (10e-6, +60e-15)
    npoints = (50, 100)

    laser = Laser(dim, lo, hi, npoints, profile, n_azimuthal_modes=2)
    laser.write_to_file("laguerrelaserRZ")
    laser.propagate(1e-6)
    laser.write_to_file("laguerrelaserRZ")


def test_profile_super_gauss():
    # Case with super-Gaussian laser
    wavelength = 0.8e-6
    pol = (1, 0)
    laser_energy = 1.0  # J
    t_peak = 0.0e-15  # s
    tau = 30.0e-15  # s
    w0 = 5.0e-6  # m
    profile = CombinedLongitudinalTransverseProfile(
        wavelength,
        pol,
        laser_energy,
        GaussianLongitudinalProfile(wavelength, tau, t_peak),
        SuperGaussianTransverseProfile(w0, n_order=10),
    )

    # - Cylindrical case
    dim = "rt"
    lo = (0e-6, -60e-15)
    hi = (10e-6, +60e-15)
    npoints = (50, 100)

    laser = Laser(dim, lo, hi, npoints, profile, n_azimuthal_modes=2)
    laser.write_to_file("superGaussianlaserRZ")
    laser.propagate(1)
    laser.write_to_file("superGaussianlaserRZ")

    return profile
