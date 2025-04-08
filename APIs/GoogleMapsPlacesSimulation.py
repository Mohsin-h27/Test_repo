import math
import json
import re
DB = [
    {
        "areaSummary": {
            "contentBlocks": [
                {
                    "content": {
                        "text": "An iconic skyscraper in Midtown Manhattan with sweeping city views.",
                        "languageCode": "en"
                    },
                    "flagContentUri": "https://maps.example.com/flag/empireAreaBlock",
                    "topic": "landmark"
                }
            ],
            "flagContentUri": "https://maps.example.com/flag/empireAreaSummary"
        },
        "userRatingCount": 25000,
        "servesBeer": False,
        "businessStatus": "OPERATIONAL",
        "formattedAddress": "20 W 34th St, New York, NY 10001, USA",
        "currentSecondaryOpeningHours": [
            {
                "nextCloseTime": "2025-03-15T23:00:00Z",
                "openNow": True,
                "nextOpenTime": "2025-03-16T09:00:00Z",
                "periods": [
                    {
                        "open": {
                            "day": 1,
                            "hour": 9,
                            "minute": 0,
                            "date": {"year": 2025, "month": 3, "day": 15}
                        },
                        "close": {
                            "day": 1,
                            "hour": 23,
                            "minute": 0,
                            "date": {"year": 2025, "month": 3, "day": 15}
                        }
                    }
                ],
                "specialDays": [],
                "weekdayDescriptions": [
                    "Mon: 09:00–23:00",
                    "Tue: 09:00–23:00",
                    "Wed: 09:00–23:00",
                    "Thu: 09:00–23:00",
                    "Fri: 09:00–23:00",
                    "Sat: 10:00–22:00",
                    "Sun: Closed"
                ],
                "secondaryHoursType": "VISIT"
            }
        ],
        "pureServiceAreaBusiness": False,
        "servesCoffee": False,
        "delivery": False,
        "takeout": False,
        "iconMaskBaseUri": "https://maps.example.com/icons/empire",
        "containingPlaces": [
            {"name": "Midtown Manhattan", "id": "region_midtown"}
        ],
        "plusCode": {
            "globalCode": "87G8Q2MV+2V",
            "compoundCode": "Q2MV+2V New York, NY"
        },
        "restroom": True,
        "location": {"latitude": 40.748817, "longitude": -73.985428},
        "primaryTypeDisplayName": {"text": "Skyscraper", "languageCode": "en"},
        "utcOffsetMinutes": -300,
        "adrFormatAddress": "ADR: 20 W 34th St, New York, NY 10001, USA",
        "id": "place_empire",
        "evChargeOptions": {
            "connectorAggregation": [],
            "connectorCount": 0
        },
        "googleMapsUri": "https://maps.example.com/place/place_empire",
        "servesBreakfast": False,
        "goodForGroups": True,
        "goodForWatchingSports": False,
        "shortFormattedAddress": "20 W 34th St",
        "liveMusic": False,
        "websiteUri": "https://www.esbnyc.com",
        "photos": [
            {
                "flagContentUri": "https://maps.example.com/flag/empirePhoto1",
                "authorAttributions": [
                    {
                        "displayName": "NYC Photographer",
                        "uri": "https://example.com/nycphotographer",
                        "photoUri": "https://example.com/nycphotographer.jpg"
                    }
                ],
                "googleMapsUri": "https://maps.example.com/photo/empire1",
                "widthPx": 1200,
                "heightPx": 900,
                "name": "places/place_empire/photos/photo_1"
            }
        ],
        "reservable": False,
        "currentOpeningHours": {
            "nextCloseTime": "2025-03-15T23:00:00Z",
            "openNow": True,
            "nextOpenTime": "2025-03-16T09:00:00Z",
            "periods": [
                {
                    "open": {
                        "day": 1,
                        "hour": 9,
                        "minute": 0,
                        "date": {"year": 2025, "month": 3, "day": 15}
                    },
                    "close": {
                        "day": 1,
                        "hour": 23,
                        "minute": 0,
                        "date": {"year": 2025, "month": 3, "day": 15}
                    }
                }
            ],
            "specialDays": [],
            "weekdayDescriptions": [
                "Mon: 09:00–23:00",
                "Tue: 09:00–23:00",
                "Wed: 09:00–23:00",
                "Thu: 09:00–23:00",
                "Fri: 09:00–23:00",
                "Sat: 10:00–22:00",
                "Sun: Closed"
            ],
            "secondaryHoursType": "VISIT"
        },
        "servesVegetarianFood": False,
        "reviews": [
            {
                "googleMapsUri": "https://maps.example.com/review/empire_rev1",
                "authorAttribution": {
                    "displayName": "Travel Guru",
                    "uri": "https://example.com/travelguru",
                    "photoUri": "https://example.com/travelguru.jpg"
                },
                "relativePublishTimeDescription": "3 days ago",
                "publishTime": "2025-03-12T18:00:00Z",
                "flagContentUri": "https://maps.example.com/flag/empire_rev1",
                "rating": 4.7,
                "name": "review_empire_1",
                "text": {"text": "A must-see landmark with incredible views!", "languageCode": "en"},
                "originalText": {"text": "A must-see landmark with incredible views!", "languageCode": "en"}
            }
        ],
        "servesWine": False,
        "goodForChildren": True,
        "internationalPhoneNumber": "+1 212-736-3100",
        "menuForChildren": False,
        "servesCocktails": False,
        "priceLevel": "PRICE_LEVEL_VERY_EXPENSIVE",
        "timeZone": {"id": "America/New_York", "version": "2023a"},
        "servesDessert": False,
        "addressComponents": [
            {
                "shortText": "NYC",
                "types": ["locality", "political"],
                "languageCode": "en",
                "longText": "New York"
            }
        ],
        "viewport": {
            "low": {"latitude": 40.744, "longitude": -73.990},
            "high": {"latitude": 40.752, "longitude": -73.979}
        },
        "rating": 4.7,
        "iconBackgroundColor": "#000000",
        "servesBrunch": False,
        "priceRange": {
            "startPrice": {"units": "100", "nanos": 0, "currencyCode": "USD"},
            "endPrice": {"units": "300", "nanos": 0, "currencyCode": "USD"}
        },
        "primaryType": "skyscraper",
        "attributions": [
            {"provider": "NYC Gov", "providerUri": "https://www1.nyc.gov"}
        ],
        "regularOpeningHours": {
            "nextCloseTime": "2025-03-15T23:30:00Z",
            "openNow": True,
            "nextOpenTime": "2025-03-16T09:00:00Z",
            "periods": [
                {
                    "open": {
                        "day": 1,
                        "hour": 9,
                        "minute": 0,
                        "date": {"year": 2025, "month": 3, "day": 15}
                    },
                    "close": {
                        "day": 1,
                        "hour": 23,
                        "minute": 30,
                        "date": {"year": 2025, "month": 3, "day": 15}
                    }
                }
            ],
            "specialDays": [],
            "weekdayDescriptions": [
                "Mon: 09:00–23:30",
                "Tue: 09:00–23:30",
                "Wed: 09:00–23:30",
                "Thu: 09:00–23:30",
                "Fri: 09:00–23:30",
                "Sat: 10:00–22:00",
                "Sun: Closed"
            ],
            "secondaryHoursType": "VISIT"
        },
        "allowsDogs": False,
        "outdoorSeating": False,
        "dineIn": False,
        "name": "Empire State Building",
        "parkingOptions": {
            "freeStreetParking": False,
            "paidParkingLot": True,
            "freeGarageParking": False,
            "freeParkingLot": False,
            "paidGarageParking": True,
            "paidStreetParking": True,
            "valetParking": False
        },
        "curbsidePickup": False,
        "googleMapsLinks": {
            "reviewsUri": "https://maps.example.com/place/place_empire/reviews",
            "writeAReviewUri": "https://maps.example.com/writeareview?place=place_empire",
            "photosUri": "https://maps.example.com/place/place_empire/photos",
            "directionsUri": "https://maps.example.com/directions?destination=place_empire",
            "placeUri": "https://maps.example.com/place/place_empire"
        },
        "servesDinner": False,
        "regularSecondaryOpeningHours": [],
        "editorialSummary": {
            "text": "An iconic landmark offering panoramic views of New York City.",
            "languageCode": "en"
        },
        "paymentOptions": {
            "acceptsNfc": False,
            "acceptsCreditCards": True,
            "acceptsDebitCards": True,
            "acceptsCashOnly": False
        },
        "generativeSummary": {
            "descriptionFlagContentUri": "https://maps.example.com/flag/genDescEmpire",
            "overviewFlagContentUri": "https://maps.example.com/flag/genOverviewEmpire",
            "description": {
                "text": "A detailed AI-generated description of the Empire State Building.",
                "languageCode": "en"
            },
            "overview": {
                "text": "Panoramic views from one of the world's most famous skyscrapers.",
                "languageCode": "en"
            },
            "references": {
                "places": ["ref_empire_001"],
                "reviews": []
            }
        },
        "fuelOptions": {
            "fuelPrices": []
        },
        "accessibilityOptions": {
            "wheelchairAccessibleParking": True,
            "wheelchairAccessibleRestroom": True,
            "wheelchairAccessibleSeating": False,
            "wheelchairAccessibleEntrance": True
        },
        "types": ["skyscraper", "landmark"],
        "subDestinations": [],
        "displayName": {"text": "Empire State Building", "languageCode": "en-US"},
        "addressDescriptor": {
            "landmarks": [
                {
                    "straightLineDistanceMeters": 100,
                    "types": ["landmark"],
                    "spatialRelationship": "NEAR",
                    "displayName": {"text": "Observation Deck", "languageCode": "en"},
                    "name": "landmark_empire_obs",
                    "placeId": "obs_empire",
                    "travelDistanceMeters": 120
                }
            ],
            "areas": [
                {
                    "name": "Midtown",
                    "containment": "WITHIN",
                    "displayName": {"text": "Midtown Manhattan", "languageCode": "en"},
                    "placeId": "area_midtown"
                }
            ]
        },
        "servesLunch": False,
        "nationalPhoneNumber": "+1 212-736-3100"
    },
    {
        "areaSummary": {
            "contentBlocks": [
                {
                    "content": {
                        "text": "A vast green oasis in the heart of New York City, offering recreational activities and scenic walks.",
                        "languageCode": "en"
                    },
                    "flagContentUri": "https://maps.example.com/flag/centralAreaBlock",
                    "topic": "park"
                }
            ],
            "flagContentUri": "https://maps.example.com/flag/centralAreaSummary"
        },
        "userRatingCount": 12000,
        "servesBeer": False,
        "businessStatus": "OPERATIONAL",
        "formattedAddress": "Central Park, New York, NY, USA",
        "currentSecondaryOpeningHours": [
            {
                "nextCloseTime": "2025-04-01T20:00:00Z",
                "openNow": True,
                "nextOpenTime": "2025-04-01T06:00:00Z",
                "periods": [
                    {
                        "open": {
                            "day": 0,
                            "hour": 6,
                            "minute": 0,
                            "date": {"year": 2025, "month": 4, "day": 1}
                        },
                        "close": {
                            "day": 0,
                            "hour": 20,
                            "minute": 0,
                            "date": {"year": 2025, "month": 4, "day": 1}
                        }
                    }
                ],
                "specialDays": [],
                "weekdayDescriptions": [
                    "Sun: 06:00–20:00",
                    "Mon: 06:00–20:00",
                    "Tue: 06:00–20:00",
                    "Wed: 06:00–20:00",
                    "Thu: 06:00–20:00",
                    "Fri: 06:00–20:00",
                    "Sat: 06:00–20:00"
                ],
                "secondaryHoursType": "VISIT"
            }
        ],
        "pureServiceAreaBusiness": False,
        "servesCoffee": True,
        "delivery": False,
        "takeout": False,
        "iconMaskBaseUri": "https://maps.example.com/icons/centralpark",
        "containingPlaces": [
            {"name": "Manhattan", "id": "region_manhattan"}
        ],
        "plusCode": {
            "globalCode": "87G8Q8QX+2V",
            "compoundCode": "8QX+2V New York, NY"
        },
        "restroom": True,
        "location": {"latitude": 40.7829, "longitude": -73.9654},
        "primaryTypeDisplayName": {"text": "Park", "languageCode": "en"},
        "utcOffsetMinutes": -300,
        "adrFormatAddress": "Central Park, New York, NY, USA",
        "id": "place_central",
        "evChargeOptions": {
            "connectorAggregation": [],
            "connectorCount": 0
        },
        "googleMapsUri": "https://maps.example.com/place/place_central",
        "servesBreakfast": False,
        "goodForGroups": True,
        "goodForWatchingSports": True,
        "shortFormattedAddress": "Central Park",
        "liveMusic": True,
        "websiteUri": "https://www.centralparknyc.org",
        "photos": [
            {
                "flagContentUri": "https://maps.example.com/flag/centralPhoto1",
                "authorAttributions": [
                    {
                        "displayName": "Park Photographer",
                        "uri": "https://example.com/parkphotog",
                        "photoUri": "https://example.com/parkphotog.jpg"
                    }
                ],
                "googleMapsUri": "https://maps.example.com/photo/central1",
                "widthPx": 1024,
                "heightPx": 768,
                "name": "places/place_central/photos/photo_1"
            }
        ],
        "reservable": False,
        "currentOpeningHours": {
            "nextCloseTime": "2025-04-01T20:00:00Z",
            "openNow": True,
            "nextOpenTime": "2025-04-01T06:00:00Z",
            "periods": [
                {
                    "open": {
                        "day": 0,
                        "hour": 6,
                        "minute": 0,
                        "date": {"year": 2025, "month": 4, "day": 1}
                    },
                    "close": {
                        "day": 0,
                        "hour": 20,
                        "minute": 0,
                        "date": {"year": 2025, "month": 4, "day": 1}
                    }
                }
            ],
            "specialDays": [],
            "weekdayDescriptions": [
                "Sun: 06:00–20:00",
                "Mon: 06:00–20:00",
                "Tue: 06:00–20:00",
                "Wed: 06:00–20:00",
                "Thu: 06:00–20:00",
                "Fri: 06:00–20:00",
                "Sat: 06:00–20:00"
            ],
            "secondaryHoursType": "VISIT"
        },
        "servesVegetarianFood": True,
        "reviews": [
            {
                "googleMapsUri": "https://maps.example.com/review/central_rev1",
                "authorAttribution": {
                    "displayName": "Local Critic",
                    "uri": "https://example.com/localcritic",
                    "photoUri": "https://example.com/localcritic.jpg"
                },
                "relativePublishTimeDescription": "5 hours ago",
                "publishTime": "2025-04-01T16:00:00Z",
                "flagContentUri": "https://maps.example.com/flag/central_rev1",
                "rating": 4.3,
                "name": "review_central_1",
                "text": {"text": "A serene escape in the midst of the city hustle.", "languageCode": "en"},
                "originalText": {"text": "A serene escape in the midst of the city hustle.", "languageCode": "en"}
            }
        ],
        "servesWine": False,
        "goodForChildren": True,
        "internationalPhoneNumber": "+1 212-310-6600",
        "menuForChildren": False,
        "servesCocktails": False,
        "priceLevel": "PRICE_LEVEL_FREE",
        "timeZone": {"id": "America/New_York", "version": "2023a"},
        "servesDessert": False,
        "addressComponents": [
            {
                "shortText": "NY",
                "types": ["locality", "political"],
                "languageCode": "en",
                "longText": "New York"
            }
        ],
        "viewport": {
            "low": {"latitude": 40.771, "longitude": -73.981},
            "high": {"latitude": 40.796, "longitude": -73.949}
        },
        "rating": 4.3,
        "iconBackgroundColor": "#76A5AF",
        "servesBrunch": False,
        "priceRange": {
            "startPrice": {"units": "0", "nanos": 0, "currencyCode": "USD"},
            "endPrice": {"units": "0", "nanos": 0, "currencyCode": "USD"}
        },
        "primaryType": "park",
        "attributions": [
            {"provider": "NYC Parks", "providerUri": "https://www.nycgovparks.org"}
        ],
        "regularOpeningHours": {
            "nextCloseTime": "2025-04-01T20:30:00Z",
            "openNow": True,
            "nextOpenTime": "2025-04-01T06:00:00Z",
            "periods": [
                {
                    "open": {
                        "day": 0,
                        "hour": 6,
                        "minute": 0,
                        "date": {"year": 2025, "month": 4, "day": 1}
                    },
                    "close": {
                        "day": 0,
                        "hour": 20,
                        "minute": 30,
                        "date": {"year": 2025, "month": 4, "day": 1}
                    }
                }
            ],
            "specialDays": [],
            "weekdayDescriptions": [
                "Sun: 06:00–20:30",
                "Mon: 06:00–20:30",
                "Tue: 06:00–20:30",
                "Wed: 06:00–20:30",
                "Thu: 06:00–20:30",
                "Fri: 06:00–20:30",
                "Sat: 06:00–20:30"
            ],
            "secondaryHoursType": "VISIT"
        },
        "allowsDogs": True,
        "outdoorSeating": True,
        "dineIn": False,
        "name": "Central Park",
        "parkingOptions": {
            "freeStreetParking": True,
            "paidParkingLot": False,
            "freeGarageParking": False,
            "freeParkingLot": True,
            "paidGarageParking": False,
            "paidStreetParking": False,
            "valetParking": False
        },
        "curbsidePickup": False,
        "googleMapsLinks": {
            "reviewsUri": "https://maps.example.com/place/place_central/reviews",
            "writeAReviewUri": "https://maps.example.com/writeareview?place=place_central",
            "photosUri": "https://maps.example.com/place/place_central/photos",
            "directionsUri": "https://maps.example.com/directions?destination=place_central",
            "placeUri": "https://maps.example.com/place/place_central"
        },
        "servesDinner": False,
        "regularSecondaryOpeningHours": [],
        "editorialSummary": {
            "text": "A vast green sanctuary amidst the concrete jungle, ideal for leisure and recreation.",
            "languageCode": "en"
        },
        "paymentOptions": {
            "acceptsNfc": False,
            "acceptsCreditCards": False,
            "acceptsDebitCards": False,
            "acceptsCashOnly": True
        },
        "generativeSummary": {
            "descriptionFlagContentUri": "https://maps.example.com/flag/genDescCentral",
            "overviewFlagContentUri": "https://maps.example.com/flag/genOverviewCentral",
            "description": {
                "text": "An AI-generated detailed description of Central Park.",
                "languageCode": "en"
            },
            "overview": {
                "text": "A peaceful retreat offering scenic views and recreational activities.",
                "languageCode": "en"
            },
            "references": {
                "places": ["ref_central_001"],
                "reviews": []
            }
        },
        "fuelOptions": {
            "fuelPrices": []
        },
        "accessibilityOptions": {
            "wheelchairAccessibleParking": True,
            "wheelchairAccessibleRestroom": True,
            "wheelchairAccessibleSeating": True,
            "wheelchairAccessibleEntrance": True
        },
        "types": ["park", "landmark"],
        "subDestinations": [],
        "displayName": {"text": "Central Park", "languageCode": "en-US"},
        "addressDescriptor": {
            "landmarks": [
                {
                    "straightLineDistanceMeters": 150.0,
                    "types": ["landmark"],
                    "spatialRelationship": "NEAR",
                    "displayName": {"text": "Bethesda Terrace", "languageCode": "en"},
                    "name": "landmark_central_1",
                    "placeId": "lm_central_1",
                    "travelDistanceMeters": 200.0
                }
            ],
            "areas": [
                {
                    "name": "Manhattan",
                    "containment": "WITHIN",
                    "displayName": {"text": "Manhattan", "languageCode": "en"},
                    "placeId": "area_manhattan"
                }
            ]
        },
        "servesLunch": False,
        "nationalPhoneNumber": "+1 212-310-6600"
    }
]



