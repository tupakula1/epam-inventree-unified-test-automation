"""API BDD scenario collector.

This module imports all step modules so pytest can collect the scenario-generated tests.
"""

from tests.api.steps.category_steps import *  # noqa: F401,F403
from tests.api.steps.docs_api_steps import *  # noqa: F401,F403
from tests.api.steps.parts_edge_cases_steps import *  # noqa: F401,F403
from tests.api.steps.parts_filter_steps import *  # noqa: F401,F403
from tests.api.steps.parts_steps import *  # noqa: F401,F403
from tests.api.steps.parts_validation_steps import *  # noqa: F401,F403
