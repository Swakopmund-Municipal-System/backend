# DefaultAPI

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createMissedWastePickupApiWasteManagementMissedWastePickupsPost**](DefaultAPI.md#createmissedwastepickupapiwastemanagementmissedwastepickupspost) | **POST** /api/waste-management/missed_waste_pickups/ | Create Missed Waste Pickup
[**getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet**](DefaultAPI.md#getmissedwastepickupdetailsapiwastemanagementmissedwastepickupsidget) | **GET** /api/waste-management/missed_waste_pickups/{id} | Get Missed Waste Pickup Details
[**getMissedWastePickupsApiWasteManagementMissedWastePickupsGet**](DefaultAPI.md#getmissedwastepickupsapiwastemanagementmissedwastepickupsget) | **GET** /api/waste-management/missed_waste_pickups | Get Missed Waste Pickups
[**updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost**](DefaultAPI.md#updatemissedwastepickupstatusapiwastemanagementmissedwastepickupsupdatestatuspost) | **POST** /api/waste-management/missed_waste_pickups/update_status | Update Missed Waste Pickup Status


# **createMissedWastePickupApiWasteManagementMissedWastePickupsPost**
```swift
    open class func createMissedWastePickupApiWasteManagementMissedWastePickupsPost(createMissedWastePickupDto: CreateMissedWastePickupDto, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Create Missed Waste Pickup

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let createMissedWastePickupDto = CreateMissedWastePickupDto(description: "description_example", date: "date_example", address: "address_example") // CreateMissedWastePickupDto | 

// Create Missed Waste Pickup
DefaultAPI.createMissedWastePickupApiWasteManagementMissedWastePickupsPost(createMissedWastePickupDto: createMissedWastePickupDto) { (response, error) in
    guard error == nil else {
        print(error)
        return
    }

    if (response) {
        dump(response)
    }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **createMissedWastePickupDto** | [**CreateMissedWastePickupDto**](CreateMissedWastePickupDto.md) |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet**
```swift
    open class func getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet(id: Int, completion: @escaping (_ data: MissedWastePickupSearchResultDto?, _ error: Error?) -> Void)
```

Get Missed Waste Pickup Details

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let id = 987 // Int | 

// Get Missed Waste Pickup Details
DefaultAPI.getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet(id: id) { (response, error) in
    guard error == nil else {
        print(error)
        return
    }

    if (response) {
        dump(response)
    }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Int** |  | 

### Return type

[**MissedWastePickupSearchResultDto**](MissedWastePickupSearchResultDto.md)

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getMissedWastePickupsApiWasteManagementMissedWastePickupsGet**
```swift
    open class func getMissedWastePickupsApiWasteManagementMissedWastePickupsGet(searchTerm: String? = nil, sortField: String? = nil, sortOrder: String? = nil, limit: Int? = nil, page: Int? = nil, completion: @escaping (_ data: [MissedWastePickupSearchResultDto]?, _ error: Error?) -> Void)
```

Get Missed Waste Pickups

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let searchTerm = "searchTerm_example" // String |  (optional) (default to "")
let sortField = "sortField_example" // String |  (optional) (default to "id")
let sortOrder = "sortOrder_example" // String |  (optional) (default to "desc")
let limit = 987 // Int |  (optional) (default to 10)
let page = 987 // Int |  (optional) (default to 1)

// Get Missed Waste Pickups
DefaultAPI.getMissedWastePickupsApiWasteManagementMissedWastePickupsGet(searchTerm: searchTerm, sortField: sortField, sortOrder: sortOrder, limit: limit, page: page) { (response, error) in
    guard error == nil else {
        print(error)
        return
    }

    if (response) {
        dump(response)
    }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **searchTerm** | **String** |  | [optional] [default to &quot;&quot;]
 **sortField** | **String** |  | [optional] [default to &quot;id&quot;]
 **sortOrder** | **String** |  | [optional] [default to &quot;desc&quot;]
 **limit** | **Int** |  | [optional] [default to 10]
 **page** | **Int** |  | [optional] [default to 1]

### Return type

[**[MissedWastePickupSearchResultDto]**](MissedWastePickupSearchResultDto.md)

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost**
```swift
    open class func updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost(updateMissedWastePickupStatusDto: UpdateMissedWastePickupStatusDto, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Update Missed Waste Pickup Status

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let updateMissedWastePickupStatusDto = UpdateMissedWastePickupStatusDto(id: 123, status: 123) // UpdateMissedWastePickupStatusDto | 

// Update Missed Waste Pickup Status
DefaultAPI.updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost(updateMissedWastePickupStatusDto: updateMissedWastePickupStatusDto) { (response, error) in
    guard error == nil else {
        print(error)
        return
    }

    if (response) {
        dump(response)
    }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **updateMissedWastePickupStatusDto** | [**UpdateMissedWastePickupStatusDto**](UpdateMissedWastePickupStatusDto.md) |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

