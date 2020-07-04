from fullmoon import NextFullMoon
from fullmoon import IsFullMoon

###################################
#	Next Full Moon Examples
###################################

n = NextFullMoon() 

# Iterate through all next full moon from "now"
print(n.next_full_moon())
print(n.next_full_moon())

# Restart from "now"
print(n.reset().next_full_moon())
print(n.next_full_moon())

# Change the origin to 1998-07-12
print(n.set_origin_date_string('1998-07-12').next_full_moon()) # PRINT: 1998-08-07
print(n.next_full_moon()) # PRINT: 1998-09-06		

# Reset the origin to 1998-07-12
n.reset()
print(n.next_full_moon()) # PRINT: 1998-08-07

# Reset the origin to "now"
print(n.set_origin_now().next_full_moon())


###################################
#	Is Full Moon Examples
###################################

i = IsFullMoon()

# Check if "now" if full moon
print(i.is_full_moon())

# Check if "1998-07-12" is full moon
print(i.set_date_string('12/07/1992', '%d/%m/%Y').is_full_moon()) # PRINT: False
