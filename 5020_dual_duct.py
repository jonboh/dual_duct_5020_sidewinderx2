import numpy as np
import solid2 as s

_FN = 10


def chained_hull(pieces):
    hulls = list()
    for i in range(len(pieces) - 1):
        p0 = pieces[i]
        p1 = pieces[i + 1]
        hulls.append(s.hull()(p0, p1))
    return s.union()(*hulls)


def section(width, heigth, exponent, steps, basic_size=1):
    pieces = list()
    for k in map(lambda x: x / steps, range(steps + 1)):
        y = k
        x = np.power(1 - np.power(y, exponent), (1 / exponent))
        pieces.append(
            s.translate([width / 2 * x, heigth / 2 * y, 0])(
                s.cube(basic_size, center=True)
            )
        )
    piece = chained_hull(pieces)
    piece = s.union()(
        piece,
        s.rotate([0, 0, 180])(piece),
        s.rotate([0, 180, 0])(piece),
        s.rotate([180, 0, 0])(piece),
    )
    return piece


def transition(p1, pT, p_t, t):
    return [p_t(p1[i], pT[i], t)[i] for i in range(len(p1))]


def make_tubbing(
    pos1, posT, pos_t, rot1, rotT, rot_t, x0, x0_, y0, y0_, x1, x1_, y1, y1_, steps
):
    union_block = s.translate([-15, -10, -2.5])(  # block
        s.hull()(
            s.translate([0, 6.5, 2.5])(s.cube([15, 14.5, 10], center=False)),
            s.translate([0, 2, 2])(
                s.rotate([60, 0, 0])(s.cube([15, 10, 2], center=False))
            ),
        )
    )
    np.arange
    exponent = lambda t: 8 if 0 < t < 0.25 else 1.5 if 0.25 < t < 0.75 else 8
    tube = chained_hull(
        [
            (
                s.translate(transition(pos1, posT, pos_t, t))(
                    s.rotate(transition(rot1, rotT, rot_t, t))(
                        section(
                            x0_ * (1 - t) + x1_ * t,
                            y0_ * (1 - t) + y1_ * t,
                            exponent(t),
                            steps,
                            1,
                        )
                    )
                )
            )
            for t in map(lambda x: x / steps, range(steps + 1))
        ]
    )
    # return tube
    outer = s.union()(
        tube,
        union_block,
    )
    # outer = tube

    inner = chained_hull(
        [
            s.translate(transition(pos1, posT, pos_t, t))(
                s.rotate(transition(rot1, rotT, rot_t, t))(
                    section(
                        x0 * (1 - t) + x1 * t,
                        y0 * (1 - t) + y1 * t,
                        exponent(t),
                        steps,
                        1.5,
                    )
                )
            )
            for t in map(lambda x: x / steps, range(steps + 1))
        ]
    )
    return (s.difference()(outer, inner), inner)


def make_left_tubbing(x0, y0, outer_width, steps):
    # 18x23
    x1 = 12 - outer_width
    y1 = 33 - outer_width

    x0_ = x0 + outer_width
    y0_ = y0 + outer_width
    x1_ = x1 + outer_width / 1.25
    y1_ = y1 + outer_width / 1.25

    pos1 = [0, 0, 0]
    posT = [-34, -15, 20]
    pos_t = lambda x, x1, t: [
        x + x1 * np.sin(np.pi / 2 * t**2.45),
        x
        + x1 * np.sin(np.pi / 2 * t**1.95)
        + (t**0.75 if t < 0.5 else (1 - t) ** 0.75) * 35
        + t * -55 * np.exp(-5 * t**1.75),
        x
        + x1 * (np.sin(np.pi / 2 * t**0.90))
        + (t * -20 * np.exp(-5 * (t) ** 1.75) if t > 0.5 else 0)
        + (t * -20 * np.exp(-5 * (t) ** 4) if t > 0.75 else 0),
    ]

    rot1 = [0, 0, 0]
    rotT = [0, -30, 70]
    rot_t = lambda x, x1, t: [x + x1 * t**1, x + x1 * t**1.5, x + x1 * t**1]
    return make_tubbing(
        pos1, posT, pos_t, rot1, rotT, rot_t, x0, x0_, y0, y0_, x1, x1_, y1, y1_, steps
    )


def make_right_tubbing(x0, y0, outer_width, steps):
    x1 = 12 - outer_width
    y1 = 30 - outer_width

    x0_ = x0 + outer_width
    y0_ = y0 + outer_width
    x1_ = x1 + outer_width / 1.25
    y1_ = y1 + outer_width / 1.25

    pos1 = [0, 0, 0]
    posT = [-28, 1.5, 20]
    pos_t = lambda x, x1, t: [
        x + x1 * np.sin(np.pi / 2 * t**2.45),
        x
        + x1 * np.sin(np.pi / 2 * t**1.95)
        + np.sin(-np.pi * t) * 10
        + t * 35 * np.exp(-6.5 * t**2.5),
        x
        + x1 * np.sin(np.pi / 2 * t**0.925)
        + (t * -20 * np.exp(-5 * (t) ** 1.75) if t > 0.5 else 0)
        + (t * -10 * np.exp(-5 * (t) ** 4) if t > 0.75 else 0),
    ]

    rot1 = [0, 0, 0]
    rotT = [0, -30, -30]
    rot_t = lambda x, x1, t: [x + x1 * t**1, x + x1 * t**1.5, x + x1 * t**1]
    return make_tubbing(
        pos1, posT, pos_t, rot1, rotT, rot_t, x0, x0_, y0, y0_, x1, x1_, y1, y1_, steps
    )


