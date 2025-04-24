# Places of Interest API

**Description:**  
Provides details about interesting and historical places in Swakopmund.

**Platforms:**  
iOS, Android, Web.

---

## Endpoints Summary

| Name            | Method | Request Data                                          | Return Data                          |
|-----------------|--------|--------------------------------------------------------|--------------------------------------|
| GetPlaces       | GET    | `name` (optional)                                     | List of places                       |
| GetPlaceDetails | GET    | `id` (path param)                                     | Detailed information about a place   |
| AddNewPlace     | POST   | `name`, `description`, `images`, `userId`             | 200 status code if successful        |
| EditPlace       | POST   | `name`, `description`, `images`                       | 200 status code if successful        |
| AddReview       | POST   | `id` (path param), `userId`, `rating`, `comment`      | 200 status code if successful        |

---

## Database Structure

### ReviewType
- id
- name (interesting_place, restuarant, activity, accomodation)

### UserReviews
- id
- user_id
- comment
- type
- rating
- *date_created*
- *date_updated*

### InterestingPlaceReview
- place_id
- review_id
- *date_created*
- *date_updated*

### InterestingPlaceImage
- place_id
- image_url
- *date_created*
- *date_updated*

### InterestingPlace
- id **( PK )**
- name
- description
- location
- *date_created*
- *date_updated*