class GoogleMaps:
    """
    The top-level class that handles the in-memory DB and provides
    save/load functionality for JSON-based state persistence.
    """

    @staticmethod
    def save_state(filepath: str) -> None:
        with open(filepath, 'w') as f:
            json.dump(DB, f)

    @staticmethod
    def load_state(filepath: str) -> None:
        global DB
        with open(filepath, 'r') as f:
            DB = json.load(f)



class Places:
    @staticmethod
    def _create_place(place_data: dict) -> dict:
        """
        A small helper function to create a place entry in the in-memory DB.

        Parameters:
          - place_data (dict): A dictionary containing the place data. Must include an "id" key.

        Returns:
          The created place dictionary.

        Raises:
          ValueError: If "id" is missing or if a place with the same id already exists.
        """
        if "id" not in place_data:
            raise ValueError("Place data must contain an 'id' field.")
        for place in Places.DB:
            if place.get("id") == place_data["id"]:
                raise ValueError(f"Place with id '{place_data['id']}' already exists.")
        Places.DB.append(place_data)
        return place_data

    @staticmethod
    def autocomplete(request_data: dict) -> dict:
        """
        Simulates returning predictions for a given input.
        Expects request_data conforming to GoogleMapsPlacesV1AutocompletePlacesRequest.
        Returns a dummy response based on the GoogleMapsPlacesV1AutocompletePlacesResponse schema.
        Not supported
        """
        # In a real implementation, you would validate and process request_data here.
        print("Called autocomplete with request_data:", request_data)
        # Return the (empty) schema structure for autocomplete response.
        return DB.get("GoogleMapsPlacesV1AutocompletePlacesResponse", {})

    @staticmethod
    def get(name, languageCode=None, sessionToken=None, regionCode=None):
        """
        Retrieve the details of a place by its resource name.

        Parameters:
          - name (str): Required. The resource name of the place in the format "places/{place_id}".
          - languageCode (str, optional): Preferred language for place details.
          - sessionToken (str, optional): Session token for billing purposes.
          - regionCode (str, optional): Unicode country/region code of the request origin.

        Returns:
          The place object as a dictionary if found; otherwise, None.
        """
        # Validate that the name matches the expected format.
        if not name.startswith("places/"):
            raise ValueError("Resource name must be in the format 'places/{place_id}'.")

        # Extract the place_id from the name.
        place_id = name.split("/")[1]

        # For this sample, we simply iterate over our static DB.
        for place in DB:
            if place.get("id") == place_id:
                # In a full implementation, languageCode, sessionToken, and regionCode
                # might adjust the returned result.
                return place
        return None

    @staticmethod
    def _haversine_distance(lat1, lon1, lat2, lon2):
        """
        Compute the Haversine distance between two points in meters.
        """
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @staticmethod
    def searchNearby(request):
        """
        Search for places near a location based on request parameters.

        The request is expected to follow the GoogleMapsPlacesV1SearchNearbyRequest schema:
          - routingParameters (Not supported currently)
          - includedPrimaryTypes (optional)
          - excludedTypes (optional)
          - locationRestriction (required)
          - includedTypes (optional)
          - maxResultCount (optional)
          - languageCode (optional)
          - excludedPrimaryTypes (optional)
          - regionCode (Not supported currently)
          - rankPreference (Not supported currently)

        Returns a dictionary following the GoogleMapsPlacesV1SearchNearbyResponse schema:
          - places: list of place objects
          - routingSummaries: Does not support yet.
        """
        filtered_places = []
        routing_summaries = []

        # Retrieve maxResultCount, default to 20 if not provided.
        max_result_count = request.get("maxResultCount", 20)
        languageCode = request.get("languageCode",'')

        # Extract filtering parameters from the request.
        included_primary_types = request.get("includedPrimaryTypes", [])
        excluded_primary_types = request.get("excludedPrimaryTypes", [])
        included_types = request.get("includedTypes", [])
        excluded_types = request.get("excludedTypes", [])

        # For location filtering, we expect a locationRestriction with a circle.
        location_restriction = request.get("locationRestriction", {})
        circle = location_restriction.get("circle")
        if circle:
            center = circle.get("center", {})
            radius = circle.get("radius", 0.0)
            center_lat = center.get("latitude")
            center_lon = center.get("longitude")
        else:
            center_lat = center_lon = radius = None

        # Loop over each place in the static DB.
        for place in DB:
            # Filter by primary types if provided.
            primary_type = place.get("primaryType")
            if included_primary_types and primary_type not in included_primary_types:
                continue
            if excluded_primary_types and primary_type in excluded_primary_types:
                continue

            if included_types:
                types = place.get("types", [])
                if not any(t in included_types for t in types):
                    continue
            if excluded_types:
                types = place.get("types", [])
                if any(t in excluded_types for t in types):
                    continue

            if languageCode and place.get("displayName", {}).get("languageCode") != languageCode:
                continue

            # If location restriction is provided, filter by distance.
            if center_lat is not None and center_lon is not None and radius is not None:
                place_location = place.get("location", {})
                place_lat = place_location.get("latitude")
                place_lon = place_location.get("longitude")
                if place_lat is None or place_lon is None:
                    continue
                distance = Places._haversine_distance(center_lat, center_lon, place_lat, place_lon)
                if distance > radius:
                    continue

            # If the place passes all filters, add it to the result list.
            filtered_places.append(place)

            # Generate a dummy routing summary for this place.
            routing_summary = {}
            routing_summaries.append(routing_summary)

            if len(filtered_places) >= max_result_count:
                break

        return {
            "places": filtered_places,
            "routingSummaries": routing_summaries
        }

    @staticmethod
    def searchText(request):
        """
        Search for places based on a text query and additional filters provided in the request.

        The request is expected to follow the GoogleMapsPlacesV1SearchTextRequest schema:
          - strictTypeFiltering (optional): If true, only results of the same type as includedType are returned.
          - priceLevels (optional): Filter results by the specified price levels.
          - locationBias (optional): A bias (e.g., a rectangle or circle) to influence the ordering of results.
          - openNow (optional): If true, only return places that are currently open.
          - minRating (optional): Only include places whose rating is greater than or equal to this value.
          - pageToken (optional): Used for pagination. (Not implemented in this sample.)
          - includePureServiceAreaBusinesses (optional): If true, include pure service area businesses.
          - locationRestriction (optional): Restrict results to places within the given location (using a circle).
          - languageCode (optional): Preferred language code; if provided, adjust localized text accordingly.
          - maxResultCount (deprecated, optional) / pageSize (optional): Limit the number of results returned.
          - regionCode (optional): A region code to affect display of details. (Not used in filtering.)
          - textQuery (required): The text string to search for. A simple substring search is performed on the place name and formattedAddress.
          - searchAlongRouteParameters (optional): Additional parameters for route-based search. (Not implemented.)
          - includedType (optional): Filter by the requested place type (matches the place's primaryType).
          - evOptions (optional): EV charging options. (Not implemented.)
          - routingParameters (optional): Additional routing parameters. (Not implemented.)
          - rankPreference (optional): How to rank results. (Not implemented.)

        Currently, the implementation supports filtering based on:
          - textQuery: A simple substring match on the "name" and "formattedAddress" fields.
          - strictTypeFiltering/includedType: When strict filtering is enabled, only places matching the includedType are returned.
          - priceLevels: If provided, only places whose priceLevel is in the given list are included.
          - openNow: Only returns places where currentOpeningHours.openNow is True.
          - minRating: Only returns places with a rating greater than or equal to the provided value.
          - includePureServiceAreaBusinesses: Excludes places marked as pure service area businesses if false.
          - locationRestriction: Filters places based on a circle (using Haversine distance).
          - languageCode: Adjusts localized text fields (e.g. displayName) if needed.
          - maxResultCount/pageSize: Limits the number of results returned.

        Other parameters (pageToken, searchAlongRouteParameters, evOptions, routingParameters, rankPreference)
        are acknowledged but not fully implemented in this sample.

        Returns a dictionary following the GoogleMapsPlacesV1SearchTextResponse schema:
          - routingSummaries: (Not fully supported; returns an empty list in this implementation.)
          - searchUri: A dummy URL constructed using the text query.
          - places: A list of place objects that match the filters.
          - contextualContents: (Not implemented; returns an empty list.)
          - nextPageToken: (Not implemented; returns an empty string.)
        """
        filtered_places = []

        # Determine the maximum number of results (using pageSize if provided, else maxResultCount defaulting to 20)
        max_results = request.get("pageSize") or request.get("maxResultCount", 20)

        # Get text query; required.
        text_query = request.get("textQuery", "").lower()
        if not text_query:
            raise ValueError("textQuery is required.")

        # Optional filters:
        strict_type_filtering = request.get("strictTypeFiltering", False)
        included_type = request.get("includedType")
        price_levels = request.get("priceLevels", [])
        open_now = request.get("openNow", False)
        min_rating = request.get("minRating", None)
        include_pure = request.get("includePureServiceAreaBusinesses", True)

        # Location restriction: assume circle filtering if provided.
        location_restriction = request.get("locationRestriction", {})
        circle = location_restriction.get("circle", {})
        if circle:
            center = circle.get("center", {})
            radius = circle.get("radius", 0.0)
            center_lat = center.get("latitude")
            center_lon = center.get("longitude")
        else:
            center_lat = center_lon = radius = None

        # languageCode for potential localized text adjustment.
        language_code = request.get("languageCode")

        # Loop through our static DB and apply filters.
        for place in DB:
            # Filter by textQuery: check if the query appears in the place name or formattedAddress.
            name_field = place.get("name", "").lower()
            formatted_address = place.get("formattedAddress", "").lower()
            if text_query not in name_field and text_query not in formatted_address:
                continue

            # Filter by strict type filtering.
            if strict_type_filtering and included_type:
                if place.get("primaryType") != included_type:
                    continue

            # Filter by priceLevels if provided.
            if price_levels:
                if place.get("priceLevel") not in price_levels:
                    continue

            # Filter by openNow if required.
            if open_now:
                current_hours = place.get("currentOpeningHours", {})
                if not current_hours.get("openNow", False):
                    continue

            # Filter by minRating if provided.
            if min_rating is not None:
                if place.get("rating", 0) < min_rating:
                    continue

            # Filter out pure service area businesses if includePure is False.
            if not include_pure:
                if place.get("pureServiceAreaBusiness", False):
                    continue

            # Filter by locationRestriction if provided.
            if center_lat is not None and center_lon is not None and radius is not None:
                place_location = place.get("location", {})
                place_lat = place_location.get("latitude")
                place_lon = place_location.get("longitude")
                if place_lat is None or place_lon is None:
                    continue
                distance = Places._haversine_distance(center_lat, center_lon, place_lat, place_lon)
                if distance > radius:
                    continue

            # Optionally adjust localized text if languageCode is provided.
            if language_code:
                display = place.get("displayName", {})
                if display.get("languageCode",'') != language_code:
                  continue

            filtered_places.append(place)

            if len(filtered_places) >= max_results:
                break

        # Construct the response.
        response = {
            "routingSummaries": [],  # Routing summaries are not supported yet.
            "places": filtered_places,
            "contextualContents": [],  # Not implemented.
            "nextPageToken": ""  # Not implemented.
        }
        return response

    class Photos:
        @staticmethod
        def getMedia(name, maxWidthPx=None, maxHeightPx=None, skipHttpRedirect=False):
            """
            Get a photo media with a photo reference string.

            Parameters:
              - name (str): Required. The resource name of a photo media in the format:
                "places/{place_id}/photos/{photo_reference}/media". Note that the photo name
                stored in the DB does not include the trailing "/media".
              - maxWidthPx (int, optional): Specifies the maximum desired width (1 to 4800).
              - maxHeightPx (int, optional): Specifies the maximum desired height (1 to 4800).
              - skipHttpRedirect (bool, optional): If True, skip HTTP redirect behavior and return JSON.

            Returns:
              List[dict]: A list of photo media objects, each following the GoogleMapsPlacesV1PhotoMedia schema:
                {
                  "photoUri": <string>,
                  "name": <string>
                }

            Raises:
              ValueError: If the resource name does not match the expected pattern or if neither
                          maxWidthPx nor maxHeightPx is provided.
            """
            # Validate the resource name pattern.
            pattern = r"^places/[^/]+/photos/[^/]+/media$"
            if not re.match(pattern, name):
                raise ValueError("Resource name must be in the format 'places/{place_id}/photos/{photo_reference}/media'.")

            # Ensure at least one dimension is provided.
            if maxWidthPx is None and maxHeightPx is None:
                raise ValueError("At least one of maxWidthPx or maxHeightPx must be specified.")

            # Extract the place_id and photo_reference.
            parts = name.split("/")
            if len(parts) != 5:
                raise ValueError("Invalid resource name format.")
            place_id = parts[1]
            photo_ref = parts[3]

            results = []
            # Search through the static DB.
            for place in DB:
                if place.get("id") == place_id:
                    for photo in place.get("photos", []):
                        # Stored photo names are in the format "places/{place_id}/photos/{photo_reference}".
                        if photo.get("name") == f"places/{place_id}/photos/{photo_ref}":
                            dims = []
                            if maxWidthPx is not None:
                                dims.append(f"w{maxWidthPx}")
                            if maxHeightPx is not None:
                                dims.append(f"h{maxHeightPx}")
                            dims_str = "_".join(dims)
                            dummy_photo_uri = f"https://maps.example.com/media/{photo.get('name')}/media?dims={dims_str}"

                            results.append({
                                "photoUri": dummy_photo_uri,
                                "name": name
                            })
            return results

