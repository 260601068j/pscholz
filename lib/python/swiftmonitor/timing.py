from swiftmonitor import observation, events2dat
from fluxtool import rms_estimator
import sys

execute = observation.timed_execute

def prepfold(datfile,parfile,nbins):
  """
    Folds pulsar using prepfold with a par file.
  """
  cmd = 'prepfold -timing -par %s -n %d %s' % (parfile, nbins, datfile)
  execute(cmd)

def pulsed_flux(profile, twocycles=True, harmonics=5):
  """
  Determine the RMS pulsed flux and pulsed fraction using Anne Archibald's 
    fluxtool. 
    Takes a profile with 3 columns (bin number, counts, error) as input.
    Returns a tuple of pulsed flux, pulsed flux error, pulsed fraction,
    and pulsed fraction error.
  """

  if twocycles:
    histogram = profile[:,1]
    uncertainties = profile[:,2]
    if (len(histogram)%2==0 and 
      all(histogram[:len(histogram)//2]==
	     histogram[len(histogram)//2:])):
      sys.stderr.write("Warning: profile appears to contain two cycles\n")
  else:
    histogram = profile[:,1]
    uncertainties = profile[:,2]
    if len(histogram)%2==1:
      parser.error("Profile was supposed to contain two cycles but has odd length")
    if not all(histogram[:len(histogram)//2]==
	     histogram[len(histogram)//2:]):
      sys.stderr.write("Warning: profile does not appear to contain two cycles\n")
    uncertainties = uncertainties[:len(histogram)//2]    
    histogram = histogram[:len(histogram)//2]    

  total_flux = mean(histogram)

  rms_value, rms_uncertainty = rms_estimator(harmonics)(histogram, uncertainties)

  print "RMS pulsed flux:            \t%#0.7g\t+/-\t%#0.7g" % (rms_value, rms_uncertainty)
  print "RMS pulsed fraction:        \t%#0.7g\t+/-\t%#0.7g" % (rms_value/total_flux, rms_uncertainty/total_flux)
  
  return (rms_value, rms_uncertainty, rms_value/total_flux, rms_uncertainty/total_flux)
  

def get_TOA(datfile, template )
  cmd = 'get_TOAs.py -e -f -t %s %s' % (template, datfile) 
  execute(cmd)
