from django.urls import reverse
import os
from django.utils import timezone
import uuid
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, CreateView
from rest_framework import viewsets, status, generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from core import settings
from dashboard.forms import ComplainForm
from dashboard.models import Complain, Dialer, Room, Service
from django.db.models import Q
from django.contrib.staticfiles import finders
from dashboard.serializers import ComplainSerializer, ExtensionSerializer, FoodCategoriesSerializer, FoodItemsSerializer, FoodOrdersSerializer, FoodSubCategoriesSerializer, PhoneDialerSerializer, ServiceSerializer, SubCategoriesSerializer
from stores.models import Cart, Category, Item, Order, OrderItem, Price, ServiceCart, ServiceOrder, ServiceOrderItem, SubCategory
from stores.serializers import CartItemSerializer, CartSerializer, CustomOrderSerializer, GetServiceCartSerializer, ItemSerializer, OrderSerializer, ServiceCartSerializer, ServiceOrderSerializer, ServiceOrdersSerializer, ServiceUpdateOrderSerializer, UpdateOrderSerializer
from django.http import HttpResponseRedirect

# Create your views here.
def showFirebaseJS(request):
    
    file_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'firebase-messaging-sw.js')
    with open(file_path, 'r') as file:
        js_content = file.read()

    return HttpResponse(js_content, content_type='application/javascript')

class NotFoundPageView(TemplateView):    
    template_name = 'pages/page-404.html'


class ModulesViewPage(TemplateView):
    template_name = "modules/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def filterItemByCategories(user, categories=None, sub_category=None, item_type=None, search=None):
    items = []
    if sub_category:
        new_item = {}
        base_query = Q(user=user, sub_category=sub_category)
        if item_type:
           if item_type == "Day Deal":
               base_query &= Q(prices__sell_price__isnull=False)
           else:
               base_query &= Q(item_type=item_type)
            
        filtered_items = Item.objects.filter(base_query).distinct()
            
        if filtered_items.exists():
           new_item['items'] = FoodItemsSerializer(filtered_items, many=True).data
           items.append(new_item)
    else:
        for item_category in categories:
            new_item = {'category': item_category.name}
    
            base_query = Q(user=user, category=item_category)
            
            if search:
                base_query &= Q(title__icontains=search)
            elif item_type:
                if item_type == "Day Deal":
                    base_query &= Q(prices__sell_price__isnull=False)
                else:
                    base_query &= Q(item_type=item_type)
            
            filtered_items = Item.objects.filter(base_query).distinct()
            
            if filtered_items.exists():
                new_item['items'] = FoodItemsSerializer(filtered_items, many=True).data
                items.append(new_item)
                
    return items


class FoodsPageView(TemplateView):
    template_name = "modules/foods_menu.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('room_token')
        if pk:
           try:
               room = Room.objects.get(room_token=pk)
           except Room.DoesNotExist:
               raise Http404("Store does not exist.")
           # context['total_users'] = User.objects.all().count()
        else:
            raise Http404("Store does not exist.")
        
        try:
            bar_enabled = Category.objects.filter(user=room.user, name="Bar").exists();
        except Category.DoesNotExist:
            bar_enabled = False
        context['bar_enabled'] = bar_enabled
        
        return context
        
        
    
    
class HomeViewPage(TemplateView):
    # model = Category
    template_name = "navs/home/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_filter = self.request.GET.get('category')
        sub_category_filter = self.request.GET.get('sub_category')
        item_type = self.request.GET.get('item_type')
        get_sub_category = None
        search = self.request.GET.get('q')
        pk = self.kwargs.get('room_token')
        if pk:
           try:
               room = Room.objects.get(room_token=pk)
           except Room.DoesNotExist:
               raise Http404("Store does not exist.")
           # context['total_users'] = User.objects.all().count()
        else:
            raise Http404("Store does not exist.")
        
        get_categories = Category.objects.filter(user=room.user).exclude(name__in=["Bar"]);
        # Filter Item by Sub Category 
        if sub_category_filter:
            try:
               get_sub_category = SubCategory.objects.filter(name=sub_category_filter)
               if item_type:
                   items = filterItemByCategories(room.user, sub_category=get_sub_category[0], item_type=item_type)
               else:
                   items = filterItemByCategories(room.user, sub_category=get_sub_category[0])
            except SubCategory.DoesNotExist:
               items = filterItemByCategories(room.user, get_categories)
               
        # Filter Item by Category 
        elif category_filter:
           try:
               category = Category.objects.filter(user=room.user, name=category_filter).exclude(name__in=["Bar"])
               get_sub_category = SubCategory.objects.filter(category=category[0])
               if item_type:
                   items = filterItemByCategories(room.user, category, item_type=item_type)
               else:
                   items = filterItemByCategories(room.user, category)
           except Category.DoesNotExist:
               items = filterItemByCategories(room.user, get_categories)
        
        #Filter by Item Type
        elif item_type:
                items = filterItemByCategories(room.user, categories=get_categories, item_type=item_type)
        # Filter Item By Search
        elif search:
            items = filterItemByCategories(room.user, get_categories, search=search)
        else:
            items = filterItemByCategories(room.user, get_categories)
                     
        
        get_cart_items = Cart.objects.filter(room=room)
        amounts = sum(item.price * item.quantity for item in get_cart_items)
        
        context['categories'] = FoodCategoriesSerializer(get_categories.exclude(name__in=["Bar", "Veg", "Non Veg"]), many=True).data    
        context['sub_categories'] = FoodSubCategoriesSerializer(get_sub_category, many=True).data
        context['items'] = items
        context['room_id'] = room.id
        context['cart_items'] = CartItemSerializer(get_cart_items, many=True).data
        context['total_price'] = amounts
        return context
    
    


