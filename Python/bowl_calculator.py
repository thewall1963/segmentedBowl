"""
Segmented Bowl Calculator
Calculates trapezoid segment dimensions for a segmented bowl ring.
"""


def get_inputs():
    print("=== Segmented Bowl Calculator ===\n")

    num_segments = int(input("Number of segments: "))
    outer_diameter = float(input("Outer diameter (inches): "))
    wall_thickness = float(input("Wall thickness (inches): "))

    return num_segments, outer_diameter, wall_thickness


def calculate_segment(num_segments, outer_diameter, wall_thickness):
    """
    Calculate trapezoid dimensions for a single segment.

    Returns a dict with the calculated dimensions.
    Add your calculation logic here.
    """
    inner_diameter = outer_diameter - (2 * wall_thickness)

    # TODO: Add your calculations here
    results = {
        "num_segments": num_segments,
        "outer_diameter": outer_diameter,
        "inner_diameter": inner_diameter,
        "wall_thickness": wall_thickness,
    }

    return results


def display_results(results):
    print("\n=== Results ===")
    for key, value in results.items():
        label = key.replace("_", " ").title()
        if isinstance(value, float):
            print(f"  {label}: {value:.4f}\"")
        else:
            print(f"  {label}: {value}")


if __name__ == "__main__":
    num_segments, outer_diameter, wall_thickness = get_inputs()
    results = calculate_segment(num_segments, outer_diameter, wall_thickness)
    display_results(results)
