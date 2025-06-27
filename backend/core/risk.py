def confidence_gate(action: str, confidence: float, threshold: float = 0.95) -> str:
    """Return the action if confidence meets the threshold, otherwise 'NONE'."""
    if confidence >= threshold:
        return action
    return "NONE"
