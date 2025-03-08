from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from .models import Document
from .serializers import DocumentSerializer, UserSerializer

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

# Upload Document
class UploadDocumentView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(author=user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Download Document
class DownloadDocumentView(generics.RetrieveAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(author=user)
    
    def get(self, request, pk):
        doc = get_object_or_404(Document, pk=pk, author=self.request.user)
        return FileResponse(doc.file, as_attachment=True, filename=doc.file.name)

# Delete Document
class DeleteDocumentView(generics.DestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(author=user)
    
    def get_object(self):
        doc = get_object_or_404(Document, pk=self.kwargs['pk'], author=self.request.user)
        return doc
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 404:
            return Response({'error': 'Document does not exist'}, status=404)
        return Response({'success': 'Document deleted!'}, status=204)

class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(author=user)

# Edit Document? This may require separate app with focus on pandas library functionalities