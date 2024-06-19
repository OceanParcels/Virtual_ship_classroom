"""ADCP instrument."""

import numpy as np
import py
from parcels import FieldSet, JITParticle, ScipyParticle, ParticleSet, Variable

from ..spacetime import Spacetime

_ADCPParticle = ScipyParticle.add_variables(
    [
        Variable("U", dtype=np.float32, initial=np.nan),
        Variable("V", dtype=np.float32, initial=np.nan),
    ]
)


def _sample_velocity(particle, fieldset, time):
    particle.U, particle.V = fieldset.UV.eval(
        time, particle.depth, particle.lat, particle.lon, applyConversion=False
    )


def simulate_adcp(
    fieldset: FieldSet,
    out_path: str | py.path.LocalPath,
    max_depth: float,
    min_depth: float,
    num_bins: int,
    sample_points: list[Spacetime],
) -> None:
    """
    Use parcels to simulate an ADCP in a fieldset.

    :param fieldset: The fieldset to simulate the ADCP in.
    :param out_path: The path to write the results to.
    :param max_depth: Maximum depth the ADCP can measure.
    :param min_depth: Minimum depth the ADCP can measure.
    :param num_bins: How many samples to take in the complete range between max_depth and min_depth.
    :param sample_points: The places and times to sample at.
    """
    sample_points.sort(key=lambda p: p.time)

    bins = np.linspace(max_depth, min_depth, num_bins)
    num_particles = len(bins)
    particleset = ParticleSet.from_list(
        fieldset=fieldset,
        pclass=_ADCPParticle,
        lon=np.full(
            num_particles, 0.0
        ),  # initial lat/lon are irrelevant and will be overruled later.
        lat=np.full(num_particles, 0.0),
        depth=bins,
        time=0,  # same for time
    )

    # define output file for the simulation
    # outputdt set to infinie as we want to just want to write at the end of every call to 'execute'
    out_file = particleset.ParticleFile(name=out_path, outputdt=np.inf)

    for point in sample_points:
        particleset.lon_nextloop[:] = point.location.lon
        particleset.lat_nextloop[:] = point.location.lat
        particleset.time_nextloop[:] = fieldset.time_origin.reltime(
            np.datetime64(point.time)
        )

        # perform one step using the particleset
        # dt and runtime are set so exactly one step is made.
        particleset.execute(
            [_sample_velocity],
            dt=1,
            runtime=1,
            verbose_progress=False,
            output_file=out_file,
        )
