from leap.workflow.tracing import traceable
from leap.workflow.nodes.input_validation import validate_input as _validate_input
from leap.workflow.nodes.planning import plan_scenes as _plan_scenes
from leap.workflow.nodes.generation import generate_code as _generate_code
from leap.workflow.nodes.validation import validate_code as _validate_code
from leap.workflow.nodes.execution import execute_code as _execute_code
from leap.workflow.nodes.correction import error_correction as _error_correction

# Apply traceable decorator to all node functions
validate_input = traceable(name="validate_input", tags=["input_validation"])(_validate_input)
plan_scenes = traceable(name="plan_scenes", tags=["planning"])(_plan_scenes)
generate_code = traceable(name="generate_code", tags=["generation"])(_generate_code)
validate_code = traceable(name="validate_code", tags=["validation"])(_validate_code)
execute_code = traceable(name="execute_code", tags=["execution"])(_execute_code)
error_correction = traceable(name="error_correction", tags=["correction"])(_error_correction)

__all__ = [
    "validate_input",
    "plan_scenes",
    "generate_code",
    "validate_code",
    "execute_code",
    "error_correction"
]
