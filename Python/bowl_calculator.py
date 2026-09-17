"""
Segmented Bowl Calculator
Calculates trapezoid segment dimensions for a segmented bowl ring.
"""

import math


def ask_float(prompt, default):
    """Ask for a number; an empty answer keeps the default."""
    answer = input(f"{prompt} [{default}]: ").strip().replace(",", ".")
    return float(answer) if answer else default


def get_inputs():
    print("=== Segmented Bowl Calculator ===\n")

    num_segments = int(input("Number of segments: "))
    outer_diameter = float(input("Outer diameter at the bottom of the ring (mm): "))
    wall_thickness = float(input("Wall thickness (mm): "))
    ring_height = ask_float("Ring height (mm)", 0.0)
    wall_slope = ask_float("Wall slope from horizontal (degrees, 90 = straight)", 90.0)

    return num_segments, outer_diameter, wall_thickness, ring_height, wall_slope


def calculate_segment(num_segments, outer_diameter, wall_thickness,
                      ring_height=0.0, wall_slope=90.0):
    """
    Calculate trapezoid dimensions for a single segment.

    outer_diameter is the finished diameter at the BOTTOM of the ring.

    A ring is not a line. On a sloping wall the outside already moves outwards
    over the height of that one ring, by ring_height / tan(wall_slope) per side.
    The blank has to reach the widest point of the ring and clear the narrowest,
    so the trapezoid is set out between those two diameters. With ring_height 0
    or a slope of 90 degrees this falls back to a single diameter.

    Returns a dict with the calculated dimensions.
    """
    alfa = 360 / (num_segments * 2)     # the angle of the trapezoid
    slope = math.radians(min(max(wall_slope, 20.0), 150.0))

    growth = 2 * ring_height / math.tan(slope)      # over the full diameter
    d_bottom = outer_diameter
    d_top = outer_diameter + growth

    outer_blank = max(d_bottom, d_top)                          # widest point
    inner_blank = min(d_bottom, d_top) - (2 * wall_thickness)   # narrowest point

    results = {
        "miter_angle": alfa,
        "longside_trapezoid": outer_blank * math.tan(math.radians(alfa)),
        "shortside_trapezoid": inner_blank * math.sin(math.radians(alfa)),
        "depth_trapezoid": (outer_blank / 2) - (inner_blank / 2) * math.cos(math.radians(alfa)),

        "outer_diameter_blank": outer_blank,
        "inner_diameter_blank": inner_blank,
        "num_segments": num_segments,
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
        if key == "miter_angle":
            print(f"  {label}: {value:.2f} deg  (each end, off square)")
        elif isinstance(value, float):
            print(f"  {label}: {value:.2f} mm")
        else:
            print(f"  {label}: {value}")


if __name__ == "__main__":
    num_segments, outer_diameter, wall_thickness, ring_height, wall_slope = get_inputs()
    results = calculate_segment(num_segments, outer_diameter, wall_thickness,
                                ring_height, wall_slope)
    display_results(results)
    draw_segment(results)