def make_plate():
    plate = s.translate([-7.5, 0, 0])(s.cube([55, 5, 45]))
    screw = s.up(5)(s.cylinder(h=10, d=3.25, center=True, _fn=25))
    screw_head = s.up(1.5)(s.cylinder(h=3.25, d=6, center=True, _fn=25))
    screw_hole = s.union()(screw, screw_head)
    screw_hole = s.rotate([-90, 0, 0])(screw_hole)
    screw_holes = s.union()(
        s.translate([4.25, 0, 40.75])(screw_hole),
        s.translate([40, 0, 5.83])(screw_hole),
    )
    plate = s.difference()(plate, screw_holes)
    plate_clearance_cutter = s.translate(-30, 5, 0)(s.cube(100, 100, 100))
    return plate, screw_holes, plate_clearance_cutter


def make_shape():
    # tubing parameters
    steps = 5
    x0 = 22.5 + 0.5
    y0 = 16.5 + 0.5
    outer_width = 6

    # fan coupling
    fan_adapter = s.difference()(
        s.cube([30, 23.5, 14], center=True),  # outer
        s.cube([26 + 0.25, 19.5 + 0.5, 15], center=True),  # inner
        s.translate([-13, 0, 3])(  # front notch
            s.cube([5, 3.3, 10], center=True)
        ),
        s.translate([0, 0, 10])(  # oblique cut
            s.rotate([0, 25, 0])(s.cube([40, 40, 10], center=True))
        ),
    )
    # fan inner perimeter
    fan_adapter = s.union()(
        fan_adapter,
        s.translate([0, 0, -5.5])(
            s.difference()(
                s.cube([26 + 0.25, 19.5 + 0.5, 3], center=True),  # inner
                s.cube([x0, y0, 4], center=True),
            ),  # inner
        ),
    )
    # screw attachments
    screw_hole = s.rotate([90, 0, 0])(s.cylinder(h=30, d=4.5, center=True, _fn=_FN))
    fan_adapter = s.union()(
        fan_adapter,
        # vertical
        s.translate([-10, 0, 25])(
            s.difference()(
                s.cube([8, 23.5, 40], center=True),
                s.cube([9, 19.5 + 0.5, 41], center=True),
                s.translate([0, 0, 16])(screw_hole),
            )
        ),
        # horizontal
        s.translate([13.5, 0, -3])(
            s.difference()(
                s.union()(
                    s.cube([50, 23.5, 8], center=True),
                    s.translate([21, 0, 6])(s.cube([8, 23.5, 7], center=True)),
                ),
                s.cube([51, 19.5 + 0.5, 20], center=True),
                s.translate([21, 0, 5.5])(screw_hole),
            )
        ),
    )
    fan_adapter = s.translate([0, 0, 7])(fan_adapter)

    tube, inner_cut_left = make_left_tubbing(x0, y0, outer_width, steps)
    rot = lambda sh: s.rotate([180, 0, 0])(sh)
    piece = rot(tube)
    inner_cut_left = rot(inner_cut_left)
    adapter_5020_left = s.union()(piece, fan_adapter)
    trans = lambda sh: s.translate([5, -14, 11])(s.rotate([0, 0, -90])(sh))
    adapter_5020_left = trans(adapter_5020_left)
    inner_cut_left = trans(inner_cut_left)

    plate, screw_hole, plate_clearance_cutter = make_plate()
    tube, inner_cut_right = make_right_tubbing(x0, y0, outer_width, steps)
    rot = lambda sh: s.rotate(180, 0, 0)(sh)
    adapter_5020_right = rot(tube)
    inner_cut_right = rot(inner_cut_right)
    adapter_5020_right = s.union()(adapter_5020_right, fan_adapter)
    trans = lambda sh: s.translate([41, -14, 11])(s.rotate([0, 0, -90])(sh))
    adapter_5020_right = trans(adapter_5020_right)
    inner_cut_right = trans(inner_cut_right)
    screw_cut = s.translate([40, -15, 6])(
        s.rotate([90, 0, 0])(s.cylinder(r=3, h=35, _fn=25, center=True))
    )
    # adapter_5020_right = s.difference()(adapter_5020_right, screw_cut)
    # duct = s.difference()(
    #     s.import_stl("./X2_Fan_Mod_Vibe.stl"),
    #     s.translate([-6.5, -25, -10])(s.cube([61, 25, 35], center=False)),
    #     # left tubbing cut
    #     s.translate([-9.65, -20, -5])(
    #         s.rotate([0, -4, -10])(s.cube([5, 20, 15], center=False))
    #     ),
    #     # right tubbing cut
    #     s.translate([52.5, -21, -5])(
    #         s.rotate([0, 4, 10])(s.cube([5, 20, 15], center=False))
    #     ),
    #     # bottom
    #     s.translate([55, 35, -19.6])(s.cube([20, 20, 10], center=True)),
    # )
    # piece = s.union()(adapter_5020_left, plate, adapter_5020_right, duct)
    piece = s.union()(adapter_5020_left, plate, adapter_5020_right)
    piece = s.difference()(
        piece,
        inner_cut_right,
        inner_cut_left,
        screw_cut,
        screw_hole,
        plate_clearance_cutter,
    )

    # extruder = s.translate(30, 25, -10)(s.cylinder(d=5, h=10, center=True))
    # piece = s.union()(piece, extruder)
    # piece = s.difference()(piece, s.translate([-5,-100,-100])(s.cube([57,200,200], center=False)))
    return piece


if __name__ == "__main__":
    piece = make_shape()
    s.scad_render_to_file(piece, "5020_dual_duct.scad")
# %%
