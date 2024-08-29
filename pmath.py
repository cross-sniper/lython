def clamp(source, min_val, max_val) -> int:
    return max(min_val, min(source, max_val))

def ease(current, target, easing_factor) -> float:
    """
    Gradually moves the current value closer to the target value.
    
    :param current: The current value.
    :param target: The target value to move towards.
    :param easing_factor: A factor between 0 and 1 determining the speed of easing.
                          A smaller value results in slower movement, closer to 1 is faster.
    :return: The new eased value.
    """
    return current + (target - current) * easing_factor
