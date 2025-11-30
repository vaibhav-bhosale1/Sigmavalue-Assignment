from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Sum
from .models import RealEstateData
from .serializers import RealEstateDataSerializer
import csv
from django.http import HttpResponse

class ChatAnalysisView(APIView):
    def post(self, request):
        user_query = request.data.get('query', '').lower()
        
        # 1. Identify the location from the query
        # We get all unique locations from DB to check against user query
        all_locations = RealEstateData.objects.values_list('final_location', flat=True).distinct()
        
        target_location = None
        for loc in all_locations:
            if loc.lower() in user_query:
                target_location = loc
                break
        
        # Default if no specific location found, just show everything (or handle error)
        if not target_location:
            return Response({
                "response": "I couldn't find a specific location in your query. Please mention a location like 'Wakad', 'Aundh', or 'Akurdi'.",
                "chart_data": [],
                "table_data": []
            })

        # 2. Fetch Data for that location
        data = RealEstateData.objects.filter(final_location__iexact=target_location).order_by('year')
        serializer = RealEstateDataSerializer(data, many=True)
        
        # 3. Generate Chart Data (Price & Sales Trends)
        chart_data = []
        for entry in data:
            chart_data.append({
                "year": entry.year,
                "price": entry.flat_weighted_avg_rate,  # Tracking Flat prices
                "sales": entry.total_sales_igr        # Tracking Sales Volume
            })

        # 4. Generate a "Mock" LLM Summary
        # We calculate real stats to make the summary sound intelligent
        avg_price = data.aggregate(Avg('flat_weighted_avg_rate'))['flat_weighted_avg_rate__avg']
        total_supply = data.aggregate(Sum('total_units'))['total_units__sum']
        latest_year = data.last()
        
        summary = (
            f"Here is the analysis for **{target_location}**.\n\n"
            f"Over the recorded years, the average flat price in this area is approximately "
            f"**₹{avg_price:,.2f} / sqft**.\n"
            f"We have tracked a total supply of **{total_supply} units** across recent years. "
            f"In {latest_year.year}, the prevailing rate for flats was between {latest_year.flat_prevailing_rate_range}."
        )

        # 5. Return everything
        return Response({
            "response": summary,
            "chart_data": chart_data,
            "table_data": serializer.data
        }, status=status.HTTP_200_OK)
        

class DownloadAnalysisView(APIView):
    def get(self, request):
        # Get the location from the URL query parameters (e.g., ?location=Wakad)
        location = request.query_params.get('location')
        
        if not location:
            return Response({"error": "Location parameter is required"}, status=400)

        # Create the CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{location}_Analysis.csv"'

        writer = csv.writer(response)
        # Write CSV Header
        writer.writerow(['Year', 'Location', 'City', 'Total Sales', 'Avg Price (Flat)', 'Supply (Units)', 'Prevailing Rate Range'])

        # Fetch Data
        data = RealEstateData.objects.filter(final_location__iexact=location).order_by('year')
        
        # Write Data Rows
        for entry in data:
            writer.writerow([
                entry.year, 
                entry.final_location, 
                entry.city, 
                entry.total_sales_igr, 
                entry.flat_weighted_avg_rate, 
                entry.total_units,
                entry.flat_prevailing_rate_range
            ])

        return response