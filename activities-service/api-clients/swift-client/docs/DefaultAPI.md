# DefaultAPI

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createNewActivityApiActivitiesPost**](DefaultAPI.md#createnewactivityapiactivitiespost) | **POST** /api/activities/ | Create New Activity
[**createNewActivityReviewApiActivitiesReviewsPost**](DefaultAPI.md#createnewactivityreviewapiactivitiesreviewspost) | **POST** /api/activities/reviews/ | Create New Activity Review
[**deleteActivityApiActivitiesActivityIdDelete**](DefaultAPI.md#deleteactivityapiactivitiesactivityiddelete) | **DELETE** /api/activities/{activity_id} | Delete Activity
[**deleteActivityImagesApiActivitiesImagesImageIdDelete**](DefaultAPI.md#deleteactivityimagesapiactivitiesimagesimageiddelete) | **DELETE** /api/activities/images/{image_id} | Delete Activity Images
[**deleteActivityReviewApiActivitiesReviewsReviewIdDelete**](DefaultAPI.md#deleteactivityreviewapiactivitiesreviewsreviewiddelete) | **DELETE** /api/activities/reviews/{review_id} | Delete Activity Review
[**getActivitiesApiActivitiesSearchGet**](DefaultAPI.md#getactivitiesapiactivitiessearchget) | **GET** /api/activities/search | Get Activities
[**getActivitiesByLocationApiActivitiesSearchLocationGet**](DefaultAPI.md#getactivitiesbylocationapiactivitiessearchlocationget) | **GET** /api/activities/search/location | Get Activities By Location
[**getActivityApiActivitiesActivityIdGet**](DefaultAPI.md#getactivityapiactivitiesactivityidget) | **GET** /api/activities/{activity_id} | Get Activity
[**getActivityImagesApiActivitiesImagesActivityActivityIdGet**](DefaultAPI.md#getactivityimagesapiactivitiesimagesactivityactivityidget) | **GET** /api/activities/images/activity/{activity_id} | Get Activity Images
[**getImageApiActivitiesImagesImageIdGet**](DefaultAPI.md#getimageapiactivitiesimagesimageidget) | **GET** /api/activities/images/{image_id} | Get Image
[**getReviewsApiActivitiesReviewsGet**](DefaultAPI.md#getreviewsapiactivitiesreviewsget) | **GET** /api/activities/reviews/ | Get Reviews
[**updateActivityApiActivitiesEditPost**](DefaultAPI.md#updateactivityapiactivitieseditpost) | **POST** /api/activities/edit | Update Activity
[**uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost**](DefaultAPI.md#uploadactivityimagesapiactivitiesimagesactivityactivityiduploadpost) | **POST** /api/activities/images/activity/{activity_id}/upload | Upload Activity Images
[**uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost**](DefaultAPI.md#uploadheroimageapiactivitiesimagesactivityactivityidherouploadpost) | **POST** /api/activities/images/activity/{activity_id}/hero/upload | Upload Hero Image


# **createNewActivityApiActivitiesPost**
```swift
    open class func createNewActivityApiActivitiesPost(name: String, type: Int, latitude: Double, longitude: Double, address: String, bookingUrl: String, description: String? = nil, files: [URL]? = nil, heroImage: URL? = nil, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Create New Activity

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let name = "name_example" // String | 
let type = 987 // Int | 
let latitude = 987 // Double | 
let longitude = 987 // Double | 
let address = "address_example" // String | 
let bookingUrl = "bookingUrl_example" // String | 
let description = "description_example" // String |  (optional)
let files = [URL(string: "https://example.com")!] // [URL] |  (optional)
let heroImage = URL(string: "https://example.com")! // URL |  (optional)

// Create New Activity
DefaultAPI.createNewActivityApiActivitiesPost(name: name, type: type, latitude: latitude, longitude: longitude, address: address, bookingUrl: bookingUrl, description: description, files: files, heroImage: heroImage) { (response, error) in
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
 **name** | **String** |  | 
 **type** | **Int** |  | 
 **latitude** | **Double** |  | 
 **longitude** | **Double** |  | 
 **address** | **String** |  | 
 **bookingUrl** | **String** |  | 
 **description** | **String** |  | [optional] 
 **files** | [**[URL]**](URL.md) |  | [optional] 
 **heroImage** | **URL** |  | [optional] 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createNewActivityReviewApiActivitiesReviewsPost**
```swift
    open class func createNewActivityReviewApiActivitiesReviewsPost(createReviewDTO: CreateReviewDTO, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Create New Activity Review

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let createReviewDTO = CreateReviewDTO(activityId: 123, rating: 123, review: "review_example") // CreateReviewDTO | 

// Create New Activity Review
DefaultAPI.createNewActivityReviewApiActivitiesReviewsPost(createReviewDTO: createReviewDTO) { (response, error) in
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
 **createReviewDTO** | [**CreateReviewDTO**](CreateReviewDTO.md) |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteActivityApiActivitiesActivityIdDelete**
```swift
    open class func deleteActivityApiActivitiesActivityIdDelete(activityId: Int, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Delete Activity

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let activityId = 987 // Int | 

// Delete Activity
DefaultAPI.deleteActivityApiActivitiesActivityIdDelete(activityId: activityId) { (response, error) in
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
 **activityId** | **Int** |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteActivityImagesApiActivitiesImagesImageIdDelete**
```swift
    open class func deleteActivityImagesApiActivitiesImagesImageIdDelete(imageId: Int, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Delete Activity Images

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let imageId = 987 // Int | 

// Delete Activity Images
DefaultAPI.deleteActivityImagesApiActivitiesImagesImageIdDelete(imageId: imageId) { (response, error) in
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
 **imageId** | **Int** |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteActivityReviewApiActivitiesReviewsReviewIdDelete**
```swift
    open class func deleteActivityReviewApiActivitiesReviewsReviewIdDelete(reviewId: Int, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Delete Activity Review

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let reviewId = 987 // Int | 

// Delete Activity Review
DefaultAPI.deleteActivityReviewApiActivitiesReviewsReviewIdDelete(reviewId: reviewId) { (response, error) in
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
 **reviewId** | **Int** |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getActivitiesApiActivitiesSearchGet**
```swift
    open class func getActivitiesApiActivitiesSearchGet(searchTerm: String? = nil, sortField: String? = nil, sortOrder: String? = nil, limit: Int? = nil, page: Int? = nil, categories: String? = nil, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Get Activities

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let searchTerm = "searchTerm_example" // String |  (optional) (default to "")
let sortField = "sortField_example" // String |  (optional) (default to "id")
let sortOrder = "sortOrder_example" // String |  (optional) (default to "desc")
let limit = 987 // Int |  (optional) (default to 10)
let page = 987 // Int |  (optional) (default to 1)
let categories = "categories_example" // String |  (optional)

// Get Activities
DefaultAPI.getActivitiesApiActivitiesSearchGet(searchTerm: searchTerm, sortField: sortField, sortOrder: sortOrder, limit: limit, page: page, categories: categories) { (response, error) in
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
 **categories** | **String** |  | [optional] 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getActivitiesByLocationApiActivitiesSearchLocationGet**
```swift
    open class func getActivitiesByLocationApiActivitiesSearchLocationGet(latitude: Double, longitude: Double, radius: Int? = nil, searchTerm: String? = nil, categories: String? = nil, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Get Activities By Location

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let latitude = 987 // Double | 
let longitude = 987 // Double | 
let radius = 987 // Int |  (optional) (default to 1000)
let searchTerm = "searchTerm_example" // String |  (optional) (default to "")
let categories = "categories_example" // String |  (optional)

// Get Activities By Location
DefaultAPI.getActivitiesByLocationApiActivitiesSearchLocationGet(latitude: latitude, longitude: longitude, radius: radius, searchTerm: searchTerm, categories: categories) { (response, error) in
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
 **latitude** | **Double** |  | 
 **longitude** | **Double** |  | 
 **radius** | **Int** |  | [optional] [default to 1000]
 **searchTerm** | **String** |  | [optional] [default to &quot;&quot;]
 **categories** | **String** |  | [optional] 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getActivityApiActivitiesActivityIdGet**
```swift
    open class func getActivityApiActivitiesActivityIdGet(activityId: Int, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Get Activity

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let activityId = 987 // Int | 

// Get Activity
DefaultAPI.getActivityApiActivitiesActivityIdGet(activityId: activityId) { (response, error) in
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
 **activityId** | **Int** |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getActivityImagesApiActivitiesImagesActivityActivityIdGet**
```swift
    open class func getActivityImagesApiActivitiesImagesActivityActivityIdGet(activityId: Int, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Get Activity Images

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let activityId = 987 // Int | 

// Get Activity Images
DefaultAPI.getActivityImagesApiActivitiesImagesActivityActivityIdGet(activityId: activityId) { (response, error) in
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
 **activityId** | **Int** |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getImageApiActivitiesImagesImageIdGet**
```swift
    open class func getImageApiActivitiesImagesImageIdGet(imageId: Int, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Get Image

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let imageId = 987 // Int | 

// Get Image
DefaultAPI.getImageApiActivitiesImagesImageIdGet(imageId: imageId) { (response, error) in
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
 **imageId** | **Int** |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getReviewsApiActivitiesReviewsGet**
```swift
    open class func getReviewsApiActivitiesReviewsGet(searchTerm: String? = nil, sortField: String? = nil, sortOrder: String? = nil, limit: Int? = nil, page: Int? = nil, activityId: Int? = nil, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Get Reviews

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let searchTerm = "searchTerm_example" // String |  (optional) (default to "")
let sortField = "sortField_example" // String |  (optional) (default to "id")
let sortOrder = "sortOrder_example" // String |  (optional) (default to "desc")
let limit = 987 // Int |  (optional) (default to 10)
let page = 987 // Int |  (optional) (default to 1)
let activityId = 987 // Int |  (optional) (default to 0)

// Get Reviews
DefaultAPI.getReviewsApiActivitiesReviewsGet(searchTerm: searchTerm, sortField: sortField, sortOrder: sortOrder, limit: limit, page: page, activityId: activityId) { (response, error) in
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
 **activityId** | **Int** |  | [optional] [default to 0]

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateActivityApiActivitiesEditPost**
```swift
    open class func updateActivityApiActivitiesEditPost(activityEditDTO: ActivityEditDTO, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Update Activity

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let activityEditDTO = ActivityEditDTO(name: "name_example", description: "description_example", latitude: 123, longitude: 123, type: 123, address: "address_example", bookingUrl: "bookingUrl_example", id: 123) // ActivityEditDTO | 

// Update Activity
DefaultAPI.updateActivityApiActivitiesEditPost(activityEditDTO: activityEditDTO) { (response, error) in
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
 **activityEditDTO** | [**ActivityEditDTO**](ActivityEditDTO.md) |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost**
```swift
    open class func uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost(activityId: Int, images: [URL], completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Upload Activity Images

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let activityId = 987 // Int | 
let images = [URL(string: "https://example.com")!] // [URL] | 

// Upload Activity Images
DefaultAPI.uploadActivityImagesApiActivitiesImagesActivityActivityIdUploadPost(activityId: activityId, images: images) { (response, error) in
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
 **activityId** | **Int** |  | 
 **images** | [**[URL]**](URL.md) |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost**
```swift
    open class func uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost(activityId: Int, image: URL, completion: @escaping (_ data: AnyCodable?, _ error: Error?) -> Void)
```

Upload Hero Image

### Example
```swift
// The following code samples are still beta. For any issue, please report via http://github.com/OpenAPITools/openapi-generator/issues/new
import OpenAPIClient

let activityId = 987 // Int | 
let image = URL(string: "https://example.com")! // URL | 

// Upload Hero Image
DefaultAPI.uploadHeroImageApiActivitiesImagesActivityActivityIdHeroUploadPost(activityId: activityId, image: image) { (response, error) in
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
 **activityId** | **Int** |  | 
 **image** | **URL** |  | 

### Return type

**AnyCodable**

### Authorization

[Authorization](../README.md#Authorization), [X-API-KEY](../README.md#X-API-KEY)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

