"""Interface to the `SLURM job scheduler <https://slurm.schedmd.com/documentation.html>`_

.. autofunction:: create_slurm_script
"""

from typing import Any, Dict, List

from ..utils import Options


def create_slurm_script(opts: Options, jobs: List[Dict[str, Any]], jobs_metadata: List[Options]) -> str:
    """Create a script to run the workflow using the SLURM job schedule."""
    slurm_file = "launch.sh"

    # Get SLURM configuration
    scheduler = opts.scheduler

    # Use the configuration provided by the user
    if scheduler.free_format is not None:
        script = scheduler.free_format
    else:
        script = make_script(opts.scheduler)

    # Append command to run the workflow
    for meta, job in zip(jobs_metadata, jobs):
        smile = job["property"]["smile"]
        input_file = opts.input.absolute().as_posix()
        workdir = opts.workdir.absolute().as_posix()
        script += f'\n{opts.command} -s "{smile}" -i {input_file} -w {workdir}'

    with open(slurm_file, 'w') as handler:
        handler.write(script)

    return f"sbatch {slurm_file.absolute().as_posix()}"


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
