from django.db.models import Q
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from goods.models import Products

"""The function allows to search for products by name and description, performing full-text search and providing
 match highlighting."""

# Define the function q_search with a single parameter query
def q_search(query):
    # Check if the query is a digit and its length is 5 or less
    if query.isdigit() and len(query) <= 5:
        # If so, filter the Products by id
        return Products.objects.filter(id=int(query))

    # Define a search vector over the "name" and "description" fields
    vector = SearchVector("name", "description")
    # Create a search query object with the provided query string
    query = SearchQuery(query)

    # Annotate the Products queryset with a search rank based on the vector and query
    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        # Filter products with a rank grater than 0
        .filter(rank__gt=0)
        # Order the results by rank in descending order
        .order_by("-rank")
    )

    # Annotate the results with a highlighted headline for the "name" field
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            # Start highlighting with a yellow background
            start_sel='<span style="background-color: yellow;">',
            # Stop highlighting
            stop_sel="</span>",
        )
    )
    # Annotate the results with a highlighted headline for the "description" field
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            # Start highlighting with a yellow background
            start_sel='<span style="background-color: yellow;">',
            # Stop highlighting
            stop_sel="</span>",
        )
    )
    # Return the final result set
    return result
    # keywords = [word for word in query.split() if len(word) > 2]

    # q_objects = Q()

    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)

    # return Products.objects.filter(q_objects)
