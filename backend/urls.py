from django.urls import path
from backend.views import ImgActions


urlpatterns = [
    path('seg_single_image/', ImgActions.as_view({'post': 'seg_single_image'})),
    path('upload_batch_image/', ImgActions.as_view({'post': 'upload_batch_image'})),
    path('seg_single_image_from_db/', ImgActions.as_view({'post': 'seg_single_image_from_db'})),
    path('seg_single_image_from_to_db/', ImgActions.as_view({'post': 'seg_single_image_from_to_db'})),
    path('get_all_image/', ImgActions.as_view({'post': 'get_all_image'})),
    path('get_segmented_images_for_image/', ImgActions.as_view({'post': 'get_segmented_images_for_image'})),

    
]
