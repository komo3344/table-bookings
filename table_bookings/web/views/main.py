from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .service.search import RestaurantSearch
from ..models import Recommendation


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        recommendations = Recommendation.objects.select_related('restaurant').filter(visible=True).order_by('sort')[:4]
        return {
            'recommendation': recommendations
        }


class SearchView(TemplateView, RestaurantSearch):
    template_name = 'main/search.html'

    def get_context_data(self, **kwargs):
        page_number = self.request.GET.get('page', '1')
        keyword = self.request.GET.get('keyword')
        category_id = self.request.GET.get('category_id')

        weekday = self.request.GET.get('weekday')
        start_time = self.request.GET.get('start')
        end_time = self.request.GET.get('end')

        return self.search(keyword, category_id, weekday, start_time, end_time, page_number)


class SearchJsonView(View, RestaurantSearch):
    def get(self, request):
        page_number = self.request.GET.get('page', '1')
        keyword = self.request.GET.get('keyword')
        category_id = self.request.GET.get('category_id')

        weekday = self.request.GET.get('weekday')
        start_time = self.request.GET.get('start')
        end_time = self.request.GET.get('end')

        data = self.search(keyword, category_id, weekday, start_time, end_time, page_number)

        results = list(
            map(lambda restaurant: {
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address,
                'image': str(restaurant.main_image.image),
                'category_name': restaurant.category.name
            }, data.get('paging'))
        )
        return JsonResponse(results, safe=False)
