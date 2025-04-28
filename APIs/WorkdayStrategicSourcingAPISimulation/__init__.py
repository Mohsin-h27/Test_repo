"""
Workday Strategic Sourcing API Simulation Package.

This package provides a simulation of the Workday Strategic Sourcing API, implementing various
endpoints and functionality for managing sourcing projects, suppliers, contracts, and related
entities. The package is organized into several main categories:

Core API Modules:
    - Projects and project management
    - Project relationships and types
    - Project descriptions and metadata

Supplier Management:
    - Supplier companies and contacts
    - Supplier segmentation
    - Supplier-related reports

Contact Management:
    - Contact types and definitions
    - Contact-related operations

Spend Management:
    - Spend categories
    - Spend tracking and reporting

User Management:
    - User operations
    - User-related endpoints

Contract Management:
    - Contract operations
    - Contract awards
    - Contract-related reports

Event Management:
    - Event templates and worksheets
    - Bids and bid line items
    - Event-related operations

Field Management:
    - Custom fields
    - Field groups and options
    - Field-related operations

Payment Management:
    - Payment currencies
    - Payment terms
    - Payment types

Reporting:
    - Project reports
    - Supplier reports
    - Performance reviews
    - Contract reports
    - Event reports
    - Savings reports

SCIM Integration:
    - Service provider configuration
    - Resource types
    - Schema management

Attachments:
    - File attachment handling
    - Document management

The package also includes a simulation engine and test suite for testing and validation purposes.
"""

from . import (
    # Core API modules
    Projects,
    ProjectById,
    ProjectByExternalId,
    ProjectTypes,
    ProjectTypeById,
    ProjectRelationshipsSupplierContacts,
    ProjectRelationshipsSupplierContactsExternalId,
    ProjectRelationshipsSupplierCompanies,
    ProjectRelationshipsSupplierCompaniesExternalId,
    ProjectsDescribe,
    
    # Supplier related modules
    Suppliers,
    SupplierCompanies,
    SupplierCompanyById,
    SupplierCompanyByExternalId,
    SupplierCompanyContacts,
    SupplierCompanyContactById,
    SupplierCompanyContactsByExternalId,
    SupplierContacts,
    SupplierContactById,
    SupplierContactByExternalId,
    SupplierCompanySegmentations,
    SupplierCompaniesDescribe,
    
    # Contact related modules
    ContactTypes,
    ContactTypeById,
    ContactTypeByExternalId,
    
    # Spend related modules
    SpendCategories,
    SpendCategoryById,
    SpendCategoryByExternalId,
    
    # User related modules
    Users,
    UserById,
    
    # Contract related modules
    Contracts,
    ContractAward,
    Awards,
    
    # Event related modules
    Events,
    EventBids,
    BidsById,
    BidsDescribe,
    BidLineItems,
    BidLineItemById,
    BidLineItemsList,
    BidLineItemsDescribe,
    EventTemplates,
    EventWorksheets,
    EventWorksheetById,
    EventWorksheetLineItems,
    EventWorksheetLineItemById,
    EventSupplierCompanies,
    EventSupplierCompaniesExternalId,
    EventSupplierContacts,
    EventSupplierContactsExternalId,
    
    # Field related modules
    Fields,
    FieldById,
    FieldByExternalId,
    FieldGroups,
    FieldGroupById,
    FieldOptions,
    FieldOptionsByFieldId,
    FieldOptionById,
    
    # Payment related modules
    PaymentCurrencies,
    PaymentCurrenciesId,
    PaymentCurrenciesExternalId,
    PaymentTerms,
    PaymentTermsId,
    PaymentTermsExternalId,
    PaymentTypes,
    PaymentTypesId,
    PaymentTypesExternalId,
    
    # Report related modules
    ProjectReports,
    ProjectMilestoneReports,
    SupplierReports,
    SupplierReviewReports,
    PerformanceReviewReports,
    PerformanceReviewAnswerReports,
    ContractReports,
    ContractMilestoneReports,
    EventReports,
    SavingsReports,
    
    # SCIM related modules
    ServiceProviderConfig,
    ResourceTypes,
    ResourceTypeById,
    Schemas,
    SchemaById,
    
    # Attachments
    Attachments,
)

# Expose subdirectories
from . import SimulationEngine
from . import test

__all__ = [
    # Core API modules
    'Projects', 'ProjectById', 'ProjectByExternalId', 'ProjectTypes', 'ProjectTypeById',
    'ProjectRelationshipsSupplierContacts', 'ProjectRelationshipsSupplierContactsExternalId',
    'ProjectRelationshipsSupplierCompanies', 'ProjectRelationshipsSupplierCompaniesExternalId',
    'ProjectsDescribe',
    
    # Supplier related modules
    'Suppliers', 'SupplierCompanies', 'SupplierCompanyById', 'SupplierCompanyByExternalId',
    'SupplierCompanyContacts', 'SupplierCompanyContactById', 'SupplierCompanyContactsByExternalId',
    'SupplierContacts', 'SupplierContactById', 'SupplierContactByExternalId',
    'SupplierCompanySegmentations', 'SupplierCompaniesDescribe',
    
    # Contact related modules
    'ContactTypes', 'ContactTypeById', 'ContactTypeByExternalId',
    
    # Spend related modules
    'SpendCategories', 'SpendCategoryById', 'SpendCategoryByExternalId',
    
    # User related modules
    'Users', 'UserById',
    
    # Contract related modules
    'Contracts', 'ContractAward', 'Awards',
    
    # Event related modules
    'Events', 'EventTemplates', 'EventWorksheets', 'EventWorksheetById',
    'EventWorksheetLineItems', 'EventWorksheetLineItemById', 'EventSupplierCompanies',
    'EventSupplierCompaniesExternalId', 'EventBids', 'BidsById', 'EventSupplierContacts',
    'EventSupplierContactsExternalId', 'BidsDescribe', 'BidLineItems', 'BidLineItemById',
    'BidLineItemsList', 'BidLineItemsDescribe',

    # Field related modules
    'Fields', 'FieldById', 'FieldByExternalId', 'FieldGroups', 'FieldGroupById',
    'FieldOptions', 'FieldOptionsByFieldId', 'FieldOptionById',
    
    # Payment related modules
    'PaymentCurrencies', 'PaymentCurrenciesId', 'PaymentCurrenciesExternalId',
    'PaymentTerms', 'PaymentTermsId', 'PaymentTermsExternalId',
    'PaymentTypes', 'PaymentTypesId', 'PaymentTypesExternalId',
    
    # Report related modules
    'ProjectReports', 'ProjectMilestoneReports', 'SupplierReports', 'SupplierReviewReports',
    'PerformanceReviewReports', 'PerformanceReviewAnswerReports', 'ContractReports',
    'ContractMilestoneReports', 'EventReports', 'SavingsReports',
    
    # SCIM related modules
    'ServiceProviderConfig', 'ResourceTypes', 'ResourceTypeById', 'Schemas', 'SchemaById',
    
    # Attachments
    'Attachments',
    
    # Subdirectories
    'SimulationEngine', 'test'
] 