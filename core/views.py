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

from .utils import rewrite_content, speech_to_text



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
    language = request.data.get("language", "english")  # 👈 NEW

    if not text:
        return Response({"error": "Text is required"}, status=400)

    rewritten = rewrite_content(text, tone, language)

    return Response({"rewritten_text": rewritten, "language": language})


# -------------------------------
# Save History
# -------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_history_view(request):
    data = request.data.copy()
    data["user"] = request.user.id

    # if language not sent from frontend, default english
    if "language" not in data:
        data["language"] = "english"

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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def voice_view(request):
    text = request.data.get("text")

    if not text:
        return Response({"error": "Text is required"}, status=400)

    from .voice import text_to_speech
    audio_file = text_to_speech(text)

    response = HttpResponse(audio_file.read(), content_type="audio/mpeg")
    response["Content-Disposition"] = 'attachment; filename="speech.mp3"'
    return response



    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def speech_to_text_view(request):
    audio = request.FILES.get("audio")
    language = request.data.get("language", "english")

    if not audio:
        return Response({"error": "audio file is required (field name: audio)"}, status=400)

    try:
        text = speech_to_text(audio, language)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    return Response({"text": text, "language": language})





