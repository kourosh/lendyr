from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.tools.types import (
    PythonToolKind,
    PluginContext,
    AgentPreInvokePayload,
    AgentPreInvokeResult,
)

# Phrases that indicate the user is asking about Lendyr branch locations.
# A whitelist approach: if NONE of these match, the request is blocked.
_ALLOWED_PATTERNS = [
    "branch",
    "branches",
    "location",
    "locations",
    "nearest",
    "closest",
    "near me",
    "find a",
    "show all",
    "show me",
    "where is",
    "where are",
    "map",
    "lendyr",
]

_BLOCKED_RESPONSE = (
    "I can only help you find Lendyr Bank branches. "
    "Try asking 'Find a branch near Oakland' or 'Show me all branch locations.'"
)


def _is_branch_query(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in _ALLOWED_PATTERNS)


@tool(
    description="Pre-invoke guardrail for the branch locator agent. Blocks any request "
                "that is not related to finding Lendyr Bank branch locations.",
    kind=PythonToolKind.AGENTPREINVOKE,
)
def branch_locator_guardrail(
    plugin_context: PluginContext,
    agent_pre_invoke_payload: AgentPreInvokePayload,
) -> AgentPreInvokeResult:
    result = AgentPreInvokeResult()

    if not agent_pre_invoke_payload or not agent_pre_invoke_payload.messages:
        result.continue_processing = True
        return result

    user_input = agent_pre_invoke_payload.messages[-1].content.text or ""

    if _is_branch_query(user_input):
        result.continue_processing = True
        result.modified_payload = agent_pre_invoke_payload
    else:
        result.continue_processing = False
        result.modified_payload = _BLOCKED_RESPONSE

    return result
