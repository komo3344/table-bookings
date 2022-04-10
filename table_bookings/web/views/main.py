import logging

from django.db.models import Avg
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .service.search import RestaurantSearch
from ..models import Recommendation, Restaurant

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        recommendations = Recommendation.objects.filter(visible=True).order_by('sort') \
                              .select_related('restaurant').all()[:4]
        latest = Restaurant.objects.order_by('-created_at')[:4]
        hottest = Restaurant.objects.annotate(average_ratings=Avg('review__ratings')) \
                      .filter(average_ratings__gte=0).order_by('-average_ratings')[:4]

        logger.info('recommendations: %d', len(recommendations))

        return {
            'recommendation': recommendations,
            'latest': latest,
            'hottest': hottest
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
