from collections import defaultdict

def invert_call_graph(call_graph: dict) -> dict:
    """
    Converts:
        caller -> [callee1, callee2]
    Into:
        callee -> [caller1, caller2]
    """
    inverted = defaultdict(set)

    for caller, callees in call_graph.items():
        for callee in callees:
            inverted[callee].add(caller)

    return {k: sorted(v) for k, v in inverted.items()}


def merge_call_graphs(graphs: list[dict]) -> dict:
    """
    Merges multiple call graphs into one.

    Each graph is expected to be:
        caller -> [callees]

    Returns:
        merged_graph: caller -> [unique callees]
    """
    merged = defaultdict(set)

    for graph in graphs:
        for caller, callees in graph.items():
            for callee in callees:
                merged[caller].add(callee)

    return {k: sorted(v) for k, v in merged.items()}
