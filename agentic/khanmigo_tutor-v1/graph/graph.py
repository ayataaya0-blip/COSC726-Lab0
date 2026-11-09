from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from graph.state import TutorState

from graph.nodes import (
    input_gate_node,
    understand_node,
    plan_node,
    action_gate_node,
    act_node,
    observe_node,
    reflect_node,
    respond_node,
    validate_node,
    output_gate_node,
    repair_node,
)

from graph.routes import (
    input_route,
    action_route,
    reflection_route,
    output_route,
)


# =========================================================
# Build Tutor Graph
# =========================================================

def build_tutor_graph():

    builder = StateGraph(TutorState)

    # -----------------------------------------------------
    # Register Nodes
    # -----------------------------------------------------

    builder.add_node(
        "input_gate",
        input_gate_node,
    )

    builder.add_node(
        "understand",
        understand_node,
    )

    builder.add_node(
        "plan",
        plan_node,
    )

    builder.add_node(
        "action_gate",
        action_gate_node,
    )

    builder.add_node(
        "act",
        act_node,
    )

    builder.add_node(
        "observe",
        observe_node,
    )

    builder.add_node(
        "reflect",
        reflect_node,
    )

    builder.add_node(
        "respond",
        respond_node,
    )

    builder.add_node(
        "validate",
        validate_node,
    )

    builder.add_node(
        "output_gate",
        output_gate_node,
    )

    builder.add_node(
        "repair",
        repair_node,
    )

    # -----------------------------------------------------
    # Start → Input Gate
    # -----------------------------------------------------

    builder.add_edge(
        START,
        "input_gate",
    )

    # -----------------------------------------------------
    # Input Gate → Understand / End
    # -----------------------------------------------------

    builder.add_conditional_edges(
        "input_gate",
        input_route,
        {
            "understand": "understand",
            "end": END,
        },
    )

    # -----------------------------------------------------
    # Understand → Plan
    # -----------------------------------------------------

    builder.add_edge(
        "understand",
        "plan",
    )

    # -----------------------------------------------------
    # Plan → Action Gate
    # -----------------------------------------------------

    builder.add_edge(
        "plan",
        "action_gate",
    )

    # -----------------------------------------------------
    # Action Gate → Act / End
    # -----------------------------------------------------

    builder.add_conditional_edges(
        "action_gate",
        action_route,
        {
            "act": "act",
            "end": END,
        },
    )

    # -----------------------------------------------------
    # Act → Observe
    # -----------------------------------------------------

    builder.add_edge(
        "act",
        "observe",
    )

    # -----------------------------------------------------
    # Observe → Reflect
    # -----------------------------------------------------

    builder.add_edge(
        "observe",
        "reflect",
    )

    # -----------------------------------------------------
    # Reflect → Plan / Respond
    # -----------------------------------------------------

    builder.add_conditional_edges(
        "reflect",
        reflection_route,
        {
            "plan": "plan",
            "respond": "respond",
        },
    )

    # -----------------------------------------------------
    # Respond → Validate
    # -----------------------------------------------------

    builder.add_edge(
        "respond",
        "validate",
    )

    # -----------------------------------------------------
    # Validate → Output Gate
    # -----------------------------------------------------

    builder.add_edge(
        "validate",
        "output_gate",
    )

    # -----------------------------------------------------
    # Output Gate → End / Repair
    # -----------------------------------------------------

    builder.add_conditional_edges(
        "output_gate",
        output_route,
        {
            "end": END,
            "repair": "repair",
        },
    )

    # -----------------------------------------------------
    # Repair → Output Gate
    # -----------------------------------------------------

    builder.add_edge(
        "repair",
        "output_gate",
    )

    # -----------------------------------------------------
    # Compile Graph
    # -----------------------------------------------------

    return builder.compile()


# =========================================================
# Compiled Tutor Graph
# =========================================================

tutor_graph = build_tutor_graph()