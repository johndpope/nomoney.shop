from django.urls import path
from listing.views import ListingDetailView, \
    ListingCreateView, ListingUpdateView, ListingDeleteView
from category.views import ListingListView


urlpatterns = [
    path('', ListingListView.as_view(), name='listing_list'),

    path(
        '<slug:type>/new/',
        ListingCreateView.as_view(),
        name='listing_create'
        ),

    path(
        '<slug:type>/new/<int:category_pk>/',
        ListingCreateView.as_view(),
        name='category_listing_create'
        ),

    path(
        '<slug:type>/<int:pk>/',
        ListingDetailView.as_view(),
        name='listing_detail'
        ),

    path(
        '<slug:type>/<int:pk>/update/',
        ListingUpdateView.as_view(),
        name='listing_update'
        ),

    path(
        '<slug:type>/<int:pk>/delete',
        ListingDeleteView.as_view(),
        name='listing_delete'
        ),

    # Image Views
    path(
        '<slug:type>/<int:listing_pk>/images/add',
        ListingDetailView.as_view(),
        name='listing_images_add'
        ),

    path(
        '<slug:type>/<int:listing_pk>/images/update',
        ListingDetailView.as_view(),
        name='listing_images_update'
        ),
]
