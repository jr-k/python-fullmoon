import math
import time as tt
from datetime import datetime

class IsFullMoon():
	ASTRONOMICAL_EPOCH = 2444238.5 # 1980 January 0.0
	ELONGE = 278.833540 # ecliptic longitude of the Sun at epoch 1980.0
	ELONGP = 282.596403 # ecliptic longitude of the Sun at perigee
	ECCENT = 0.016718 # eccentricity of Earth's orbit
	SUNSMAX =  1.495985e8 # semi-major axis of Earth's orbit, km
	SUNANGSIZ =  0.533128 # sun's angular size, degrees, at semi-major axis distance

	# Elements of the Moon's orbit, epoch 1980.0.
	MMLONG = 64.975464 # moon's mean longitude at the epoch
	MMLONGP =  349.383063 # mean longitude of the perigee at the epoch
	MLNODE = 151.950429 # mean longitude of the node at the epoch
	MINC = 5.145396 # inclination of the Moon's orbit
	MECC = 0.054900 # eccentricity of the Moon's orbit
	MANGSIZ = 0.5181 # moon's angular size at distance a from Earth
	MSMAX =  384401.0 # semi-major axis of Moon's orbit in km
	MPARALLAX = 0.9507 # parallax at distance a from Earth
	SYNMONTH = 29.53050000 # synodic month (new Moon to new Moon)
	
	def __init__(self):
		self.set_date_now()
	
	def set_date_now(self): 
		self._ts = tt.time()
		return self
		
	def set_date_timestamp(self, ts:int):
		self._ts = ts
		return self
	
	def set_date_datetime(self, datetime:datetime):
		self._ts = int(datetime.timestamp())
		return self
	
	def set_date_string(self, datestring:str, format:str = '%Y-%m-%d'):
		self._ts = int(datetime.strptime(datestring, format).timestamp())
		return self

	def is_full_moon(self, ts:int = None):
		today = int(ts if ts else self._ts)
		full_moon = False
		phases = self.phase_list(today)

		for phase in phases:
			if phase > 100:
				moon_data = self.get_phase(phase)
				moon_illum = moon_data[1]
				
				if round(moon_illum) == 1:
					full_moon = True
					break

		return full_moon

	# convert internal date and time to astronomical
	# Julian time (i.e. Julian date plus day fraction)
	def julian_time(self, time:int):
		return (time / 86400.0) + 2440587.5

	# convert Julian day to a UNIX epoch
	def julian_day_to_seconds(self, julian_day:float):#check
		return (julian_day - 2440587.5) * 86400

	# convert Julian date to DateTime object
	def julian_date(self, td:float):
		td += 0.5
		z = math.floor(td)
		f = td - z
		
		if z < 2299161.0:
			a = z
		else:
			alpha = math.floor((z - 1867216.25) / 36524.25)
			a = z + 1 + alpha - math.floor(alpha / 4)

		b = a + 1524
		c = math.floor((b - 122.1) / 365.25)
		d = math.floor(365.25 * c)
		e = math.floor((b - d) / 30.6001)

		dd = b - d - math.floor(30.6001 * e) + f
		mm = e - 1 if e < 14 else e - 13
		yy = c - 4716 if mm > 2 else c - 4715

		dd = int(dd)

		return datetime.strptime(f"{yy}-{str(mm).zfill(2)}-{str(dd).zfill(2)}", '%Y-%m-%d')

	# degrees to radians
	def to_radian(self, degrees:float):
		return degrees * math.pi / 180

	# radians to degrees
	def to_degree(self, radians):
		return radians * 180 / math.pi
	
	# sin converting degrees to radians
	def dsin(self, angle:float):
		return math.sin(self.to_radian(angle))

	# cos converting degrees to radians
	def dcos(self, angle:float):
		return math.cos(self.to_radian(angle))

	def fix_angle(self, angle):
		return angle - (360.0 * math.floor(angle / 360.0))

	def kepler(self, m, ecc):
		epsilon = 1e-6;
		e = m = self.to_radian(m)

		while True:
			delta = e - ecc * math.sin(e) - m;
			e -= delta / (1 - ecc * math.cos(e))
			
			if math.fabs(delta) > epsilon:
				break

		return e

	def get_phase(self, time):
		pdate = self.julian_time(time)
		day = pdate - self.ASTRONOMICAL_EPOCH

		n = self.fix_angle((360 / 365.2422) * day)
		m = self.fix_angle(n + self.ELONGE - self.ELONGP)
		m_rad = self.to_radian(m)

		ec = self.kepler(m, self.ECCENT)
		ec = math.sqrt((1 + self.ECCENT) / (1 - self.ECCENT)) * math.tan(ec / 2)
		ec = 2 * self.to_degree(math.atan(ec))

		lambda_sun = self.fix_angle(ec + self.ELONGP)
		f = (1 + (self.ECCENT * math.cos(self.to_radian(ec)))) / (1 - self.ECCENT**2)
		sun_dist = self.SUNSMAX / f
		sun_ang = f * self.SUNANGSIZ

		ml = self.fix_angle(13.1763966 * day + self.MMLONG)

		mm = self.fix_angle(ml - 0.1114041 * day - self.MMLONGP)

		mn = self.fix_angle(self.MLNODE - 0.0529539 * day)

		ev = 1.2739 * math.sin(self.to_radian(2 * (ml - lambda_sun) - mm))

		ae = 0.1858 * math.sin(m_rad)

		a3 = 0.37 * math.sin(m_rad)

		mmp = mm + ev - ae - a3

		mec = 6.2886 * math.sin(self.to_radian(mmp))

		a4 = 0.214 * math.sin(self.to_radian(2 * mmp))

		lp = ml + ev + mec - ae + a4

		v = 0.6583 * math.sin(self.to_radian(2 * (lp - lambda_sun)))

		lpp = lp + v

		np = mn - 0.16 * math.sin(m_rad)

		y = math.sin(self.to_radian(lpp - np)) * math.cos(self.to_radian(self.MINC))

		x = math.cos(self.to_radian(lpp - np))

		lambda_moon = self.to_degree(math.atan2(y, x))
		lambda_moon += np

		beta_m = self.to_degree(math.asin(math.sin(self.to_radian(lpp - np)) * math.sin(self.to_radian(self.MINC))))

		moon_age = lpp - lambda_sun

		moon_phase = (1 - math.cos(self.to_radian(moon_age))) / 2

		moon_dist = (self.MSMAX * (1 - self.MECC * self.MECC)) / (1 + self.MECC * math.cos(self.to_radian(mmp + mec)))

		moon_d_frac = moon_dist / self.MSMAX
		moon_ang = self.MANGSIZ / moon_d_frac

		moon_par = self.MPARALLAX / moon_d_frac

		pphase = moon_phase
		mage = self.SYNMONTH * (self.fix_angle(moon_age) / 360.0)
		dist = moon_dist
		angdia = moon_ang
		sudist = sun_dist
		suangdia = sun_ang
		mpfrac = self.fix_angle(moon_age) / 360.0

		return [mpfrac, pphase, mage, dist, angdia, sudist, suangdia]

	def true_phase(self, k, phase):
		apcor = 0
		k += phase
		t = k / 1236.85
		t2 = t**2
		t3 = t**3

		pt = 2415020.75933 + (self.SYNMONTH * k) + (0.0001178 * t2) - (0.000000155 * t3) + (0.00033 * self.dsin(166.56 + 132.87 * t - 0.009173 * t2))

		m = 359.2242 + (29.10535608 * k) - (0.0000333 * t2) - (0.00000347 * t3)

		mprime = 306.0253 + (385.81691806 * k) + (0.0107306 * t2) + (0.00001236 * t3)

		f = 21.2964 + (390.67050646 * k) - (0.0016528 * t2) - (0.00000239 * t3)

		if phase < 0.01 or math.fabs(phase - 0.5) < 0.01:
			pt += (0.1734 - 0.000393 * t) * self.dsin(m)
			+ (0.0021 * self.dsin(2 * m ))
			- (0.4068 * self.dsin(mprime))
			+ (0.0161 * self.dsin(2 * mprime))
			- (0.0004 * self.dsin(3 * mprime))
			+ (0.0104 * self.dsin(2 * f))
			- (0.0051 * self.dsin(m + mprime))
			- (0.0074 * self.dsin(m - mprime))
			+ (0.0004 * self.dsin(2 * f + m))
			- (0.0004 * self.dsin(2 * f - m))
			- (0.0006 * self.dsin(2 * f + mprime))
			+ (0.0010 * self.dsin(2 * f - mprime))
			+ (0.0005 * self.dsin(m + 2 * mprime))

			apcor = 1
		elif math.fabs(phase - 0.25) < 0.01 or math.fabs(phase - 0.75) < 0.01:
			pt += (0.1721 - 0.0004 * t) * self.dsin(m)
			+ 0.0021 * self.dsin(2 * m)
			- 0.6280 * self.dsin(mprime)
			+ 0.0089 * self.dsin(2 * mprime)
			- 0.0004 * self.dsin(3 * mprime)
			+ 0.0079 * self.dsin(2 * f)
			- 0.0119 * self.dsin(m + mprime)
			- 0.0047 * self.dsin(m - mprime)
			+ 0.0003 * self.dsin(2 * f + m)
			- 0.0004 * self.dsin(2 * f - m)
			- 0.0006 * self.dsin(2 * f + mprime)
			+ 0.0021 * self.dsin(2 * f - mprime)
			+ 0.0003 * self.dsin(m + 2 * mprime)
			+ 0.0004 * self.dsin(m - 2 * mprime)
			- 0.0003 * self.dsin(2 * m + mprime)

			if phase < 0.5:
				pt += 0.0028 - 0.0004 * self.dcos(m) + 0.0003 * self.dcos(mprime)
			else:
				pt += -0.0028 + 0.0004 * self.dcos(m) - 0.0003 * self.dcos(mprime)

			apcor = 1
			
		return pt
		
	def phase_list(self, date):
		start_date = self.julian_time(date - (3600 * 12))
		end_date = self.julian_time(date + (3600 * 12))
		phases = []

		date_julian = self.julian_date(start_date)
		k = math.floor((date_julian.year + ((date_julian.month - 1) * (1/12)) - 1900) * 12.3685) - 2

		while True:
			k += 1
			defined_phases = [0.0, 0.25, 0.5, 0.75]
			
			for defined_phase in defined_phases:
				d = self.true_phase(k, defined_phase)
				
				if d >= end_date:
					return phases

				if d >= start_date:
					if len(phases) == 0:
						phases.append(math.floor(4 * defined_phase))
					
					phases.append(self.julian_day_to_seconds(d))

