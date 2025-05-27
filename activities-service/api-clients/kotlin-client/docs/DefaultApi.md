# DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createNewActivityApiActivitiesPost**](DefaultApi.md#createNewActivityApiActivitiesPost) | **POST** /api/activities/ | Create New Activity
[**createNewActivityReviewApiActivitiesReviewsPost**](DefaultApi.md#createNewActivityReviewApiActivitiesReviewsPost) | **POST** /api/activities/reviews/ | Create New Activity Review
[**deleteActivityApiActivitiesActivityIdDelete**](DefaultApi.md#deleteActivityApiActivitiesActivityIdDelete) | **DELETE** /api/activities/{activity_id} | Delete Activity
[**deleteActivityImagesApiActivitiesImagesImageIdDelete**](DefaultApi.md#deleteActivityImagesApiActivitiesImagesImageIdDelete) | **DELETE** /api/activities/images/{image_id} | Delete Activity Images
[**deleteActivityReviewApiActivitiesReviewsReviewIdDelete**](DefaultApi.md#deleteActivityReviewApiActivitiesReviewsReviewIdDelete) | **DELETE** /api/activities/reviews/{review_id} | Delete Activity Review
[**getActivitiesApiActivitiesSearchGet**](DefaultApi.md#getActivitiesApiActivitiesSearchGet) | **GET** /api/activities/search | Get Activities
[**getActivitiesByLocationApiActivitiesSearchLocationGet**](DefaultApi.md#getActivitiesByLocationApiActivitiesSearchLocationGet) | **GET** /api/activities/search/location | Get Activities By Location
[**getActivityApiActivitiesActivityIdGet**](DefaultApi.md#getActivityApiActivitiesActivityIdGet) | **GET** /api/activities/{activity_id} | Get Activity
[**getActivityImagesApiActivitiesImagesActivityActivityIdGet**](DefaultApi.md#getActivityImagesApiActivitiesImagesActivityActivityIdGet) | **GET** /api/activities/images/activity/{activity_id} | Get Activity Images
[**getImageApiActivitiesImagesImageIdGet**](DefaultApi.md#getImageApiActivitiesImagesImageIdGet) | **GET** /api/activities/images/{image_id} | Get Image
[**getReviewsApiActivitiesReviewsGet**](DefaultApi.md#getReviewsApiActivitiesReviewsGet) | **GET** /api/activities/reviews/ | Get Reviews
[**updateActivityApiActivitiesEditPost**](DefaultApi.md#updateActivityApiActivitiesEditPost) | **POST** /api/activities/edit | Update Activity
[**uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost**](DefaultApi.md#uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost) | **POST** /api/activities/images/activity/{activity_id}/upload | Upload Activity Images
[**uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost**](DefaultApi.md#uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost) | **POST** /api/activities/images/activity/{activity_id}/hero/upload | Upload Hero Image


<a id="createNewActivityApiActivitiesPost"></a>
# **createNewActivityApiActivitiesPost**
> kotlin.Any createNewActivityApiActivitiesPost(name, type, latitude, longitude, address, bookingUrl, description, files, heroImage)

Create New Activity

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val name : kotlin.String = name_example // kotlin.String | 
val type : kotlin.Int = 56 // kotlin.Int | 
val latitude : java.math.BigDecimal = 8.14 // java.math.BigDecimal | 
val longitude : java.math.BigDecimal = 8.14 // java.math.BigDecimal | 
val address : kotlin.String = address_example // kotlin.String | 
val bookingUrl : kotlin.String = bookingUrl_example // kotlin.String | 
val description : kotlin.String = description_example // kotlin.String | 
val files : kotlin.collections.List<java.io.File> = /path/to/file.txt // kotlin.collections.List<java.io.File> | 
val heroImage : java.io.File = BINARY_DATA_HERE // java.io.File | 
try {
    val result : kotlin.Any = apiInstance.createNewActivityApiActivitiesPost(name, type, latitude, longitude, address, bookingUrl, description, files, heroImage)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#createNewActivityApiActivitiesPost")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#createNewActivityApiActivitiesPost")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **kotlin.String**|  |
 **type** | **kotlin.Int**|  |
 **latitude** | **java.math.BigDecimal**|  |
 **longitude** | **java.math.BigDecimal**|  |
 **address** | **kotlin.String**|  |
 **bookingUrl** | **kotlin.String**|  |
 **description** | **kotlin.String**|  | [optional]
 **files** | **kotlin.collections.List&lt;java.io.File&gt;**|  | [optional]
 **heroImage** | **java.io.File**|  | [optional]

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

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

<a id="createNewActivityReviewApiActivitiesReviewsPost"></a>
# **createNewActivityReviewApiActivitiesReviewsPost**
> kotlin.Any createNewActivityReviewApiActivitiesReviewsPost(createReviewDTO)

Create New Activity Review

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val createReviewDTO : CreateReviewDTO =  // CreateReviewDTO | 
try {
    val result : kotlin.Any = apiInstance.createNewActivityReviewApiActivitiesReviewsPost(createReviewDTO)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#createNewActivityReviewApiActivitiesReviewsPost")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#createNewActivityReviewApiActivitiesReviewsPost")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **createReviewDTO** | [**CreateReviewDTO**](CreateReviewDTO.md)|  |

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

<a id="deleteActivityApiActivitiesActivityIdDelete"></a>
# **deleteActivityApiActivitiesActivityIdDelete**
> kotlin.Any deleteActivityApiActivitiesActivityIdDelete(activityId)

Delete Activity

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val activityId : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : kotlin.Any = apiInstance.deleteActivityApiActivitiesActivityIdDelete(activityId)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#deleteActivityApiActivitiesActivityIdDelete")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#deleteActivityApiActivitiesActivityIdDelete")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activityId** | **kotlin.Int**|  |

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="deleteActivityImagesApiActivitiesImagesImageIdDelete"></a>
# **deleteActivityImagesApiActivitiesImagesImageIdDelete**
> kotlin.Any deleteActivityImagesApiActivitiesImagesImageIdDelete(imageId)

Delete Activity Images

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val imageId : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : kotlin.Any = apiInstance.deleteActivityImagesApiActivitiesImagesImageIdDelete(imageId)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#deleteActivityImagesApiActivitiesImagesImageIdDelete")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#deleteActivityImagesApiActivitiesImagesImageIdDelete")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **imageId** | **kotlin.Int**|  |

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="deleteActivityReviewApiActivitiesReviewsReviewIdDelete"></a>
# **deleteActivityReviewApiActivitiesReviewsReviewIdDelete**
> kotlin.Any deleteActivityReviewApiActivitiesReviewsReviewIdDelete(reviewId)

Delete Activity Review

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val reviewId : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : kotlin.Any = apiInstance.deleteActivityReviewApiActivitiesReviewsReviewIdDelete(reviewId)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#deleteActivityReviewApiActivitiesReviewsReviewIdDelete")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#deleteActivityReviewApiActivitiesReviewsReviewIdDelete")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reviewId** | **kotlin.Int**|  |

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="getActivitiesApiActivitiesSearchGet"></a>
# **getActivitiesApiActivitiesSearchGet**
> kotlin.Any getActivitiesApiActivitiesSearchGet(searchTerm, sortField, sortOrder, limit, page, categories)

Get Activities

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
val categories : kotlin.String = categories_example // kotlin.String | 
try {
    val result : kotlin.Any = apiInstance.getActivitiesApiActivitiesSearchGet(searchTerm, sortField, sortOrder, limit, page, categories)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#getActivitiesApiActivitiesSearchGet")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#getActivitiesApiActivitiesSearchGet")
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
 **categories** | **kotlin.String**|  | [optional]

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="getActivitiesByLocationApiActivitiesSearchLocationGet"></a>
# **getActivitiesByLocationApiActivitiesSearchLocationGet**
> kotlin.Any getActivitiesByLocationApiActivitiesSearchLocationGet(latitude, longitude, radius, searchTerm, categories)

Get Activities By Location

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val latitude : java.math.BigDecimal = 8.14 // java.math.BigDecimal | 
val longitude : java.math.BigDecimal = 8.14 // java.math.BigDecimal | 
val radius : kotlin.Int = 56 // kotlin.Int | 
val searchTerm : kotlin.String = searchTerm_example // kotlin.String | 
val categories : kotlin.String = categories_example // kotlin.String | 
try {
    val result : kotlin.Any = apiInstance.getActivitiesByLocationApiActivitiesSearchLocationGet(latitude, longitude, radius, searchTerm, categories)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#getActivitiesByLocationApiActivitiesSearchLocationGet")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#getActivitiesByLocationApiActivitiesSearchLocationGet")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latitude** | **java.math.BigDecimal**|  |
 **longitude** | **java.math.BigDecimal**|  |
 **radius** | **kotlin.Int**|  | [optional] [default to 1000]
 **searchTerm** | **kotlin.String**|  | [optional] [default to &quot;&quot;]
 **categories** | **kotlin.String**|  | [optional]

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="getActivityApiActivitiesActivityIdGet"></a>
# **getActivityApiActivitiesActivityIdGet**
> kotlin.Any getActivityApiActivitiesActivityIdGet(activityId)

Get Activity

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val activityId : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : kotlin.Any = apiInstance.getActivityApiActivitiesActivityIdGet(activityId)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#getActivityApiActivitiesActivityIdGet")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#getActivityApiActivitiesActivityIdGet")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activityId** | **kotlin.Int**|  |

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="getActivityImagesApiActivitiesImagesActivityActivityIdGet"></a>
# **getActivityImagesApiActivitiesImagesActivityActivityIdGet**
> kotlin.Any getActivityImagesApiActivitiesImagesActivityActivityIdGet(activityId)

Get Activity Images

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val activityId : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : kotlin.Any = apiInstance.getActivityImagesApiActivitiesImagesActivityActivityIdGet(activityId)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#getActivityImagesApiActivitiesImagesActivityActivityIdGet")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#getActivityImagesApiActivitiesImagesActivityActivityIdGet")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activityId** | **kotlin.Int**|  |

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="getImageApiActivitiesImagesImageIdGet"></a>
# **getImageApiActivitiesImagesImageIdGet**
> kotlin.Any getImageApiActivitiesImagesImageIdGet(imageId)

Get Image

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val imageId : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : kotlin.Any = apiInstance.getImageApiActivitiesImagesImageIdGet(imageId)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#getImageApiActivitiesImagesImageIdGet")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#getImageApiActivitiesImagesImageIdGet")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **imageId** | **kotlin.Int**|  |

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="getReviewsApiActivitiesReviewsGet"></a>
# **getReviewsApiActivitiesReviewsGet**
> kotlin.Any getReviewsApiActivitiesReviewsGet(searchTerm, sortField, sortOrder, limit, page, activityId)

Get Reviews

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
val activityId : kotlin.Int = 56 // kotlin.Int | 
try {
    val result : kotlin.Any = apiInstance.getReviewsApiActivitiesReviewsGet(searchTerm, sortField, sortOrder, limit, page, activityId)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#getReviewsApiActivitiesReviewsGet")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#getReviewsApiActivitiesReviewsGet")
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
 **activityId** | **kotlin.Int**|  | [optional] [default to 0]

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

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a id="updateActivityApiActivitiesEditPost"></a>
# **updateActivityApiActivitiesEditPost**
> kotlin.Any updateActivityApiActivitiesEditPost(activityEditDTO)

Update Activity

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val activityEditDTO : ActivityEditDTO =  // ActivityEditDTO | 
try {
    val result : kotlin.Any = apiInstance.updateActivityApiActivitiesEditPost(activityEditDTO)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#updateActivityApiActivitiesEditPost")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#updateActivityApiActivitiesEditPost")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activityEditDTO** | [**ActivityEditDTO**](ActivityEditDTO.md)|  |

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

<a id="uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost"></a>
# **uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost**
> kotlin.Any uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost(activityId, images)

Upload Activity Images

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val activityId : kotlin.Int = 56 // kotlin.Int | 
val images : kotlin.collections.List<java.io.File> = /path/to/file.txt // kotlin.collections.List<java.io.File> | 
try {
    val result : kotlin.Any = apiInstance.uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost(activityId, images)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activityId** | **kotlin.Int**|  |
 **images** | **kotlin.collections.List&lt;java.io.File&gt;**|  |

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

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

<a id="uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost"></a>
# **uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost**
> kotlin.Any uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost(activityId, image)

Upload Hero Image

### Example
```kotlin
// Import classes:
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiInstance = DefaultApi()
val activityId : kotlin.Int = 56 // kotlin.Int | 
val image : java.io.File = BINARY_DATA_HERE // java.io.File | 
try {
    val result : kotlin.Any = apiInstance.uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost(activityId, image)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost")
    e.printStackTrace()
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activityId** | **kotlin.Int**|  |
 **image** | **java.io.File**|  |

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

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

