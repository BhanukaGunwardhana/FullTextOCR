from ConnectToBackEnd import *
async def test():
    
    await getUserToken_()
    #await getIntermediateOCR_()
    #await deleteRecordsInIntermediateOCR()
    dict={}
    await sendResponse_()

asyncio.run(test())
#testtextextraction("MicrosoftTeams-image (1).png")