# DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createMissedWastePickupApiWasteManagementMissedWastePickupsPost**](DefaultApi.md#createMissedWastePickupApiWasteManagementMissedWastePickupsPost) | **POST** /api/waste-management/missed_waste_pickups/ | Create Missed Waste Pickup
[**getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet**](DefaultApi.md#getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet) | **GET** /api/waste-management/missed_waste_pickups/{id} | Get Missed Waste Pickup Details
[**getMissedWastePickupsApiWasteManagementMissedWastePickupsGet**](DefaultApi.md#getMissedWastePickupsApiWasteManagementMissedWastePickupsGet) | **GET** /api/waste-management/missed_waste_pickups | Get Missed Waste Pickups
[**updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost**](DefaultApi.md#updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost) | **POST** /api/waste-management/missed_waste_pickups/update_status | Update Missed Waste Pickup Status


<a id="createMissedWastePickupApiWasteManagementMissedWastePickupsPost"></a>
# **createMissedWastePickupApiWasteManagementMissedWastePickupsPost**
> kotlin.Any createMissedWastePickupApiWasteManagementMissedWastePickupsPost(createMissedWastePickupDto)

Create Missed Waste Pickup

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val createMissedWastePickupDto : CreateMissedWastePickupDto =  // CreateMissedWastePickupDto | 
try {
    val result : kotlin.Any = apiInstance.createMissedWastePickupApiWasteManagementMissedWastePickupsPost(createMissedWastePickupDto)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#createMissedWastePickupApiWasteManagementMissedWastePickupsPost")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#createMissedWastePickupApiWasteManagementMissedWastePickupsPost")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **createMissedWastePickupDto** | [**CreateMissedWastePickupDto**](CreateMissedWastePickupDto.md)|  |

### Return type

[**kotlin.Any**](kotlin.Any.md)

### Authorization


Configure Authorization:
    ApiClient.apiKey["Authorization"] = ""
    ApiClient.apiKeyPrefix["Authorization"] = ""
Configure X-API-KEY:
    ApiClient.apiKey["X-API-KEY"] = ""
    ApiClient.apiKeyPrefix["X-API-KEY"] = ""

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a id="getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet"></a>
# **getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet**
> MissedWastePickupSearchResultDto getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet(id)

Get Missed Waste Pickup Details

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val id : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : MissedWastePickupSearchResultDto = apiInstance.getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet(id)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#getMissedWastePickupDetailsApiWasteManagementMissedWastePickupsIdGet")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **kotlin.Int**|  |

### Return type

[**MissedWastePickupSearchResultDto**](MissedWastePickupSearchResultDto.md)

### Authorization


Configure Authorization:
    ApiClient.apiKey["Authorization"] = ""
    ApiClient.apiKeyPrefix["Authorization"] = ""
Configure X-API-KEY:
    ApiClient.apiKey["X-API-KEY"] = ""
    ApiClient.apiKeyPrefix["X-API-KEY"] = ""

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="getMissedWastePickupsApiWasteManagementMissedWastePickupsGet"></a>
# **getMissedWastePickupsApiWasteManagementMissedWastePickupsGet**
> kotlin.collections.List&lt;MissedWastePickupSearchResultDto&gt; getMissedWastePickupsApiWasteManagementMissedWastePickupsGet(searchTerm, sortField, sortOrder, limit, page)

Get Missed Waste Pickups

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val searchTerm : kotlin.String = searchTerm_example // kotlin.String | 
val sortField : kotlin.String = sortField_example // kotlin.String | 
val sortOrder : kotlin.String = sortOrder_example // kotlin.String | 
val limit : kotlin.Int = 56 // kotlin.Int | 
val page : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : kotlin.collections.List<MissedWastePickupSearchResultDto> = apiInstance.getMissedWastePickupsApiWasteManagementMissedWastePickupsGet(searchTerm, sortField, sortOrder, limit, page)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#getMissedWastePickupsApiWasteManagementMissedWastePickupsGet")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#getMissedWastePickupsApiWasteManagementMissedWastePickupsGet")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **searchTerm** | **kotlin.String**|  | [optional] [default to &quot;&quot;]
 **sortField** | **kotlin.String**|  | [optional] [default to &quot;id&quot;]
 **sortOrder** | **kotlin.String**|  | [optional] [default to &quot;desc&quot;]
 **limit** | **kotlin.Int**|  | [optional] [default to 10]
 **page** | **kotlin.Int**|  | [optional] [default to 1]

### Return type

[**kotlin.collections.List&lt;MissedWastePickupSearchResultDto&gt;**](MissedWastePickupSearchResultDto.md)

### Authorization


Configure Authorization:
    ApiClient.apiKey["Authorization"] = ""
    ApiClient.apiKeyPrefix["Authorization"] = ""
Configure X-API-KEY:
    ApiClient.apiKey["X-API-KEY"] = ""
    ApiClient.apiKeyPrefix["X-API-KEY"] = ""

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost"></a>
# **updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost**
> kotlin.Any updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost(updateMissedWastePickupStatusDto)

Update Missed Waste Pickup Status

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val updateMissedWastePickupStatusDto : UpdateMissedWastePickupStatusDto =  // UpdateMissedWastePickupStatusDto | 
try {
    val result : kotlin.Any = apiInstance.updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost(updateMissedWastePickupStatusDto)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#updateMissedWastePickupStatusApiWasteManagementMissedWastePickupsUpdateStatusPost")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **updateMissedWastePickupStatusDto** | [**UpdateMissedWastePickupStatusDto**](UpdateMissedWastePickupStatusDto.md)|  |

### Return type

[**kotlin.Any**](kotlin.Any.md)

### Authorization


Configure Authorization:
    ApiClient.apiKey["Authorization"] = ""
    ApiClient.apiKeyPrefix["Authorization"] = ""
Configure X-API-KEY:
    ApiClient.apiKey["X-API-KEY"] = ""
    ApiClient.apiKeyPrefix["X-API-KEY"] = ""

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