class BarPageView(TemplateView):
    # model = Category
    template_name = "navs/home/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_filter = self.request.GET.get('category')
        sub_category_filter = self.request.GET.get('sub_category')
        get_sub_categories = None
        search = self.request.GET.get('q')
        pk = self.kwargs.get('room_token')
        if pk:
           try:
               room = Room.objects.get(room_token=pk)
           except Room.DoesNotExist:
               raise Http404("Store does not exist.")
           # context['total_users'] = User.objects.all().count()
        else:
            raise Http404("Store does not exist.")
        
        get_category = Category.objects.filter(user=room.user, name="Bar");
        # Filter Item by Category 
        if sub_category_filter:
           try:
               get_sub_categories = SubCategory.objects.filter(category=get_category[0], name=sub_category_filter)
               items = filterItemByCategories(room.user, sub_category=get_sub_categories[0])
           except SubCategory.DoesNotExist:
               items = filterItemByCategories(room.user, categories=get_category)
        
        
        # Filter Item By Search
        elif search:
            items = filterItemByCategories(room.user, categories=get_category, search=search)
        
        else:
            get_sub_categories = SubCategory.objects.filter(category=get_category[0]);
            items = filterItemByCategories(room.user, categories=get_category)
                     
        
        get_cart_items = Cart.objects.filter(room=room)
        amounts = sum(item.price * item.quantity for item in get_cart_items)
        
        context['sub_categories'] = FoodSubCategoriesSerializer(get_sub_categories, many=True).data
        context['items'] = items
        context['room_id'] = room.id
        context['cart_items'] = CartItemSerializer(get_cart_items, many=True).data
        context['total_price'] = amounts
        return context



class ProductDetailView(DetailView):
    model = Item
    template_name = 'navs/home/item_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        pk = self.kwargs.get('room_token')
        if pk:
           try:
               room = Room.objects.get(room_token=pk)
           except Room.DoesNotExist:
               raise Http404("Store does not exist.")
        else:
            raise Http404("Store does not exist.")
        
        get_cart_items = Cart.objects.filter(room=room)
        amounts = sum(item.price * item.quantity for item in get_cart_items)
        
        # context['related_products'] = Item.objects.filter(category=product.category).exclude(product_id=product.product_id)[:6]
        context['item'] = ItemSerializer(product, context={'request': self.request}).data
        context['room_id'] = room.id
        context['cart_items'] = CartItemSerializer(get_cart_items, many=True).data
        context['total_price'] = amounts
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Item, id=self.kwargs['item_id'], created_at__lte=timezone.now())




