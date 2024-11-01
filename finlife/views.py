from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Max
from .serializer import DepositOptionsSerializer, DepositProductsSerializer
from .models import DepositProducts, DepositOptions

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests

API_KEY = settings.API_KEY


# 정기예금 상품 목록 데이터를 가져와 정기예금 상품 목록과 옵션 목록을 DB에 저장
@api_view(['GET'])
def save_deposit_products(request):
    URL = 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }

    # 서버 요청을 한 번만 수행
    result_data = requests.get(URL, params=params).json().get('result')
    baseList = result_data.get('baseList')
    optionList = result_data.get('optionList')

    # baseList 저장
    for lst in baseList:
        save_product(lst)

    # optionList 저장
    for lst in optionList:
        save_option(lst)

    return Response({'message': '데이터 저장에 성공하였습니다.'})
    

# GET : 전체 정기예금 상품 목록 반환
# POST : 상품 데이터 저장
@api_view(['GET', 'POST'])
def deposit_products(request):

    
    if request.method == 'GET':
        deposit_products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(deposit_products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# 특정 상품의 옵션 리스트 반환
@api_view(['GET'])
def deposit_products_options(request, fin_prdt_cd):
    # fin_prdt_cd에 해당하는 DepositProducts 객체 조회
    deposit_products = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)

    # 해당 상품의 DepositOptions 역참조
    deposit_options = deposit_products.depositoptions_set.all()

    # 결과가 없다면 404 응답 반환
    if not deposit_options.exists():
        return Response({'error': '해당 금융 상품의 옵션이 없습니다.'}, status=404)

    # 각 옵션을 직렬화하여 반환
    serializer = DepositOptionsSerializer(deposit_options, many=True)
    return Response(serializer.data)


# 가입 기간에 상관없이 최고 금리가 가장 높은 금융 상품과 해당 상품의 옵션 리스트 출력
@api_view(['GET'])
def top_rate(request):
    top_rate_option_id = DepositOptions.objects.aggregate(Max('intr_rate2'))['intr_rate2__max']
    print(top_rate_option_id)
    top_product = DepositProducts.objects.get(pk=top_rate_option_id)

    product_serializer = DepositProductsSerializer(top_product)
    options_serializer = DepositOptionsSerializer(DepositOptions.objects.filter(product=top_product), many=True)
    
    # 응답 데이터 구성
    response_data = {
        'product': product_serializer.data,
        'options': options_serializer.data
    }

    return Response(response_data)

#################################################

def save_product(lst):
    product_data = {
        'fin_prdt_cd': lst.get('fin_prdt_cd'),
        'kor_co_nm': lst.get('kor_co_nm'),
        'fin_prdt_nm': lst.get('fin_prdt_nm'),
        'etc_note': lst.get('etc_note'),
        'join_deny': lst.get('join_deny'),
        'join_member': lst.get('join_member'),
        'join_way': lst.get('join_way'),
        'spcl_cnd': lst.get('spcl_cnd'),
    }

    # 중복 확인 및 저장
    DepositProducts.objects.get_or_create(
        fin_prdt_cd=product_data['fin_prdt_cd'],
        defaults=product_data
    )


def save_option(lst):
    fin_prdt_cd = lst.get('fin_prdt_cd')
    product = DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()

    if product:  # 상품이 존재하는 경우에만 옵션 저장
        option_data = {
            'product': product,
            'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type_nm': lst.get('intr_rate_type_nm'),
            'intr_rate': lst.get('intr_rate') if lst.get('intr_rate') is not None else -1,
            'intr_rate2': lst.get('intr_rate2') if lst.get('intr_rate2') is not None else -1,
            'save_trm': lst.get('save_trm'),
        }

        # 중복 확인 및 저장
        DepositOptions.objects.get_or_create(
            product=product,
            fin_prdt_cd=option_data['fin_prdt_cd'],
            intr_rate_type_nm=option_data['intr_rate_type_nm'],
            save_trm=option_data['save_trm'],
            defaults=option_data
        )