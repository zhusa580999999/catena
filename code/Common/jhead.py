# Copyright (c) 2012, Adam J. Rossi. All rights reserved. See README for licensing details.
import os
import Utility
import ExecutablePath

class jheadInfo:
    
    def __init__(self, imagePath):
        self._imagePath = imagePath
        self._fillInfo()
        
    def _fillInfo(self):

        for l in Utility.RunCommand("\"%s\" \"%s\"" % (Utility.GetAbsoluteFilePath(__file__, ExecutablePath.EXE_JHead), self._imagePath),
                                           cwd=os.path.split(ExecutablePath.EXE_JHead)[0], printStdout=False, captureCout=True):
            if (len(l.strip())==0): continue
            x = l.split(":")
            self.__dict__[x[0].strip()] = x[1].strip()
            
            
    def GetExposureTime(self):  return self.__dict__["Exposure time"]
    def GetCCDWidth(self):      return self.__dict__["CCD width"]
    def GetFocalLength(self):   return self.__dict__["Focal length"]
    def GetCameraMake(self):    return self.__dict__["Camera make"]
    def GetDateTime(self):      return self.__dict__["Date/Time"]
    def GetCameraMake(self):    return self.__dict__["Camera make"]
    def GetFileName(self):      return self.__dict__["File name"]
    def GetFileDate(self):      return self.__dict__["File date"]
    def GetFocusDistance(self): return self.__dict__["Focus dist."]
    def GetFileSize(self):      return self.__dict__["File size"]
    def GetMeteringMode(self):  return self.__dict__["Metering Mode"]
    def GetFlashUsed(self):     return self.__dict__["Flash used"]
    def GetAperture(self):      return self.__dict__["Aperture"]
    def GetLightSource(self):   return self.__dict__["Light Source"]
    def GetResolution(self):    return self.__dict__["Resolution"]
    def GetCameraModel(self):   return self.__dict__["Camera model"]
    def GetExposureBias(self):  return self.__dict__["Exposure bias"]
    
    def GetFocalLengthMM(self):
        return float(self.GetFocalLength().split("mm")[0].strip())
        
    def GetCCDWidthInMM(self):
        import CCDdatabase
        try:
            makeModel = "%s %s" % (self.GetCameraMake(), self.GetCameraModel())
            return CCDdatabase.Instance.GetCameraCCDWidth(makeModel)
        except:
            return None
        
    def GetXResolution(self):
        return int(self.GetResolution().split("x")[0])
        
    def GetYResolution(self):
        return int(self.GetResolution().split("x")[1])

    def GetFocalPixels(self):
        ccdWidthMM = self.GetCCDWidthInMM()
        if (not ccdWidthMM): return None
        
        xRes = self.GetXResolution()
        yRes = self.GetYResolution()
        
        # NOTE: perl script swaps x/y if aspect ratio is "wrong"
        if (xRes<yRes): t = xRes; xRes = yRes; yRes = t;
        
        focalPixels = xRes * (self.GetFocalLengthMM() / ccdWidthMM)
        return focalPixels

    def __str__(self):
        s = ""
        for k,v in self.__dict__.items():
            s += "%s: %s\n" % (k,v)
        return s

