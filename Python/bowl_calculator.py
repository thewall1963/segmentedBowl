"""
Segmented Bowl Calculator
Calculates trapezoid segment dimensions for a segmented bowl ring.
"""

import math


def get_inputs():
    print("=== Segmented Bowl Calculator ===\n")

    num_segments = int(input("Number of segments: "))
    outer_diameter = float(input("Outer diameter (mm): "))
    wall_thickness = float(input("Wall thickness (mm): "))

    return num_segments, outer_diameter, wall_thickness


def calculate_segment(num_segments, outer_diameter, wall_thickness):
    """
    Calculate trapezoid dimensions for a single segment.

    Returns a dict with the calculated dimensions.
    Add your calculation logic here.
    """
    inner_diameter = outer_diameter - (2 * wall_thickness)


    # TODO: Add your calculations here

    alfa = 360 /(num_segments*2)    # the angle of the trapezoid



    results = {
        "longside_trapezoid" : 2 * ((outer_diameter / 2) * math.tan(math.radians(alfa))),
        "depth_trapezoid" : (outer_diameter/2) - ((outer_diameter/2) - wall_thickness ) * math.cos(math.radians(alfa)),

        "num_segments": num_segments,
        #"outer_diameter": outer_diameter,
        #"inner_diameter": inner_diameter,
        #"wall_thickness": wall_thickness,
    }

    return results


def draw_segment(results):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Arc

    longside = results["longside_trapezoid"]
    depth    = results["depth_trapezoid"]
    alfa     = 360 / (results["num_segments"] * 2)

    offset    = depth * math.tan(math.radians(alfa))
    shortside = longside - 2 * offset

    # Corners: bottom-left, bottom-right, top-right, top-left
    points = [
        [0,                  0],
        [longside,           0],
        [longside - offset,  depth],
        [offset,             depth],
    ]

    fig, ax = plt.subplots()
    polygon = Polygon(points, closed=True, fill=False, edgecolor="black", linewidth=2)
    ax.add_patch(polygon)

    margin = longside * 0.1
    ax.set_xlim(-margin, longside + margin)
    ax.set_ylim(-margin, depth + margin)
    ax.set_aspect("equal")
    ax.set_xlabel("mm")
    ax.set_ylabel("mm")
    ax.annotate(f"Long side: {longside:.2f} mm",   xy=(longside / 2, -1),     ha="center", va="top",    fontsize=9)
    ax.annotate(f"Short side: {shortside:.2f} mm", xy=(longside / 2, depth+1), ha="center", va="bottom", fontsize=9)
    ax.annotate(f"Depth: {depth:.2f} mm",          xy=(longside, depth / 2), ha="left",   va="center", fontsize=9, rotation=90)

    # Draw angle arc at bottom-left corner (angle between base and slant side)
    arc_r = depth * 0.3
    interior_angle = 90 - alfa   # angle from horizontal to the slant
    arc = Arc((0, 0), width=arc_r*2, height=arc_r*2,
              angle=0, theta1=90 - alfa, theta2=90, color="blue", linewidth=1.5)
    ax.add_patch(arc)
    # Label in the middle of the arc
    label_angle = math.radians(90 - alfa / 2)
    ax.annotate(f"α={alfa:.1f}°",
                xy=(arc_r * 0.6 * math.cos(label_angle), arc_r * 0.6 * math.sin(label_angle)),
                ha="right", va="bottom", fontsize=8, color="blue")
    plt.title("Trapezoid Segment")
    plt.tight_layout()
    plt.show()


def display_results(results):
    print("\n=== Results ===")
    for key, value in results.items():
        label = key.replace("_", " ").title()
        if isinstance(value, float):
            print(f"  {label}: {value:.2f} mm")
        else:
            print(f"  {label}: {value}")


if __name__ == "__main__":
    num_segments, outer_diameter, wall_thickness = get_inputs()
    results = calculate_segment(num_segments, outer_diameter, wall_thickness)
    display_results(results)
    draw_segment(results)
