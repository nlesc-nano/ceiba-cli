"""Interface to the `SLURM job scheduler <https://slurm.schedmd.com/documentation.html>`_

.. autofunction:: create_slurm_script
"""

from pathlib import Path

from ..utils import Options


def create_slurm_script(opts: Options, input_file: Path) -> str:
    """Create a script to run the workflow using the SLURM job schedule."""
    job_workdir = input_file.parent
    slurm_file = job_workdir / "launch.sh"

    # Get SLURM configuration
    scheduler = opts.scheduler

    # Use the configuration provided by the user
    if scheduler.free_format is not None:
        script = scheduler.free_format
    else:
        script = make_script(opts.scheduler)

    # Append command to run the workflow
    cmd = f"\n{opts.command} {input_file.absolute().as_posix()}"
    script += f"\n{cmd}"

    with open(slurm_file, 'w') as handler:
        handler.write(script)

    return slurm_file.absolute().as_posix()


def make_script(scheduler: Options) -> str:
    """Create a SLURM script using the ``scheduler`` options."""
    arguments = {"cpus-per-task", "partition"}
    script = f"""#!/bin/bash

#SBATCH -N {scheduler.nodes}
#SBATCH -t {scheduler.wall_time}
"""
    # Add optional arguments
    for arg in arguments:
        value = scheduler.get(arg, None)
        if value is not None:
            script += f"#SBATCH --{arg} {value}\n"

    return script
