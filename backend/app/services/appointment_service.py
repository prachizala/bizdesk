from typing import List, Dict, Any, Tuple

def time_to_minutes(time_str: str) -> int:
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])

def check_time_collision(
    new_start: str,
    new_end: str,
    existing_slots: List[Tuple[str, str]]
) -> bool:
    """
    Enforces atomic temporal non-overlap constraint:
    Overlap iff (New_Start < Exist_End) and (New_End > Exist_Start)
    """
    n_start = time_to_minutes(new_start)
    n_end = time_to_minutes(new_end)

    if n_start >= n_end:
        raise ValueError("Start time must be strictly before end time.")

    for ex_start, ex_end in existing_slots:
        e_start = time_to_minutes(ex_start)
        e_end = time_to_minutes(ex_end)
        if (n_start < e_end) and (n_end > e_start):
            return True  # Collision detected

    return False  # Available
