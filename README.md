# User Management API with Flask and Swagger

This project is a RESTful API built using Flask and Flask-RESTx, featuring Swagger documentation for a User Management system. The API allows CRUD operations on user data and provides an interactive Swagger UI for testing and documentation.

## Features

#### Endpoints:
- `GET /api/users` - List all users.

- `POST /api/users` - Create a new user.

- `GET /api/users/<id>` - Retrieve a user by ID.

- `PUT /api/users/<id>` - Update user details.

- `DELETE /api/users/<id>` - Delete a user.

#### Swagger Documentation:

- Auto-generated API documentation with Swagger UI.

- Available at /swagger.


## Project Structure

```
Swagger
├── service
│   ├── app.py
├── .gitignore
├── requirements.txt
```


## Technical Details

### Backend:
- **Flask**: Python web framework.

- **Flask-RESTx**: Extension for building REST APIs with Swagger support.

### Documentation:
- **Swagger UI**: Interactive API documentation.


### Data model
- User Model 
     ```
    "id": "integer (auto-generated)",
    "username": "string",
    "email": "string",
    "created_at": "DateTime"
    ```

### Error Handling

The API returns appropriate **HTTP status codes** to indicate the result of each request:

- **200**: Success  
  The request was successful, and the response contains the expected data.

- **201**: Created successfully  
  The request was successful, and a new resource has been created.


- **404**: Not found  
  The requested resource could not be found.



## Requirements

- Python 3
- Flask
- Flask-RESTx

All project dependencies are listed in the `requirements.txt` file.

## Installation and Setup

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Shazid18/Swagger_Documentation.git
   cd Swagger_Documentation
   ```
2. **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate     # For Windows
   ```
3. **Install Dependencies**
    ```bash
   pip install -r requirements.txt
   ```
4. **Run The Service**
    ```bash
    cd service
    python app.py
   ```
5. **Access Swagger UI**
   
   Open your browser an navigate to : http://127.0.0.1:5000/swagger

 
## Conclusion

This project demonstrates the integration of Swagger documentation into a Flask application using Flask-RESTx. It provides a user-friendly, interactive interface for API testing and enhances the overall development and collaboration experience. By standardizing API documentation and ensuring ease of use, this project serves as a strong foundation for scalable and maintainable RESTful applications. Future enhancements, such as authentication and advanced features, can further elevate the utility and security of the API.
