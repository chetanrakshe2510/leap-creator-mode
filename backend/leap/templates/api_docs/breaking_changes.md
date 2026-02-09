v0.19.0

#3797: Replaced Code.styles_list with Code.get_styles_list()
The styles_list attribute of the Code class has been replaced with a class method Code.get_styles_list(). This method returns a list of all available values for the formatter_style argument of Code.

#3884: Renamed parameters and variables conflicting with builtin functions
To avoid having keyword arguments named after builtin functions, the following two changes were made to user-facing functions:

ManimColor.from_hex(hex=...) is now ManimColor.from_hex(hex_str=...)

Scene.next_section(type=...) is now Scene.next_section(section_type=...)

#3922: Removed inner_radius and outer_radius from Sector constructor
To construct a Sector, you now need to specify a radius (and an angle). In particular, AnnularSector still accepts both inner_radius and outer_radius arguments.

#2476: Improved structure of the mobject module
Arrow tips now have to be imported from manim.mobject.geometry.tips instead of manim.mobject.geometry.

#2387: Refactored BarChart and made it inherit from Axes
BarChart now inherits from Axes, allowing it to use Axes’ methods. Also improves BarChart’s configuration and ease of use.
Added get_bar_labels() to annotate the value of each bar of a BarChart.


