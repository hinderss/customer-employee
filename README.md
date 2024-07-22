# Customers-Employees Task Manager
## Company task manager service.
- django 5.0.6
- djangorestframework 3.15.2
### API Endpoints

1. **Default Router URLs**
   - **Endpoint**: 
   ```
    /
   ```
   - **Description**: Includes all the default URLs provided by the Django REST Framework's router for view sets.

2. **Token Obtain Pair**
   - **Endpoint**: 
   ```
   /api/token/
   ```
   - **Description**: Obtains a pair of access and refresh tokens for authentication.
   - **Method**: POST
   - **Request Body**:
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```

3. **Token Refresh**
- **Endpoint**: 
   ```
  /api/token/refresh/
  ```
  - **Description**: Refreshes the access token using a refresh token.
  - **Method**: POST
  - **Request Body**:
    ```json
    {
      "refresh": "your_refresh_token"
    }
    ```

4. **Customer Registration**
   - **Endpoint**: 
   ```
   /register/customer/
   ```
   - **Description**: Registers a new customer.
   - **Required Permissions**: `can_add_customer`
   - **Method**: POST
   - **Request Body**:
     ```json
     {
       "username": "customer1",
       "password": "password",
       "first_name": "John",
       "last_name": "Doe",
       "email": "johndoe@example.com",
       "phone": "+123456789"
     }
     ```

5. **Employee Registration**
   - **Endpoint**: 
   ```
    /register/employee/
   ```
   - **Description**: Registers a new employee.
   - **Required Permissions**: `can_add_employee`
   - **Method**: POST
   - **Request Body**:
     ```json
     {
       "username": "employee1",
       "password": "password",
       "first_name": "John",
       "last_name": "Doe",
       "email": "johndoe@example.com",
       "phone": "+987654321"
     }
     ```

6. **Employee List**
   - **Endpoint**: 
   ```
   /employees/
   ```
   - **Description**: Lists all employees.
   - **Required Permissions**: `can_view_employees`
   - **Method**: GET

7. **Current User Information**
   - **Endpoint**: 
   ```
   /me/
   ```
   - **Description**: Retrieves information about the current authenticated user.
   - **Method**: GET

8. **Task Creation**
   - **Endpoint**: 
   ```
   /tasks/
   ```
   - **Description**: Creates a new task.
   - **Required Permissions**: `can_add_employee` or to be `Customer`
   - **Method**: POST
   - **Request Body**:
     ```json
     {
       "customer_id": 1
     }
     ```

9. **Assign Task**
   - **Endpoint**: 
   ```
   /tasks/<int:pk>/assign/
   ```
   - **Description**: Assigns a task to an employee.
   - **Required Permissions**: to be `Employee`
   - **Method**: PATCH
   - **Request Body**:
     ```json
     {
       "employee_id": 1  // Employee ID
     }
     ```

10. **Complete Task**
    - **Endpoint**: 
	```
	/tasks/<int:pk>/complete/
	```
    - **Description**: Marks a task as complete.
    - **Required Permissions**: to be `Employee`
    - **Method**: PATCH
    - **Request Body**:
      ```json
      {
        "report": "Report"
      }
      ```

### Atomic Permissions

**Employee Permissions**:
1. **can_create_task**
   - **Description**: Can create a new task.
   - **Usage**: Allows employees to create tasks in the system.

2. **can_view_all_tasks**
   - **Description**: Can view all tasks.
   - **Usage**: Grants employees the ability to view all tasks, not just the ones assigned to them.

3. **can_add_customer**
   - **Description**: Can add a new customer.
   - **Usage**: Allows employees to register new customers in the system.

4. **can_add_employee**
   - **Description**: Can add a new employee.
   - **Usage**: Allows employees to register new employees in the system.

**Customer Permissions**:
1. **can_view_employees**
   - **Description**: Can view employees.
   - **Usage**: Grants customers the ability to see the list of employees in the system.


### Pre-registered Administrator

During setup, a pre-registered administrator account is available for initial access:

- **Username:** `admin`
- **Password:** `password`

This administrator account has full permissions to manage all aspects of the application.

### Environment Configuration
To run the application, you need to create a `.env` file with the following content:
```
SECRET_KEY = 'your_security_key'
DEBUG = False
```

Replace `'your_security_key'` with a secure, random string.
