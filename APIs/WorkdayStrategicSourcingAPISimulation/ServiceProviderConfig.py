"""
SCIM Service Provider Configuration Module

This module provides functionality for managing and retrieving the SCIM (System for Cross-domain
Identity Management) service provider configuration in the Workday Strategic Sourcing system.

The module interfaces with the simulation database to provide access to the service provider
configuration, which details the SCIM specification features and capabilities supported by the
system, including authentication schemes, supported operations, and bulk configuration.

Functions:
    get: Retrieves the complete service provider configuration
"""

from typing import Dict, Any, List
from .SimulationEngine import db

def get() -> Dict[str, Any]:
    """
    Retrieves the complete SCIM service provider configuration.

    This function implements the SCIM service provider configuration endpoint as specified
    in RFC 7643, section 5. It returns detailed information about the SCIM features and
    capabilities supported by the system.

    Returns:
        Dict[str, Any]: A dictionary containing the service provider configuration details.
            The dictionary includes the following key-value pairs:
            - "schemas" (List[str]): List of SCIM schemas used in the configuration
            - "documentationUri" (str): URI of the service provider's documentation
            - "patch" (Dict[str, bool]): Configuration for PATCH operations
                - "supported" (bool): Whether PATCH operations are supported
            - "bulk" (Dict[str, Any]): Configuration for bulk operations
                - "supported" (bool): Whether bulk operations are supported
                - "maxOperations" (int): Maximum number of operations in a bulk request
                - "maxPayloadSize" (int): Maximum payload size in bytes
            - "filter" (Dict[str, bool]): Configuration for filtering
                - "supported" (bool): Whether filtering is supported
                - "maxResults" (int): Maximum number of results returned
            - "changePassword" (Dict[str, bool]): Configuration for password changes
                - "supported" (bool): Whether password changes are supported
            - "sort" (Dict[str, bool]): Configuration for sorting
                - "supported" (bool): Whether sorting is supported
            - "etag" (Dict[str, bool]): Configuration for ETags
                - "supported" (bool): Whether ETags are supported
            - "authenticationSchemes" (List[Dict[str, Any]]): List of supported authentication schemes
                Each scheme dictionary contains:
                - "type" (str): The authentication scheme type
                - "name" (str): The name of the authentication scheme
                - "description" (str): A description of the authentication scheme
                - "specUri" (str): URI to the authentication scheme specification
                - "documentationUri" (str): URI to the authentication scheme documentation
            - "meta" (Dict[str, Any]): Configuration metadata
                - "location" (str): The configuration's URI
                - "resourceType" (str): The type of resource (ServiceProviderConfig)
                - "created" (str): Creation timestamp
                - "lastModified" (str): Last modification timestamp
                - "version" (str): The configuration version
    """
    return db.DB["scim"]["service_provider_config"] 