class CartModelView(viewsets.ModelViewSet):
    authentication_classes = [] 
    permission_classes = []
    serializer_class = CartSerializer
    
    def get_queryset(self):
        return Cart.objects.all()
    
    
    def perform_create(self, serializer):
        instance = serializer.save() 
        object_id = instance.id
        return object_id
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_id = self.request.POST.get('item')
        price_id = self.request.POST.get('price')
        room_id = self.request.POST.get('room')
        
        item = Item.objects.get(id=item_id)
        price = 0
        if int(price_id) > 1:
            get_price = Price.objects.get(id=price_id)
            if get_price.sell_price:
                price = get_price.sell_price
            else:
                price = get_price.price
        else:
            get_price = item.prices.first()
            if get_price.sell_price:
                price = get_price.sell_price
            else:
                price = get_price.price
            
        additional_data = {
            'price': price,
        }
        for key, value in additional_data.items():
            serializer.validated_data[key] = value
            
        object_id = self.perform_create(serializer)
        room = Room.objects.get(id=room_id)
        cart_items = Cart.objects.filter(room=room)
        amounts = sum(item.price * item.quantity for item in cart_items)
        extra_data = {
            'id': object_id,
            'total_price': amounts,
            'total_items': cart_items.count(),
        }

        return Response(extra_data, status=status.HTTP_201_CREATED)
    
    
    def destroy(self, request, *args, **kwargs):
        cart_id = self.kwargs['pk']
        instance = self.get_object()
        cart = Cart.objects.get(id=cart_id)
        self.perform_destroy(instance)
        get_cart_items = Cart.objects.filter(room=cart.room)
        amounts = sum(item.price * item.quantity for item in get_cart_items)
        response_data = {
            'total_price': amounts,
            'total_items': get_cart_items.count(),
        }
        return Response(response_data, status=status.HTTP_200_OK)


class OrderModelView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateOrderSerializer
        else:
            return self.serializer_class 
    
    def get_queryset(self):
        return Order.objects.all()
    
    
        
    
class PlaceOrderAPIView(APIView):
    authentication_classes = [] 
    permission_classes = []
    serializer_class = CustomOrderSerializer
    
    def post(self, request, format=None):
        serializer = CustomOrderSerializer(data=request.data)
        if serializer.is_valid():
           get_room = Room.objects.get(id=serializer.data['room'])
           cart_items = Cart.objects.filter(room=get_room)
           if cart_items:
               order_id = str(uuid.uuid4().int & (10**8-1))
               order = Order.objects.create(order_id=order_id, room=get_room)
               order.save()
               total_amount = 0
               for cart in cart_items:
                   item = cart.item
                   quantity = cart.quantity
                   total_amount += cart.price * quantity
                   order_item = OrderItem.objects.create(order=order, item=item, quantity=quantity, price=cart.price)
                   order.items.add(order_item)
                   
               order.total_price = total_amount
               order.save()
               cart_items.delete()
               return Response({"success": "Order has been Placed.", "room_id": get_room.room_token, "order_id": order_id}, status=status.HTTP_201_CREATED)
           else:
               return Response({"error": "Cart is empty"}, status=status.HTTP_401_UNAUTHORIZED)    
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          


class OrderStatusViewPage(TemplateView):
    template_name = "navs/order/order_status.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_token = self.kwargs.get('room_token')
        order_id = self.kwargs.get('order_id')
        if room_token and order_id:
            try:
                order = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                raise Http404("Order does not exist.")
        else:
            raise Http404("Order does not exist.")
        
        context['order'] = FoodOrdersSerializer(order).data
        
        return context
        
    
        
class QRCodeViewPage(TemplateView):
    template_name = "pages/phone.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('room_token')
        if pk:
               try:
                   room = Room.objects.get(room_token=pk)
               except Room.DoesNotExist:
                  raise Http404("Room does not exist.")
        else:
            raise Http404("Room does not exist.")
        
        get_dialers = Dialer.objects.filter(extension__user=room.user)
        context['dialers'] = PhoneDialerSerializer(get_dialers, many=True).data
        context['extension'] = ExtensionSerializer(room.extension).data
        
        return context



class ServicesPageView(TemplateView):
    template_name = "navs/service/services.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('room_token')
        if pk:
               try:
                   room = Room.objects.get(room_token=pk)
               except Room.DoesNotExist:
                  raise Http404("Room does not exist.")
        else:
            raise Http404("Room does not exist.")
        
        get_services = Service.objects.filter(user=room.user);
        
        
        get_cart_items = ServiceCart.objects.filter(room=room)
        amounts = sum(item.service.price * 1 for item in get_cart_items)
        
        context['services'] = ServiceSerializer(get_services, many=True).data
        context['room_id'] = room.id
        context['cart_items'] = GetServiceCartSerializer(get_cart_items, many=True).data
        context['total_price'] = amounts
        return context 


