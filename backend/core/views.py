from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from rest_framework_simplejwt.tokens import RefreshToken

from .models import RewriteHistory
from .serializers import RewriteHistorySerializer, RegisterSerializer
from .utils import rewrite_content
from .exports import generate_pdf


# -------------------------------
# Register User
# -------------------------------
@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User registered successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        })

    return Response(serializer.errors, status=400)


# -------------------------------
# AI Rewrite Content
# -------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rewrite_view(request):
    text = request.data.get("text")
    tone = request.data.get("tone", "formal")

    if not text:
        return Response({"error": "Text is required"}, status=400)

    rewritten = rewrite_content(text, tone)

    return Response({"rewritten_text": rewritten})


# -------------------------------
# Save History
# -------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_history_view(request):
    data = request.data.copy()
    data["user"] = request.user.id

    serializer = RewriteHistorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


# -------------------------------
# List User History
# -------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_history_view(request):
    items = RewriteHistory.objects.filter(user=request.user).order_by("-created_at")
    serializer = RewriteHistorySerializer(items, many=True)
    return Response(serializer.data)


# -------------------------------
# Delete History Item
# -------------------------------
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_history_view(request, pk):
    try:
        item = RewriteHistory.objects.get(pk=pk, user=request.user)
        item.delete()
        return Response({"message": "Deleted"})
    except RewriteHistory.DoesNotExist:
        raise Http404


# -------------------------------
# Export PDF
# -------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_pdf_view(request, pk):
    try:
        item = RewriteHistory.objects.get(pk=pk, user=request.user)
    except RewriteHistory.DoesNotExist:
        raise Http404

    pdf = generate_pdf(item.rewritten_text)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="rewrite_{pk}.pdf"'
    return response
