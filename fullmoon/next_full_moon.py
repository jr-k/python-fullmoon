import math
import time as tt
from datetime import datetime

class NextFullMoon():

	SYNMONTH = 29.53050000
	
	def __init__(self):
		self._counter = 0
		self._last_set_origin = 0
		self.set_origin_now()
		
	@property
	def counter(self):
		return self._counter
		
	def reset(self):
		self._from_timestamp = self._last_set_origin
		self.reset_counter()
		return self
		
	def reset_counter(self):
		self._counter = 0
		return self
	
	def set_origin_now(self):
		self._from_timestamp = tt.time()
		self._last_set_origin = self._from_timestamp
		return self
		
	def set_origin_timestamp(self, ts:int):
		self._from_timestamp = ts
		self._last_set_origin = self._from_timestamp
		return self
	
	def set_origin_datetime(self, datetime:datetime):
		self._from_timestamp = int(datetime.timestamp())
		self._last_set_origin = self._from_timestamp
		return self
	
	def set_origin_date_string(self, datestring:str, format:str = '%Y-%m-%d'):
		self._from_timestamp = int(datetime.strptime(datestring, format).timestamp())
		self._last_set_origin = self._from_timestamp
		return self
		
	def next_full_moon(self, prevent_update=False):
		self._counter += 1
		time = self._from_timestamp
		full_moon = self.moon_phase(time, 0.5)
		ts = 0
		
		if full_moon < time:
			ts = math.floor(self.moon_phase(time, 0.5, True))
		else:
			ts = math.floor(full_moon)
		
		if not prevent_update:
			self._from_timestamp = ts + 86400
		
		return datetime.fromtimestamp(ts)

	def moon_phase(self, time:int, phase:float, second:bool = False):
		k1k2 = self.time_2k_1_k2(time)

		if not second:
			return self.julian_day_to_seconds(self.true_phase(k1k2[0], phase))

		return self.julian_day_to_seconds(self.true_phase(k1k2[1], phase))

	def time_2k_1_k2(self, time:int):
		start_date = self.julian_time(time)
		a_date = start_date - 45

		date_julian = self.julian_date(a_date)
		k1 = math.floor((date_julian.year + ((date_julian.month - 1) * (1.0 / 12.0)) - 1900) * 12.3685 )
		
		# why using a_date again
		a_date = nt1 = self.mean_phase(a_date, k1)

		while True:
			a_date += self.SYNMONTH
			k2 = k1 + 1
			nt2 = self.mean_phase(a_date, k2)
			
			if nt1 <= a_date and nt2 > start_date:
				break
				
			nt1 = nt2
			k1 = k2

		return [k1, k2]

	def julian_time(self, time:int):
		return (time / 86400.0) + 2440587.5

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


    # Calculates time of the mean new Moon for a given
    # base date. This argument K to this function is the
    # precomputed synodic month index, given by:
    # K = (year - 1900) * 12.3685
    # where year is expressed as a year and fractional year.
	def mean_phase(self, start_date:float, k:int):
		t = (start_date - 2415020) / 365.25 # time in centuries since 1900 January 0.5
		t2 = t**2

		nt1 = 2415020.75933 + self.SYNMONTH * k
		+ 0.0001178 * t2
		- 0.000000155 * t**3
		+ 0.00033 * self.dsin(166.56 + 132.87 * t - 0.009173 * t2)

		return nt1

	def dsin(self, angle:float):
		return math.sin(self.to_radian(angle))

	def dcos(self, angle:float):
		return math.cos(self.to_radian(angle))

	def to_radian(self, degrees:float):
		return degrees * math.pi / 180

	def true_phase(self, k:int, phase:float):
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

	def julian_day_to_seconds(self, julian_day:float):
		return (julian_day - 2440587.5) * 86400
