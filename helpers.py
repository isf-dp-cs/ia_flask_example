import random

def diversity_score(group):
    """
    Example: Higher score for a better mix of sciences.
    Returns the count of unique science majors in the group.
    """
    if not group: return 0
    sciences = [s.science for s in group]
    return len(set(sciences))

def maybe_swap(group_1, group_2):
    """Based on Ms. Genzlinger's version with help of Gemini """
    old_sum = diversity_score(group_1) + diversity_score(group_2)
    
    for i in range(len(group_1)):
        for j in range(len(group_2)):
            # 1. Perform the swap using Python's "a, b = b, a" trick
            group_1[i], group_2[j] = group_2[j], group_1[i]
            
            new_sum = diversity_score(group_1) + diversity_score(group_2)
            
            # 2. If it improved, keep it and stop
            if new_sum > old_sum:
                return True
            
            # 3. If it DID NOT improve, swap them back exactly where they were
            group_1[i], group_2[j] = group_2[j], group_1[i]
            
    return False


def random_assignment(students, num_groups):
    random.shuffle(students)
    groups = [[] for _ in range(num_groups)]
    for i in range(len(students)):
        groups[i % num_groups].append(students[i])
    return groups

def assign_to_groups(students, num_groups):
    """Written by Ms. Genzlinger"""

    groups = random_assignment(students, num_groups)
    while True:
        has_swapped = False
        for i in range(len(groups)):
            group_1 = groups[i]
            for j in range(i + 1, len(groups)):
                group_2 = groups[j]
                if maybe_swap(group_1, group_2):
                    has_swapped = True
        if not has_swapped:
            return groups