class ComplainCreateView(CreateView):
    permission_required = ''
    template_name = "navs/complain/complain.html"
    model = Complain
    form_class = ComplainForm
    
    
    def get_form_kwargs(self):
        kwargs = super(ComplainCreateView, self).get_form_kwargs()
        pk = self.kwargs.get('room_token')
        if pk:
               try:
                   room = Room.objects.get(room_token=pk)
               except Room.DoesNotExist:
                  raise Http404("Room does not exist.")
        else:
            raise Http404("Room does not exist.")
        kwargs['user'] = room.user
        return kwargs
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('room_token')
        if pk:
               try:
                   room = Room.objects.get(room_token=pk)
               except Room.DoesNotExist:
                  raise Http404("Room does not exist.")
        else:
            raise Http404("Room does not exist.")
        
        context['room_id'] = room.id
        return context
    
    def get_success_url(self):
        return reverse('stores:complaint_detail', args=[self.object.room.room_token, self.object.complain_id])
    

class ComplainDetailsView(TemplateView):
    template_name = "navs/complain/complain_status.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_token = self.kwargs.get('room_token')
        complain_id = self.kwargs.get('complain_id')
        if room_token and complain_id:
            try:
                complain = Complain.objects.get(complain_id=complain_id)
            except Complain.DoesNotExist:
                raise Http404("Complain does not exist.")
        else:
            raise Http404("Complain does not exist.")
        
        context['complain'] = ComplainSerializer(complain).data
        
        return context


"""
Service cart
"""
class ServiceCartModelView(viewsets.ModelViewSet):
    authentication_classes = [] 
    permission_classes = []
    serializer_class = ServiceCartSerializer
    
    def get_queryset(self):
        return ServiceCart.objects.all()
    
    
    def perform_create(self, serializer):
        instance = serializer.save() 
        object_id = instance.id
        return object_id
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        get_qunatity = self.request.POST.get('qunatity')
        get_price = self.request.POST.get('price')
        room_id = self.request.POST.get('room')
        print(get_qunatity)
        new_price = int(get_qunatity) * int(get_price)
        serializer.validated_data['price'] = new_price
        object_id = self.perform_create(serializer)
        room = Room.objects.get(id=room_id)
        cart_items = ServiceCart.objects.filter(room=room)
        amounts = sum(item.service.price * 1 for item in cart_items)
        
        extra_data = {
            'id': object_id,
            'total_price': amounts,
            'total_items': cart_items.count(),
        }

        return Response(extra_data, status=status.HTTP_201_CREATED)
    
    
    def destroy(self, request, *args, **kwargs):
        cart_id = self.kwargs['pk']
        instance = self.get_object()
        cart = ServiceCart.objects.get(id=cart_id)
        self.perform_destroy(instance)
        get_cart_items = ServiceCart.objects.filter(room=cart.room)
        amounts = sum(item.service.price * 1 for item in get_cart_items)
        response_data = {
            'total_price': amounts,
            'total_items': get_cart_items.count(),
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class ServiceOrderPlaceAPIView(APIView):
    authentication_classes = [] 
    permission_classes = []
    serializer_class = CustomOrderSerializer
    
    def post(self, request, format=None):
        serializer = CustomOrderSerializer(data=request.data)
        if serializer.is_valid():
           get_room = Room.objects.get(id=serializer.data['room'])
           cart_items = ServiceCart.objects.filter(room=get_room)
           if cart_items:
               order_id = str(uuid.uuid4().int & (10**8-1))
               order = ServiceOrder.objects.create(order_id=order_id, room=get_room)
               order.save()
               total_amount = 0
               for cart in cart_items:
                   service = cart.service
                   quantity = cart.quantity
                   total_amount += cart.service.price * quantity
                   order_service = ServiceOrderItem.objects.create(order=order, service=service, quantity=quantity, price=cart.price)
                   order.services.add(order_service)
                   
               order.total_price = total_amount
               order.save()
               cart_items.delete()
               return Response({"success": "Order has been Placed.", "room_id": get_room.room_token, "order_id": order_id}, status=status.HTTP_201_CREATED)
           else:
               return Response({"error": "Cart is empty"}, status=status.HTTP_401_UNAUTHORIZED)    
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ServiceOrderStatusViewPage(TemplateView):
    template_name = "navs/service/service_order_status.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_token = self.kwargs.get('room_token')
        order_id = self.kwargs.get('order_id')
        if room_token and order_id:
            try:
                order = ServiceOrder.objects.get(order_id=order_id)
            except ServiceOrder.DoesNotExist:
                raise Http404("Order does not exist.")
        else:
            raise Http404("Order does not exist.")
        
        context['order'] = ServiceOrdersSerializer(order).data
        
        return context
    
class ServiceOrderModelView(viewsets.ModelViewSet):
    serializer_class = ServiceOrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'update':
            return ServiceUpdateOrderSerializer
        else:
            return self.serializer_class 
    
    def get_queryset(self):
        return ServiceOrder.objects.all()   