# Assertions for Places.get
empire = Places.get("places/place_empire")
assert empire is not None, "Empire State Building not found"
assert empire["id"] == "place_empire", "Incorrect place id for Empire State Building"

central = Places.get("places/place_central")
assert central is not None, "Central Park not found"
assert central["id"] == "place_central", "Incorrect place id for Central Park"

try:
    Places.get("invalid/place_empire")
    assert False, "Expected ValueError for invalid resource name"
except ValueError:
    pass

# Assertions for searchNearby (using locationRestriction filtering)
request_nearby = {
    "maxResultCount": 10,
    "locationRestriction": {
        "circle": {
            "center": {"latitude": 40.748817, "longitude": -73.985428},
            "radius": 50  # 50 meters radius
        }
    }
}
result_nearby = Places.searchNearby(request_nearby)
assert "places" in result_nearby, "searchNearby response must contain 'places'"
assert len(result_nearby["places"]) == 1, "Expected only one place within 50 meters"
assert result_nearby["places"][0]["id"] == "place_empire", "Expected Empire State Building in nearby search"

# Assertions for searchText (using textQuery filtering)
request_text = {
    "textQuery": "central park",
    "pageSize": 10
}
result_text = Places.searchText(request_text)
assert "places" in result_text, "searchText response must contain 'places'"
found_ids = [p["id"] for p in result_text["places"]]
assert "place_central" in found_ids, "Expected Central Park in searchText results"

# Assertions for Photos.getMedia
# Valid resource name with dimensions specified.
empire_photo_media = Places.Photos.getMedia("places/place_empire/photos/photo_1/media", maxWidthPx=400)
assert isinstance(empire_photo_media, list), "getMedia should return a list"
assert len(empire_photo_media) > 0, "Expected at least one photo media object"
assert "w400" in empire_photo_media[0]["photoUri"], "Photo URI should contain requested width 'w400'"

# Invalid resource name should raise ValueError.
try:
    Places.Photos.getMedia("invalid/photo/media", maxWidthPx=400)
    assert False, "Expected ValueError for invalid photo resource name"
except ValueError:
    pass

print("All assertions passed.")
