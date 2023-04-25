import uuid

async def getToken():
   return str( uuid.uuid4() )
