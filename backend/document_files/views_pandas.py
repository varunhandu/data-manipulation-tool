import pandas as pd
import io
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from .models import Document

allowed_docs = ['csv', 'xls', 'xlsx', 'json', 'xml']

def convertFileToDataFrame(file_path, file_type):
    if file_type == 'csv':
        df = pd.read_csv(file_path)
    elif file_type == 'xls' or file_type == 'xlsx':
        df = pd.read_excel(file_path)
    elif file_type == 'json':
        df = pd.read_json(file_path)
    elif file_type == 'xml':
        df = pd.read_xml(file_path)
    else:
        df = None
    return df

def convertDataFrameToBuffer(df, file_type):
    buffer = io.BytesIO()
    if file_type == 'csv':
        df.to_csv(buffer, index=False)
    elif file_type == 'xls' or file_type == 'xlsx':
        df.to_excel(buffer, index=False)
    elif file_type == 'json':
        df.to_json(buffer, orient='records')
    elif file_type == 'xml':
        df.to_xml(buffer)
    else:
        buffer = None

    if buffer is not None:
        buffer.seek(0)

    return buffer

class CreateDataframe(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     doc = get_object_or_404(Document, pk=self.kwargs['pk'], author=self.request.user)
    #     # document = request.FILES.get('file')
    #     if not doc:
    #         return Response({'error': 'No file uploaded'}, status=400)

    def get(self, request, pk):
        # doc = get_object_or_404(Document, pk=self.kwargs['pk'], author=self.request.user)
        doc = get_object_or_404(Document, pk=pk, author=self.request.user)
        if not doc:
            return Response({'error': 'The file does not exist'}, status=400)
        file_path = doc.file.path
        file_type = doc.file_type

        df = convertFileToDataFrame(file_path, file_type)
        
        if df is None:
            return Response({'error': 'File type not supported'}, status=400)

        # Do something with the DataFrame
        # save dataframe in session

        request.session['dataframe'] = df.to_json()
        request.session['file_name'] = doc.file.name
        request.session['file_type'] = doc.file_type
        print('dataframe stored in session')

        return Response({'success': 'DataFrame created!'}, status=200)
    
class ModifyDataframe(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # get dataframe from session
        df_json = request.session['dataframe']
        if not df_json:
            return Response({'error': 'No dataframe in session'}, status=400)

        df = pd.read_json(df_json)
        # modify dataframe


        # save dataframe in session
        request.session['dataframe'] = df.to_json();
        print('dataframe stored in session')
        return Response({'success': 'DataFrame modified!'}, status=200)

class DownloadDataframe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get dataframe from session
        df_json = request.session['dataframe']
        if not df_json:
            return Response({'error': 'No dataframe in session'}, status=400)

        file_type = request.session['file_type']
        
        if file_type == 'json':
            request.session.delete()
            return FileResponse(df_json, as_attachment=True, filename="filtered_" + og_file.file.name)
    
        df = pd.read_json(df_json)
        buffer = convertDataFrameToBuffer(df, file_type)

        content_type = 'text/csv'
        if file_type == 'xls' or file_type == 'xlsx':
            content_type = 'application/vnd.ms-excel'
        elif file_type == 'json':
            content_type = 'application/json'
        elif file_type == 'xml':
            content_type = 'application/xml'

        response = Response(buffer.getvalue(), content_type="text/csv", headers={
            "Content-Disposition": f'attachment; filename="filtered_data.{file_type}"'
        })
        request.session.delete()
        print('filtered file downloaded')
        return response

# Possible improvements:
# use Redis instead of Sessions
# StreamingHTTPResponse to stream the file, avoids memory overflow in larger files