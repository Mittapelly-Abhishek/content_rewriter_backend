from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import RewriteHistory
from .serializers import RewriteHistorySerializer, RegisterSerializer
from .utils import rewrite_content, speech_to_text
from .exports import generate_pdf


# -------------------------------
# REGISTER USER
# -------------------------------
@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response({
            "status": "success",
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

   

# -------------------------------
# LOGIN (EMAIL BASED)
# -------------------------------
@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({
            "status": "error",
            "message": "Email and password are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Invalid email or password"
        }, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({
            "status": "error",
            "message": "Invalid email or password"
        }, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response = Response({
        "status": "success",
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    }, status=status.HTTP_200_OK)

    #  Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,   # True in production (HTTPS)
        samesite="Lax"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax"
    )

    return response



# -------------------------------
# AI REWRITE CONTENT
# -------------------------------
 
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rewrite_view(request):
    text = request.data.get("text")
    tone = request.data.get("tone", "formal")
    language = request.data.get("language", "english")

    if not text:
        return Response({
            "status": "error",
            "message": "Text is required"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        rewritten = rewrite_content(text, tone, language)

        return Response({
            "status": "success",
            "original_text": text,
            "rewritten_text": rewritten,
            "tone": tone,
            "language": language
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------------------------------
# SAVE HISTORY (OPTIONAL MANUAL)
# -------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_history_view(request):

    original_text = request.data.get("original_text")
    rewritten_text = request.data.get("rewritten_text")
    tone = request.data.get("tone", "formal")
    language = request.data.get("language", "english")

    if not original_text or not rewritten_text:
        return Response({
            "status": "error",
            "message": "Original and rewritten text are required"
        }, status=400)

    item = RewriteHistory.objects.create(
        user=request.user,
        original_text=original_text,
        rewritten_text=rewritten_text,
        tone=tone,
        language=language
    )

    serializer = RewriteHistorySerializer(item)

    return Response({
        "status": "success",
        "data": serializer.data
    }, status=201)

   
    
# -------------------------------
# LIST HISTORY
# -------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_history_view(request):
    items = RewriteHistory.objects.filter(user=request.user).order_by("-created_at")
    serializer = RewriteHistorySerializer(items, many=True)

    return Response({
        "status": "success",
        "data": serializer.data
    })


# -------------------------------
# DELETE HISTORY
# -------------------------------
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_history_view(request, pk):
    try:
        item = RewriteHistory.objects.get(pk=pk, user=request.user)
        item.delete()

        return Response({
            "status": "success",
            "message": "Deleted successfully"
        })

    except RewriteHistory.DoesNotExist:
        raise Http404


# -------------------------------
# EXPORT PDF
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

