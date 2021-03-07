from rest_framework.response import Response
class Error(Exception):
    pass
class AppError(Error):
    def __init__(self,message,statuscode):
        self.statuscode = statuscode         
        self.status= 'fail' if statuscode[0]=='4' else 'error'
        self.message = message
        self.isOperational = True
        super().__init__(self.message)


def errorResponse(message,statuscode):
    err= AppError(message,statuscode)
    data={'status':err.status,'message':err.message}
    return Response(data,status=err.statuscode)

