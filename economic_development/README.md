# Economic Development API

**Purpose:**  
Support and promote local tourism and business initiatives.

**Users:**  
Business Owners, Tourists, Municipal Business Support Department.

---

## Endpoints Summary

| Name                   | Method | Request Data        | Return Data                                 |
|------------------------|--------|---------------------|----------------------------------------------|
| businesses/registered  | GET    | `searchString`      | List of registered businesses                |
| businesses/register    | POST   | Application form    | 200 status code if successful                |
| tourism/attractions    | GET    | `searchString`      | List of top tourist attractions in Swakopmund|
| tourism/events         | GET    | `searchString`      | Upcoming tourism-related events              |
