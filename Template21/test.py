import groupCounter

counterA = groupCounter.groupCounter()

counterA.readGjfFile(fileName='C9H18_100_r015.gjf', directory='Gjfs', moleculeLabel='test1')
counterA.readGroupTemplate()
counterA.writeDBGCVector(overwrite=False)

counterA.readGjfFile(fileName='C10H22_57_r019.gjf', directory='Gjfs', moleculeLabel='test1')
counterA.readGroupTemplate()
counterA.writeDBGCVector(overwrite=False)