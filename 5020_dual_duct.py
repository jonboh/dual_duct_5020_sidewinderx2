import numpy as np
import solid2 as s


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


def make_left_tubbing():
    x1 = 18.25 - 2 * outer_width
    y1 = 11.25 - 2 * outer_width

    x0_ = x0 + outer_width
    y0_ = y0 + outer_width
    x1_ = x1 + outer_width
    y1_ = y1 + outer_width

    pos1 = lambda t: [
        0,
        -13.5 * np.cos(np.pi / 2 * t**1.75),
        10.75 * np.sin(np.pi / 2 * t**1.35),
    ]
    rot1 = lambda t: [-85 * t**2, 1.5 * t**2.5, 10 * t**2.5]
    union_block = s.translate([-15, -25, -2.5])(  # block
        s.hull()(
            s.translate([0, 6.5, 2.5])(s.cube([15, 14.5, 10], center=False)),
            s.translate([0, 2, 2])(
                s.rotate([60, 0, 0])(s.cube([15, 10, 2], center=False))
            ),
        )
    )
    outer = s.union()(
        chained_hull(
            [
                s.translate(pos1(t))(
                    s.rotate(rot1(t))(
                        s.translate([-4.5 * t, 0, 0])(
                            section(
                                x0_ * (1 - t) + x1_ * t,
                                y0_ * (1 - t) + y1_ * t,
                                1.7 + 8 * (1 - t) ** 4,
                                steps,
                                1,
                            )
                        )
                    )
                )
                for t in map(lambda x: x / steps, range(steps + 1))
            ]
        ),
        union_block,
    )

    inner = chained_hull(
        [
            s.translate(pos1(t))(
                s.rotate(rot1(t))(
                    s.translate([-4.5 * t, 0, 0])(
                        section(
                            x0 * (1 - t) + x1 * t,
                            y0 * (1 - t) + y1 * t,
                            1.7 + 8 * (1 - t) ** 3,
                            steps,
                            1.25,
                        )
                    )
                )
            )
            for t in map(lambda x: x / steps, range(steps + 1))
        ]
    )

    piece = s.rotate([180, 0, 0])(
        s.translate([-0.6, 13.5, 0])(s.difference()(outer, inner))
    )

    adapter_5020 = s.union()(piece, fan_adapter)

    return adapter_5020


def make_right_tubbing():
    x1 = 18.35 - 2 * outer_width
    y1 = 11 - 2 * outer_width

    x0_ = x0 + outer_width
    y0_ = y0 + outer_width
    x1_ = x1 + outer_width
    y1_ = y1 + outer_width

    pos1 = lambda t: [
        0,
        -13.5 * np.cos(np.pi / 2 * t**1.75),
        10.15 * np.sin(np.pi / 2 * t**1.35),
    ]
    rot1 = lambda t: [-85 * t**2, 1.5 * t**2.5, 10 * t**2.5]
    union_block = s.translate([-15, -25, -2.5])(  # block
        s.hull()(
            s.translate([0, 6.5, 2.5])(s.cube([15, 14.5, 10], center=False)),
            s.translate([0, 2, 2])(
                s.rotate([60, 0, 0])(s.cube([15, 10, 2], center=False))
            ),
        )
    )
    outer = s.union()(
        chained_hull(
            [
                s.translate(pos1(t))(
                    s.rotate(rot1(t))(
                        s.translate([-4.5 * t, 0, 0])(
                            section(
                                x0_ * (1 - t) + x1_ * t,
                                y0_ * (1 - t) + y1_ * t,
                                1.7 + 8 * (1 - t) ** 4,
                                steps,
                                1,
                            )
                        )
                    )
                )
                for t in map(lambda x: x / steps, range(steps + 1))
            ]
        ),
        union_block,
    )

    inner = chained_hull(
        [
            s.translate(pos1(t))(
                s.rotate(rot1(t))(
                    s.translate([-4.5 * t, 0, 0])(
                        section(
                            x0 * (1 - t) + x1 * t,
                            y0 * (1 - t) + y1 * t,
                            1.7 + 8 * (1 - t) ** 3,
                            steps,
                            1.25,
                        )
                    )
                )
            )
            for t in map(lambda x: x / steps, range(steps + 1))
        ]
    )

    piece = s.rotate([180, 0, 0])(
        s.translate([1, 14.25, 0])(s.difference()(outer, inner))
    )

    adapter_5020 = s.union()(piece, fan_adapter)

    return adapter_5020


if __name__ == "__main__":
    # tubing parameters
    steps = 30
    x0 = 22.5 + 0.5
    y0 = 16.5 + 0.5
    outer_width = 2.5

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
    screw_hole = s.rotate([90, 0, 0])(s.cylinder(h=30, d=4.5, center=True, _fn=25))
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

    adapter_5020_left = make_left_tubbing()
    adapter_5020_left = s.translate([5, -14, 11])(
        s.rotate([0, 0, -90])(adapter_5020_left)
    )

    adapter_5020_right = s.mirror([0, 1, 0])(make_right_tubbing())
    adapter_5020_right = s.translate([42.5, -14, 11])(
        s.rotate([0, 0, -90])(adapter_5020_right)
    )

    screw_cut = s.translate([40, -15, 6])(
        s.rotate([90, 0, 0])(s.cylinder(2.75, 30, _fn=25, center=True))
    )
    adapter_5020_right = s.difference()(adapter_5020_right, screw_cut)

    duct = s.import_stl("./X2_Fan_Mod_Vibe.stl")
    duct = s.difference()(
        duct,
        s.translate([-6.5, -25, -10])(s.cube([61, 25, 35], center=False)),
        # left tubbing cut
        s.translate([-9.65, -20, -5])(
            s.rotate([0, -4, -10])(s.cube([5, 20, 15], center=False))
        ),
        # right tubbing cut
        s.translate([52.5, -21, -5])(
            s.rotate([0, 4, 10])(s.cube([5, 20, 15], center=False))
        ),
        # bottom
        s.translate([55, 35, -19.6])(s.cube([20, 20, 10], center=True)),
    )
    piece = s.union()(adapter_5020_left, adapter_5020_right, duct)
    # piece = s.difference()(piece, s.translate([-5,-100,-100])(s.cube([57,200,200], center=False)))

    s.scad_render_to_file(piece, "5020_dual_duct.scad")
