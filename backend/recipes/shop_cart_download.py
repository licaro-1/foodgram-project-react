import io
from django.http import FileResponse
from rest_framework.views import APIView
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .services import _get_ingredients_dictionary_by_user
from rest_framework.permissions import IsAuthenticated


class DownloadCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        shop_cart_list = _get_ingredients_dictionary_by_user(user)
        pdfmetrics.registerFont(
            TTFont('wiguru-13', './Recipes/ttf/wiguru-13.ttf'))
        buffer = io.BytesIO()
        file = canvas.Canvas(buffer)
        file.setFont('wiguru-13', 40)
        line_start = 700
        file.drawString(225, 800, 'FOODGRAM')
        file.setFont('wiguru-13', 27)
        for ingredient, amount in shop_cart_list.items():
            file.drawString(40, line_start, f'{ingredient} — {amount}')
            line_start -= 50
        file.showPage()
        file.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='shop_cart_list.pdf')
