

class Constant(object):
	"""docstring for Constant"""
	def __init__(self, name, value, description, units="units"):
		super(Constant, self).__init__()
		self.name = name
		self.value = value
		self.desc = description
		self.units = units

	def show_help(self):
		fdict = dict(
			NAME=self.name,
			DEFAULT=self.value,
			DESC=self.desc,
			UNITS=self.units
		)
		print("\n[ CONSTANT ]\nCalling: {NAME} = pkg.Constant(\"{NAME}\")\nDefault: {DEFAULT} {UNITS}\nDescription: {DESC}\n".format(**fdict))

soflight = Constant(
	"c",
	3*pow(10,8),
	"Speed Of Light",
	units="m/s"
)
gravConstant = Constant(
	"G",
	6.67*pow(10,-11),
	"Gravitational Constant",
	"m^3/(kg*s^2)"
)
soflight.show_help()
gravConstant.show_help()