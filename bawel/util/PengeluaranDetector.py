import re

from bawel.util.ImageProcessor import ImageProcessor


class PengeluaranDetector(object):
    def __init__(self, imagePath):
        self.IP = ImageProcessor()
        self.imagePath = imagePath

    def checkForTotal(self):
        totalCandidate = float()
        keyWordForTotal = ["jumlah", "total", "RP"]

        if (self.IP.process_image(self.imagePath)):
            temp = self.IP.process_image(self.imagePath)
            lines = temp.splitlines()

            for line in lines:
                for key in keyWordForTotal:
                    searchSpended = re.compile(
                        r'{0}\D*(\d+\.+\d+|\d+).*'.format(key), flags=re.IGNORECASE)
                    spended = searchSpended.findall(line)
                    if (spended):
                        for spent in spended:
                            spent = float(spent)
                        totalCandidate = max(spended)
                        break

            if totalCandidate == 0:
                searchSpended = re.compile(
                    r'\D*(\d+[\.,]+\d+).*', flags=re.IGNORECASE)
                spended = searchSpended.findall(line)

                if (spended):
                    for spent in spended:
                        spent = float(spent)
                        totalCandidate = max(spended)

            return (str(totalCandidate))

# PD = PengeluaranDetector("/home/gazandic/5845125959350.jpg")
# fl = str(PD.checkForTotal())
# print(fl)
