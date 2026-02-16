"""
SECURITY DOCUMENTATION FOR MULTI-TENANT API VIEWS

This document explains the security mechanisms implemented in the inventory API
to ensure complete company isolation and data protection.

═══════════════════════════════════════════════════════════════════════════════

1. ARCHITECTURE OVERVIEW
─────────────────────────

All API views inherit from BaseCompanyAPIView which enforces:
- IsAuthenticated permission (JWT tokens required)
- Company isolation (NEVER trust company from request body)
- Automatic company assignment from user.profile.company
- Validation that all accessed objects belong to user's company

2. SECURITY IMPLEMENTATION
──────────────────────────

2.1 AUTHENTICATION
   - All views require IsAuthenticated permission
   - Company obtained from request.user.profile.company
   - NEVER accept company from request.data or query parameters

2.2 MULTI-TENANT ISOLATION
   - Every model has a company foreign key (except Movement/Batch which inherit via Product)
   - All querysets filtered by user's company
   - Cross-company access returns 404 (appears as not found)
   - Prevents data leakage between companies

2.3 DATA VALIDATION
   - Company ID forced during POST/PUT operations
   - Category/Product existence validated within same company
   - Batch/Movement queries filter by product company
   - No direct company modification allowed

═══════════════════════════════════════════════════════════════════════════════

3. ENDPOINT SECURITY RULES
──────────────────────────

3.1 CategoryAPIView

   GET /categories/
   ├─ Lists all categories for user's company
   ├─ Query filters: name, slug
   └─ Security: Company filter applied

   POST /categories/
   ├─ Creates category in user's company
   ├─ Company automatically assigned
   ├─ Cannot override company field
   └─ Returns 400 if invalid data

   GET /categories/{id}/
   ├─ Retrieves specific category
   ├─ Returns 404 if doesn't belong to company
   └─ Security: Company validation

   PUT /categories/{id}/
   ├─ Updates entire category
   ├─ Company cannot be changed
   ├─ Returns 403 if cross-company access
   └─ Security: Company validation + preservation

   PATCH /categories/{id}/
   ├─ Partial update
   ├─ Company field is removed before save
   └─ Security: Company preservation

   DELETE /categories/{id}/
   ├─ Deletes only if belongs to company
   └─ Returns 403 if unauthorized

3.2 ProductAPIView

   Same as CategoryAPIView, with additional validation:
   - Category must belong to same company
   - Returns 400 if category from other company
   - Company assignment on creation

3.3 BatchAPIView

   GET /batches/
   ├─ Lists batches of products in user's company
   ├─ Query filters: product_id
   └─ Security: Filter by product.company

   POST /batches/
   ├─ Creates batch for product in user's company
   ├─ Uses StockService for consistency
   ├─ Validates product ownership
   └─ Returns 404 if product doesn't belong

   GET /batches/{id}/
   ├─ Returns batch only if product in company
   └─ Returns 404 otherwise

   DELETE /batches/{id}/
   ├─ Deletes only if product belongs to company
   └─ Security: Product company validation

3.4 MovementAPIView

   GET /movements/
   ├─ Lists all movements for company batches
   ├─ Query filters: batch_id, movement_type
   └─ Security: Filter by batch.product.company

   POST /movements/
   ├─ Creates movement for batch in company
   ├─ Uses StockService for consistency
   ├─ Validates batch ownership
   ├─ Supports types: IN, OUT, ADJUST, EXPIRED
   └─ Returns 404 if batch doesn't belong

   GET /movements/{id}/
   ├─ Returns movement only if batch in company
   └─ Returns 404 otherwise

═══════════════════════════════════════════════════════════════════════════════

4. ERROR CODES AND RESPONSES
────────────────────────────

200 OK
   - Successful GET, PUT, PATCH
   - List operations with results

201 CREATED
   - Successful POST
   - Resource created successfully

204 NO CONTENT
   - Successful DELETE
   - No data returned

400 BAD REQUEST
   - Invalid input data
   - Missing required fields
   - Category/Product from other company
   - Example: {"detail": "Category not found or doesn't belong to your company"}

403 FORBIDDEN
   - Cross-company access attempt
   - Unauthorized operation
   - Example: {"detail": "You don't have permission to access this resource"}

404 NOT FOUND
   - Resource doesn't exist
   - Cross-company access (appears as not found)
   - Example: {"detail": "Resource not found"}

500 INTERNAL SERVER ERROR
   - Unexpected error
   - Should be logged and monitored

═══════════════════════════════════════════════════════════════════════════════

5. IMPLEMENTATION DETAILS
─────────────────────────

BaseCompanyAPIView Methods:

get_company()
   ├─ Retrieves company from request.user.profile.company
   ├─ Raises ValueError if user has no profile
   └─ NEVER accepts company from request

get_company_queryset()
   ├─ Returns model.objects.filter(company=company)
   ├─ All queries must use this or similar filtering
   └─ Prevents accidental cross-company queries

validate_company_ownership(obj)
   ├─ Checks obj.company == user.company
   ├─ Raises PermissionError if mismatch
   └─ Called before modifications

handle_exception(exc)
   ├─ Converts exceptions to proper DRF responses
   ├─ Maps error types to HTTP status codes
   └─ Secure error messages without exposing internals

═══════════════════════════════════════════════════════════════════════════════

6. PRODUCTION CHECKLIST
───────────────────────

✓ All views inherit from BaseCompanyAPIView
✓ IsAuthenticated permission enforced
✓ Company obtained from user.profile.company
✓ Request.data.company ignored for POST/PUT
✓ All querysets filter by company
✓ Cross-company access returns 404
✓ Proper JSON error responses
✓ Input validation on all endpoints
✓ Database transactions for consistency (via StockService)
✓ Logging for security events (recommended)

═══════════════════════════════════════════════════════════════════════════════

7. EXAMPLE SCENARIOS
────────────────────

Scenario 1: User tries to access another company's category

User from Company A requests: GET /categories/999/
Category 999 belongs to Company B

Result:
   Status: 404 NOT FOUND
   Body: {"detail": "Resource not found"}
   
Security: Category not found or company mismatch returns same 404
         Prevents leaking information about other companies

Scenario 2: User tries to create product with wrong category

User from Company A requests: POST /products/
Body: {
    "name": "Product X",
    "category": 50,  ← Belongs to Company B
    "company": 2,    ← Attempt to override
    ...
}

Result:
   Status: 400 BAD REQUEST
   Body: {
       "detail": "Category not found or doesn't belong to your company"
   }

Security:
   1. Request company field is ignored, Company A is used
   2. Category validated within Company A
   3. Cross-company category properly rejected

Scenario 3: User tries to modify another company's product

User from Company A requests: PUT /products/10/
Product 10 belongs to Company B
Body: {"name": "New Name", ...}

Result:
   Status: 404 NOT FOUND
   Body: {"detail": "Resource not found"}

Security: Similar to Scenario 1, no information leaked

═══════════════════════════════════════════════════════════════════════════════

8. MIGRATION NOTES
──────────────────

If upgrading from insecure views (SuperApiView):

Old Code (INSECURE):
   class ProductAPIView(SuperApiView):
       model = Product
       serializer_class = ProductSerializer
       # ❌ No company filtering
       # ❌ No authentication check
       # ❌ query: Product.objects.all()

New Code (SECURE):
   class ProductAPIView(BaseCompanyAPIView):
       model = Product
       serializer_class = ProductSerializer
       # ✓ Automatic company filtering
       # ✓ IsAuthenticated required
       # ✓ query: Product.objects.filter(company=company)

Update URLs still compatible:
   path("products/", ProductAPIView.as_view())
   path("products/<int:pk>/", ProductAPIView.as_view())

═══════════════════════════════════════════════════════════════════════════════

9. TESTING GUIDE
────────────────

Required Test Cases:

1. Authentication Tests
   - GET without token → 401 UNAUTHORIZED
   - GET with invalid token → 401 UNAUTHORIZED
   - GET with valid token → 200 OK

2. Multi-Tenant Tests
   - User A accesses Company A data → Success
   - User A accesses Company B data → 404 NOT FOUND
   - User creates object, verify company assigned → Company A
   - User tries to override company → Company preserved

3. Data Validation Tests
   - POST without required fields → 400 BAD REQUEST
   - POST with category from other company → 400 BAD REQUEST
   - POST with invalid category → 400 BAD REQUEST

4. Permission Tests
   - DELETE object from same company → 204 NO CONTENT
   - DELETE object from other company → 404 NOT FOUND

═══════════════════════════════════════════════════════════════════════════════

10. LOGGING RECOMMENDATIONS
────────────────────────────

Recommended Security Events to Log:

- Failed authentication attempts
- Cross-company access attempts
- Data modification operations (POST, PUT, PATCH, DELETE)
- Validation errors
- Exception handling

Example implementation:
   
   import logging
   logger = logging.getLogger(__name__)
   
   def post(self, request):
       try:
           company = self.get_company()
           logger.info(f"User {request.user} creating in company {company}")
           ...
       except PermissionError:
           logger.warning(f"Unauthorized access by {request.user}")
           ...

═══════════════════════════════════════════════════════════════════════════════

For questions or security concerns, contact your security team.

Last Updated: 2026-02-15
Version: 1.0
"""
